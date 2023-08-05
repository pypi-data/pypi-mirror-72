# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for data transformation."""
from typing import List, Union, Any, Optional, Dict, Mapping

import numpy as np
import pandas as pd
import logging
from sklearn_pandas import DataFrameMapper
import json

from .featurization import DataTransformer, data_transformer_utils, TransformerAndMapper
from .featurization._featurizer_container import FeaturizerContainer
from .featurization._unprocessed_featurizer import FeaturizerFactory
from .featurizer.transformer.featurization_utilities import get_transform_names, does_property_hold_for_featurizer
from azureml.automl.core.constants import FeaturizationRunConstants
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.exceptions import CacheException, ClientException
from azureml.automl.runtime._engineered_feature_names import _GenerateEngineeredFeatureNames
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.types import DataInputType, DataSingleColumnInputType
from azureml.automl.runtime.shared.pickler import DefaultPickler
from azureml.core import Run


logger = logging.getLogger(__name__)
_PICKLER = DefaultPickler()


def _upload_pickle(obj: Any, run_obj: Run, file_name: str) -> None:
    """
    Helper function for pickling and uploading object to storage with specified file name.

    :param obj: The object to be uploaded.
    :param run_obj: The run through which we upload the file.
    :param file_name: The name of the file to be created in storage.
    :return: None
    """
    _PICKLER.dump(obj, file_name)
    run_obj.upload_file(file_name, file_name)


def _download_pickle(file_name: str) -> Any:
    """
    Helper function for downloading file from storage.

    :param file_name: The name of the file to be downloaded.
    :return: The downloaded, unpickled object.
    """
    return _PICKLER.load(file_name)


def load_and_update_from_sweeping(data_transformer: DataTransformer,
                                  df: DataInputType) -> None:
    """
    Function called in the featurization run for updating the newly-instantiated data transformer
    with values from the setup iteration's data transformer that are necessary for full featurization.

    :param data_transformer: The data transformer to update.
    :param df: The input data used for recreating the column types mapping.
    :return: None.
    """

    run = Run.get_context()
    property_dict = run.get_properties()

    with logging_utilities.log_activity(logger=logger, activity_name="FeatureConfigDownload"):
        try:
            feature_config = _download_pickle(property_dict.get(FeaturizationRunConstants.CONFIG_PROP,
                                                                FeaturizationRunConstants.CONFIG_PATH))
        except Exception as e:
            logging_utilities.log_traceback(
                exception=e,
                logger=logger,
                override_error_msg="Error when retrieving feature config from local node storage.")
            raise e

    if data_transformer._is_onnx_compatible:
        data_transformer.mapper = feature_config
    else:
        data_transformer.transformer_and_mapper_list = feature_config

    with logging_utilities.log_activity(logger=logger, activity_name="EngineeredFeatureNamesDownload"):
        try:
            data_transformer._engineered_feature_names_class = \
                _download_pickle(property_dict.get(FeaturizationRunConstants.NAMES_PROP,
                                                   FeaturizationRunConstants.NAMES_PATH))
        except Exception as e:
            logging_utilities.log_traceback(
                exception=e,
                logger=logger,
                override_error_msg="Error when retrieving feature names from local node storage.")
            raise e

    if data_transformer._columns_types_mapping is None:
        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)

        data_transformer._columns_types_mapping = data_transformer_utils.get_pandas_columns_types_mapping(df)

    data_transformer._feature_sweeped = True


def save_feature_config(feature_config: Union[List[TransformerAndMapper], DataFrameMapper]) -> None:
    """
    Logic for saving the transformer_and_mapper_list or mapper from the setup run's data transformer.

    :param feature_config: The feature config to be downloaded and used in the featurization run.
    :return: None.
    """
    run = Run.get_context()
    with logging_utilities.log_activity(logger=logger, activity_name="FeatureConfigUpload"):
        _upload_pickle(feature_config, run, FeaturizationRunConstants.CONFIG_PATH)


def save_engineered_feature_names(engineered_feature_names: _GenerateEngineeredFeatureNames) -> None:
    """
    Logic for saving the engineered feature names from the setup run's data transformer.

    :param engineered_feature_names: The feature names to be downloaded and used in the featurization run.
    :return: None.
    """
    run = Run.get_context()
    with logging_utilities.log_activity(logger=logger, activity_name="EngineeredFeatureNamesUpload"):
        _upload_pickle(engineered_feature_names, run, FeaturizationRunConstants.NAMES_PATH)


def pull_fitted_featurizers_from_cache(cache_store: Optional[CacheStore],
                                       featurizer_container: FeaturizerContainer) -> Mapping[int, Any]:
    """
    Pull any featurizers that were already fitted and cached in their own independent runs back
    into the DataTransformer. If missing from the cache, raise an exception.

    :param cache_store: The AzureFileCacheStore.
    :param featurizer_container: Object containing featurizers and other relevant settings.
    :return: The featurizer index mapping that will be used to mutate the DataTransformer object.
    """
    cache_keys = [get_cache_key_from_index(featurizer.index) for featurizer
                  in featurizer_container if featurizer.is_cached]
    if cache_store is None:
        if len(cache_keys) > 0:
            raise ClientException("Cannot pull cached featurizers from null cache.", has_pii=False)
        return {}

    cache_store.load()
    fitted_featurizers = cache_store.get(cache_keys)
    featurizer_index_mapping = {}
    for featurizer_cache_key in cache_keys:
        index = get_data_transformer_index_from_cache_key_string(featurizer_cache_key)
        if fitted_featurizers[featurizer_cache_key] is None:  # cache lookup failed and a default value was returned
            raise CacheException("Cached entry for featurizer index {} unexpectedly missing.".format(index),
                                 has_pii=False)
        featurizer_index_mapping[index] = fitted_featurizers[featurizer_cache_key]
    return featurizer_index_mapping


def get_data_transformer_index_from_cache_key_string(key_name: str) -> int:
    """
    Given the key string used to store a fitted featurizer in the cache, extract the index.

    :param key_name: The cache key string.
    :return: The index.
    """
    return int(key_name.split('_')[-1])


def get_cache_key_from_index(index: int) -> str:
    """
    Given a featurizer's index in the DataTransformer featurizer collection, generate the cache key.

    :param index: The index.
    :return: The cache key string.
    """
    return FeaturizationRunConstants.FEATURIZER_CACHE_PREFIX + str(index)


class FeaturizationJsonParser:
    """
    Class for constructing and deconstructing the featurization JSON. Builds and saves it in the setup run for
    JOS to interpret, and processes the returned JSON from JOS in the featurization run.

    Example JSON:
    {
        "featurizers": [
            {
                "index": 0,
                "transformers": [
                    "StringCastTransformer",
                    "TfidfVectorizer"
                ]
            },
            {
                "index": 1,
                "transformers": [
                    "StringCastTransformer",
                    "TfidfVectorizer"
                ]
            },
            {
                "index": 2,
                "transformers": [
                    "StringCastTransformer",
                    "TfidfVectorizer",
                    "PretrainedTextDNNTransformer"
                ],
                "is_distributable": True,
                "is_separable": True
            }
        ]
    }
    """
    @staticmethod
    def _build_jsonifiable_featurization_props(feature_config: Union[List[TransformerAndMapper], DataFrameMapper]) \
            -> Dict[str, Union[List[Dict[str, Any]], bool]]:
        """
        Function encapsulating the JSON construction logic. Given the feature config, extracts the
        transformer names for each featurizer, notes that featurizer's index in the config, and
        associates any necessary flags (e.g. distributed) with the entry.

        :param feature_config: The feature_config generated in the setup run's data transformer.
        :return: A jsonifiable featurizer dict.
        """
        if isinstance(feature_config, DataFrameMapper):
            featurizers = [feature_config.features[i][1] for i in range(len(feature_config.features))]
        else:
            featurizers = [feature_config[i].transformers for i in range(len(feature_config))]

        featurizer_properties_list = []  # type: List[Dict[str, Any]]
        for index, featurizer in enumerate(featurizers):
            featurizer_properties_list.append({
                FeaturizationRunConstants.INDEX_KEY: index,
                FeaturizationRunConstants.TRANSFORMERS_KEY: get_transform_names(featurizer),
                FeaturizationRunConstants.IS_DISTRIBUTABLE:
                    does_property_hold_for_featurizer(featurizer, FeaturizationRunConstants.IS_DISTRIBUTABLE),
                FeaturizationRunConstants.IS_SEPARABLE:
                    does_property_hold_for_featurizer(featurizer, FeaturizationRunConstants.IS_SEPARABLE)
            })
        return {FeaturizationRunConstants.FEATURIZERS_KEY: featurizer_properties_list}

    @staticmethod
    def save_featurization_json(featurization_props: Dict[str, Union[List[Dict[str, Any]], bool]]) -> None:
        """
        Builds featurization json and saves it to the run's artifact store.

        :param featurization_props: The featurization properties distilled from the feature_config
        to be json serialized.
        :return: None.
        """
        run = Run.get_context()
        with logging_utilities.log_activity(logger=logger, activity_name="FeaturizationJsonUpload"):
            with open(FeaturizationRunConstants.FEATURIZATION_JSON_PATH, 'w') as file_obj:
                json.dump(featurization_props, file_obj)
            run.upload_file(FeaturizationRunConstants.FEATURIZATION_JSON_PATH,
                            FeaturizationRunConstants.FEATURIZATION_JSON_PATH)

    @staticmethod
    def parse_featurizer_container(json_props: str,
                                   is_onnx_compatible: bool = False) -> "FeaturizerContainer":
        """
        Given the fragment of the featurization JSON string corresponding to to the featurizer list,
        return the corresponding featurizer list object with the correct properties.

        :param json_props: The json fragment, containing the properties for the featurizers and featurizer list.
        :param is_onnx_compatible: Boolean flag for whether onnx is enabled or not.
        :return: The featurizer list object.
        """
        try:
            featurizer_container_properties = json.loads(json_props)
            list_of_featurizers = \
                [FeaturizerFactory.get_featurizer(featurizer_props, is_onnx_compatible=is_onnx_compatible)
                 for featurizer_props in featurizer_container_properties.pop(
                    FeaturizationRunConstants.FEATURIZERS_KEY)]
            return FeaturizerContainer(featurizer_list=list_of_featurizers, **featurizer_container_properties)
        except (KeyError, TypeError, json.JSONDecodeError) as e:
            logger.exception("Malformed JSON provided to independent featurizer run.")
            logging_utilities.log_traceback(e, logger)
            raise
