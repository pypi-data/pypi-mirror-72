# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Context manager that wraps an AutoML run context."""
from typing import Any, Callable, cast, Dict, List, Optional
from abc import ABC, abstractmethod
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
import json
import logging
import os
import pickle
import re

from .onnx_convert import OnnxConverter
from azureml.automl.core.shared import constants, exceptions, logging_utilities, reference_codes
from azureml.automl.runtime._run_history import RunType
import azureml.automl.core.inference as inference

# Timeout in seconds for artifact upload
ARTIFACT_UPLOAD_TIMEOUT_SECONDS = 1200
logger = logging.getLogger(__name__)


class AutoMLAbstractRunContext(ABC):
    """Wrapper class for an AutoML run context."""

    def __init__(self):
        """Initialize the run context wrapper."""
        self._run_id = None              # type: Optional[str]
        self._uploaded_artifacts = None  # type: Optional[Dict[str, Any]]

    @abstractmethod
    def _get_run_internal(self) -> RunType:
        """Retrieve the run context. Must be overridden by subclasses."""
        raise NotImplementedError  # PII safe to raise directly

    @property
    def parent_run_id(self) -> str:
        """
        Get the parent run id for this execution context, or the run id if this is a parent run.

        :return: the parent run id
        """
        match = re.fullmatch(r'(.*?)_(?:setup|[0-9]+)', self.run_id)
        if match is None:
            return self.run_id
        return match.group(1)

    @property
    def run_id(self) -> str:
        """
        Get the run id associated with the run wrapped by this run context. The run id is assumed to be immutable.

        :return: the run id
        """
        if self._run_id is None:
            with self.get_run() as run:
                self._run_id = run.id
        return cast(str, self._run_id)

    @contextmanager
    def get_run(self):
        """
        Yield a run context.

        Wrapped by contextlib to convert it to a context manager. Nested invocations will return the same run context.
        """
        yield self._get_run_internal()

    def save_model_output(self, fitted_pipeline: Any, remote_path: str, working_dir: Optional[str]) -> None:
        """
        Save the given fitted model to the given path using this run context.

        :param fitted_pipeline: the fitted model to save
        :param remote_path: the path to save to
        """
        self._save_model(fitted_pipeline, remote_path, self._save_python_model, working_dir)

    def save_onnx_model_output(self, onnx_model: object, remote_path: str, working_dir: Optional[str]) -> None:
        """
        Save the given onnx model to the given remote path using this run context.

        :param onnx_model: the onnx model to save
        :param remote_path: the path to save to
        """
        self._save_model(onnx_model, remote_path, self._save_onnx_model, working_dir)

    def save_onnx_model_resource(self, onnx_resource: Dict[Any, Any], remote_path: str, working_dir: Optional[str]) \
            -> None:
        """
        Save the given onnx model resource to the given remote path using this run context.

        :param onnx_resource: the onnx model resource dict to save
        :param remote_path: the path to save to
        """
        self._save_file(onnx_resource, remote_path, False, self._save_dict_to_json_output, working_dir)

    def _save_model(self, model_object: Any, remote_path: str,
                    serialization_method: "Callable[[Any], None]",
                    working_directory: Optional[str]) -> None:
        self._save_file(model_object, remote_path, binary_mode=True, serialization_method=serialization_method,
                        working_directory=working_directory)

    def _save_file(self, save_object: Any, remote_path: str, binary_mode: bool,
                   serialization_method: "Callable[[Any], None]",
                   working_directory: Optional[str]) -> None:
        if binary_mode:
            write_mode = "wb+"
        else:
            write_mode = "w+"
        output = None
        try:
            output = NamedTemporaryFile(mode=write_mode, delete=False, dir=working_directory)
            serialization_method(save_object, output)
            with self.get_run() as run_object:
                artifact_response = run_object.upload_file(remote_path, output.name)
                if artifact_response:
                    self._uploaded_artifacts = artifact_response.artifacts
        finally:
            if output is not None:
                output.close()
                try:
                    os.unlink(output.name)
                except PermissionError as e:
                    DeleteFileException = exceptions.DeleteFileException.from_exception(
                        e,
                        target="_save_file",
                        reference_code=reference_codes.ReferenceCodes._DELETE_FILE_PERMISSION_ERROR
                    ).with_generic_msg("PermissionError while cleaning up temp file.")
                    logging_utilities.log_traceback(DeleteFileException, logger)

    def _get_artifact_id(self, artifact_path: str) -> str:
        """
        Parse the run history response message to get the artifact ID.

        :param artifact_path: the path to artifact
        :return: the composed artifact ID string
        """
        try:
            if self._uploaded_artifacts and self._uploaded_artifacts.get(artifact_path) is not None:
                return cast(str, inference.AMLArtifactIDHeader +
                            self._uploaded_artifacts[artifact_path].artifact_id)
            else:
                return ""
        except Exception:
            return ""

    def _get_artifact_id_run_properties(self):
        properties = {
            inference.AutoMLInferenceArtifactIDs.CondaEnvDataLocation:
                self._get_artifact_id(constants.CONDA_ENV_FILE_PATH),
            inference.AutoMLInferenceArtifactIDs.ModelDataLocation:
                self._get_artifact_id(constants.MODEL_PATH)
        }
        if self._uploaded_artifacts and constants.SCORING_FILE_PATH in self._uploaded_artifacts:
            properties[inference.AutoMLInferenceArtifactIDs.ScoringDataLocation] = \
                self._get_artifact_id(constants.SCORING_FILE_PATH)
        return properties

    def _save_onnx_model(self, model_object: Any, model_output) -> None:
        OnnxConverter.save_onnx_model(model_object, model_output.name)

    def _save_python_model(self, model_object: Any, model_output) -> None:
        with(open(model_output.name, 'wb')):
            _, ext = os.path.splitext(model_output.name)
            if ext == '.pt':
                try:
                    import torch
                    torch.save(model_object, model_output)
                except Exception:
                    pickle.dump(model_object, model_output)
            else:
                pickle.dump(model_object, model_output)
            model_output.flush()

    def _save_str_output(self, str_object: Any, output) -> None:
        with open(output.name, "w") as f:
            f.write(str_object)

    def _save_dict_to_json_output(self, dict_object: Dict[Any, Any], output) -> None:
        with open(output.name, 'w') as f:
            json.dump(dict_object, f)

    def save_str_output(self, input_str: str, remote_path: str,
                        overwrite_mode: bool = False,
                        working_directory: Optional[str] = None) -> None:
        """
        Save the str file as a txt into the Artifacts.

        :param input_str: the input string.
        :param remote_path: the file name in the Artifacts.
        """
        self._save_file(input_str, remote_path, binary_mode=False,
                        serialization_method=self._save_str_output, working_directory=working_directory)

    def batch_save_artifacts(self,
                             working_directory: Optional[str],
                             input_strs: Dict[str, str],
                             model_outputs: Dict[str, Any]) -> None:
        """
        Save a batch of text files and models into the Artifacts.
        This is more efficient than saving individual artifacts.

        :param working_directory: Directory to use for temporary storage.
        :param input_strs: Dictionary of strings. The key is the artifact name and the value is the content.
        :param model_outputs: Dictionary of models. The key is the artifact name and the value is the model.
        """
        temp_files = []
        file_keys = []
        file_paths = []

        try:
            for name, contents in input_strs.items():
                text_file = NamedTemporaryFile(mode="w", delete=False, dir=working_directory)
                self._save_str_output(contents, text_file)
                temp_files.append(text_file)
                file_keys.append(name)
                file_paths.append(text_file.name)

            for name, model in model_outputs.items():
                model_file = NamedTemporaryFile(mode="wb", delete=False, dir=working_directory)
                self._save_python_model(model, model_file)
                temp_files.append(model_file)
                file_keys.append(name)
                file_paths.append(model_file.name)

            self._batch_save_artifact_files(file_keys, file_paths)

        finally:
            for f in temp_files:
                f.close()
                try:
                    os.unlink(f.name)
                except PermissionError as e:
                    DeleteFileException = exceptions.DeleteFileException.from_exception(
                        e,
                        target="batch_save_artifacts",
                        reference_code=reference_codes.ReferenceCodes._DELETE_FILE_BATCH_PERMISSION_ERROR
                    ).with_generic_msg("PermissionError while cleaning up temp file.")
                    logging_utilities.log_traceback(DeleteFileException, logger)

    def _batch_save_artifact_files(self, file_keys: List[str], file_paths: List[str]) -> None:
        """
        Save a batch of files in artifact store.
        Batch uploading files is more efficient than uploading files one by one.
        """
        with self.get_run() as run_object:
            upload_response = run_object.upload_files(file_keys, file_paths, return_artifacts=True,
                                                      timeout_seconds=ARTIFACT_UPLOAD_TIMEOUT_SECONDS)
            if upload_response:
                self._uploaded_artifacts = upload_response[0]
