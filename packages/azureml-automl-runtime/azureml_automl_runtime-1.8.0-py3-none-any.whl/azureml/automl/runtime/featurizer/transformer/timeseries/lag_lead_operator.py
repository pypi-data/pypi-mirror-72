# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Create lags and leads (negative lags) of target and features."""
from typing import Any, Dict, Optional, List, Union, cast, Iterable
from warnings import warn, filterwarnings

import pandas as pd
import numpy as np
import gc
import datetime

from azureml.automl.core.shared.constants import TimeSeriesInternal, TimeSeries
from azureml.automl.core.shared.forecasting_exception import NotTimeSeriesDataFrameException, \
    DuplicatedIndexException, ColumnTypeNotSupportedException
from azureml.automl.core.shared.exceptions import ConfigException,\
    ClientException, FitException
from azureml.automl.core.shared.forecasting_utils import flatten_list, invert_dict_of_lists
from azureml.automl.core.shared.forecasting_verify import is_list_oftype, is_iterable_but_not_string, Messages
from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.time_series_data_frame import TimeSeriesDataFrame
from .forecasting_base_estimator import AzureMLForecastTransformerBase
from .forecasting_constants import ORIGIN_TIME_COLNAME_DEFAULT
from .transform_utils import OriginTimeMixin
from .time_series_imputer import TimeSeriesImputer
from .max_horizon_featurizer import MaxHorizonFeaturizer
from azureml.automl.runtime.featurizer.transformer.timeseries.missingdummies_transformer import \
    MissingDummiesTransformer


class LagLeadOperator(AzureMLForecastTransformerBase, OriginTimeMixin):
    """
    A transformation class for computing lags and leads for values.
    Work for general time series data sets, sparse or non-sparse.
    Has two lag options: "lag_by_time" or "lag_by_occurrence"
    default: "lag_by_occurrence"
    "lag_by_time" is good for (almost) evenly spaced time series data, while
    "lag_by_occurrence" is a better option for non-evenly spaced data
    This module will automatically select the right one by checking
    data sparsity.

    .. py:class:: LagLeadOperator

    .. _pandas.Series.shift: https://pandas.pydata.org/pandas-docs/stable/
                            generated/pandas.Series.shift.html

    This will be used as a featurization step inside the forecast pipeline.

    :param lags:
        dictionary of the form {'column_to_lag' : [lag_order1, lag_order2]}.
        Dictionary keys must be names of columns in the data frame to which
        the transform is applied. Dictionary values are either integers or
        lists of integers indicating what lags must be constructed.
        Negative values are allowed, and indicate 'leads' i.e. moving into
        the future values of time series.
    :type lags: dict

    :param max_horizon:
        how many steps ahead do you intend to predict the series later. This
        is used to construct a full grid of `time` and `origin_time` to make
        sure that output is compatible with multi-step forecasting featurizers
        downstream. This argument is ignored if the input data has
        `origin_time_colname` set, because it is assumed that the job of
        setting up multi-horizon data structure had already been performed.
        Defaults to 1 to produce expected behavior for most users.
    :type max_horizon: int

    :param dropna:
        should missing values from lag creation be dropped? Defaults to False.
        Note that the missing values from the test data are not dropped but
        are instead 'filled in' with values from training data.
    :type dropna: bool

    :param origin_time_column_name:
        how to name the `origin_time` column when the input does not contain
        one. Must be a single string. This argument is ignored if the input
        data has `origin_time_colname` set, because it is assumed that the job
        of setting up multi-horizon data structure had already been performed.
        Defaults to "origin".
    :type origin_time_column_name: str

    :param overwrite_columns:
        Flag that permits the transform to overwrite existing columns in the
        input TimeSeriesDataFrame for features that are already present in it.
        If True, prints a warning and overwrites columns.
        If False, throws a RuntimeError.
        Defaults to False to protect user data.
    :type overwrite_columns: bool

    :param backfill_cache:
                         Back fill the chache to avoid NaNs to prevent the output data
                         frame shape degradation.
    :type backfill_cache: bool

    Example 1 (Evenly Spaced Time Series Data, Will Use Lag_By_Time):
    Construct a small TimeSeriesDataFrame:

    >>> raw_data = {'store': ['storeA'] * 3 + ['storeB'] * 4,
    ...             'date' : pd.to_datetime(
    ...                 ['2017-01-01', '2017-02-01', '2017-03-01'] * 2 +
    ...                 ['2017-04-01'] ),
    ...             'sales': range(8, 15)}
    >>> tsdf = TimeSeriesDataFrame(
    ...    data=pd.DataFrame(raw_data),
    ...    grain_colnames=['store'], time_colname=['date'],
    ...    ts_value_colname='sales')
    >>> tsdf = tsdf.set_index(['store', 'date']).sort_index()
    >>> tsdf
                            sales
    store      date
    storeA     2017-01-01      8
               2017-02-01      9
               2017-03-01     10
    storeB     2017-01-01     11
               2017-02-01     12
               2017-03-01     13
               2017-04-01     14
    >>> tsdf=MaxHorizonFeaturizer(1).fit_transform(tsdf)
                                     sales  horizon_origin
    store      date       origin
    storeA     2017-01-01 2016-12-01     8               1
               2017-02-01 2017-01-01     9               1
               2017-03-01 2017-02-01    10               1
    storeB     2017-01-01 2016-12-01    11               1
               2017-02-01 2017-01-01    12               1
               2017-03-01 2017-02-01    13               1
               2017-04-01 2017-03-01    14               1
    >>> make_lags = LagLeadOperator(
    ...                 lags_to_construct={'sales': [-1, 1]})
    >>> make_lags.fit(tsdf)
    >>> result = make_lags.transform(tsdf)
    >>> result
                                     sales  horizon_origin  sales_lead1  sales_lag1
    store      date       origin
    storeA     2017-01-01 2016-12-01     8               1         9.00         nan
               2017-02-01 2017-01-01     9               1        10.00        8.00
               2017-03-01 2017-02-01    10               1          nan        9.00
    storeB     2017-01-01 2016-12-01    11               1        12.00         nan
               2017-02-01 2017-01-01    12               1        13.00       11.00
               2017-03-01 2017-02-01    13               1        14.00       12.00
               2017-04-01 2017-03-01    14               1          nan       13.00

    Example 2 (Non-evenly Spaced Time Series Data, Will Use Lag_By_Occurrence):
    Construct a small TimeSeriesDataFrame:

    >>> raw_data = {'store': ['storeA'] * 3 + ['storeB'] * 4,
    ...             'date' : pd.to_datetime(
    ...                 ['2017-01-01', '2017-02-01', '2017-04-01'] * 2 +
    ...                 ['2017-07-01'] ),
    ...             'sales': range(8, 15)}
    >>> tsdf = TimeSeriesDataFrame(
    ...    data=pd.DataFrame(raw_data),
    ...    grain_colnames=['store'], time_colname=['date'],
    ...    ts_value_colname='sales')
    >>> tsdf = tsdf.set_index(['store', 'date']).sort_index()
    >>> tsdf
                            sales
    store      date
    storeA     2017-01-01      8
               2017-02-01      9
               2017-04-01     10
    storeB     2017-01-01     11
               2017-02-01     12
               2017-04-01     13
               2017-07-01     14
    >>> tsdf=MaxHorizonFeaturizer(1).fit_transform(tsdf)
    >>> tsdf
                                     sales  horizon_origin
    store      date       origin
    storeA     2017-01-01 2016-12-01     8               1
               2017-02-01 2017-01-01     9               1
               2017-04-01 2017-03-01    10               1
    storeB     2017-01-01 2016-12-01    11               1
               2017-02-01 2017-01-01    12               1
               2017-04-01 2017-03-01    13               1
               2017-07-01 2017-06-01    14               1
    >>> make_lags = LagLeadOperator(
    ...                 lags_to_construct={'sales': [1]})
    >>> make_lags.fit(tsdf)
    >>> result = make_lags.transform(tsdf)
    >>> result
                                     sales  horizon_origin   sales_occurrence_lag1  date_occurrence_lag1_timeDiffDays
    store      date       origin
    storeA     2017-01-01 2016-12-01     8               1                     nan                                nan
               2017-02-01 2017-01-01     9               1                    8.00                                 31
               2017-04-01 2017-03-01    10               1                    9.00                                 59
    storeB     2017-01-01 2016-12-01    11               1                     nan                                nan
               2017-02-01 2017-01-01    12               1                   11.00                                 31
               2017-04-01 2017-03-01    13               1                   12.00                                 59
               2017-07-01 2017-06-01    14               1                   13.00                                 91
    """

    LAG_BY_TIME = 'lag_by_time'
    LAG_BY_OCCURRENCE = 'lag_by_occurrence'
    SPARSITY_THRESHOLD = 0.02  # threshold parameter to decide between lag by time and occurrence options

    def __init__(self,
                 lags: Dict[str, Union[int, List[int]]],
                 max_horizon: int = 1, dropna: bool = False,
                 origin_time_column_name: str = ORIGIN_TIME_COLNAME_DEFAULT,
                 overwrite_columns: bool = False,
                 backfill_cache: bool = False) -> None:
        """Create a LagLeadOperator."""
        super().__init__()
        self.lags_to_construct = lags
        self.max_horizon = max_horizon
        self.dropna = dropna
        self.origin_time_colname = origin_time_column_name
        self.overwrite_columns = overwrite_columns
        self.backfill_cache = backfill_cache

        # lag options: "lag_by_time" or "lag_by_occurrence"
        # default: "lag_by_occurrence"
        # "lag_by_time" is good for (almost) evenly spaced time series data, while
        # "lag_by_occurrence" is a better option for non-evenly spaced data
        self.lag_option = LagLeadOperator.LAG_BY_OCCURRENCE

        # iniitialize fitted status - to False, obviously
        self._is_fit = False
        self._cache = None
        self._ts_freq = None
        # set the flag for train and test set
        self._in_fit_transform = False

    ############################################################################
    # Housekeeping - use properties to rule out incorrect inputs from users
    ############################################################################
    @property
    def lags_to_construct(self) -> Dict[str, Union[int, List[int]]]:
        """Get the dictionary of column names to lists of lags/leads to construct."""
        return self._lags_to_construct

    # set value of _lags_to_constuct, and check for incorrect user input
    @lags_to_construct.setter
    def lags_to_construct(self, value: Dict[str, Union[int, List[int]]]) -> None:
        # check if input value is a dict
        if not isinstance(value, dict):
            error_msg = 'Value must be of type {0}'
            raise ConfigException(error_msg.format(
                dict), reference_code=ReferenceCodes._LAG_LEAD_LAG_TYPE
            ).with_generic_msg(error_msg.format('[MASKED]'))
        # check if all keys are strings
        try:
            is_list_oftype(list(value.keys()), str)
        except FitException:
            raise ColumnTypeNotSupportedException(
                'The list of columns must be a list of strings.',
                reference_code=ReferenceCodes._LAG_LEAD_COLUMN_TYPE,
                has_pii=False)
        # check if every value is either list of ints or an int
        for v in value.values():
            if np.issubdtype(type(v), np.signedinteger):
                pass
            elif is_iterable_but_not_string(v):
                # This assert is to pass through mypy check, the condition above handles it.
                assert(isinstance(v, Iterable))
                if not all([np.issubdtype(type(val), np.signedinteger) for val in v]):
                    error_message = \
                        ("When `lags_to_construct` input argument "
                         "is a collection, every element of it must be of "
                         "type `int`!")
                    raise ConfigException(error_message, has_pii=False,
                                          reference_code=ReferenceCodes._LAG_LEAD_LAG_TYPE_INT_LIST)
            else:
                msg = \
                    ("In 'lags_to_construct' input argument, "
                     "dictionary values must be either ints or lists of "
                     "ints. Instead got {}!")
                error_message = msg.format(type(v))
                raise ConfigException(error_message,
                                      reference_code=ReferenceCodes._LAG_LEAD_LAG_TYPE_INT
                                      ).with_generic_msg(msg.format('[Masked]'))
        # all checks passed, can assign
        self._lags_to_construct = value

    @property
    def dropna(self) -> bool:
        """See `dropna` parameter."""
        return self._dropna

    @dropna.setter
    def dropna(self, value: bool) -> None:
        if not isinstance(value, bool):
            error_message = ("Input 'dropna' must be True or False.")
            raise ClientException(error_message, has_pii=False,
                                  reference_code=ReferenceCodes._LAG_LEAD_DROPNA)
        self._dropna = value

    @property
    def max_horizon(self) -> int:
        """See `max_horizon` parameter."""
        return self._max_horizon

    @max_horizon.setter
    def max_horizon(self, value: int) -> None:
        self.verify_max_horizon_input(value)
        self._max_horizon = value

    @property
    def origin_time_colname(self) -> str:
        """See `origin_time_colname` parameter."""
        return self._origin_time_colname

    @origin_time_colname.setter
    def origin_time_colname(self, value: str) -> None:
        if not isinstance(value, str):
            msg = ('Input argument `origin_time_colname` must be a '
                   'single string, instead got {}')
            raise ColumnTypeNotSupportedException(
                msg.format(type(value)),
                reference_code=ReferenceCodes._LAG_LEAD_ORIGIN,
                has_pii=True).with_generic_msg(msg.format('[Masked]'))
        self._origin_time_colname = value

    @property
    def overwrite_columns(self) -> bool:
        """See `overwrite_columns` parameter."""
        return self._overwrite_columns

    @overwrite_columns.setter
    def overwrite_columns(self, value: bool) -> None:
        if not isinstance(value, bool):
            error_message = ("Input 'overwrite_column' must be True or "
                             "False, instead received {}")
            raise ClientException(
                error_message.format(value),
                reference_code=ReferenceCodes._LAG_LEAD_OVERWRITE_COL).with_generic_msg(
                error_message.format('[MASKED]'))
        self._overwrite_columns = value

    ############################################################################
    # Private methods: all the work is done through them
    ############################################################################

    def _check_columns_to_lag(self, X: TimeSeriesDataFrame) -> Dict[str, List[int]]:
        """
        Check from which columns user wants to construct lags.

        Exclude columns that are not in X or are properties of X.

        :param X: is a TimeSeriesDataFrame

        :return: list of valid column labels which will be lagged.
        """
        # get a list of TSDF property columns, except ts_value_colname
        property_cols = set(flatten_list([getattr(X, attr) for attr in X._metadata]))
        property_cols.remove(X.ts_value_colname)

        # if asked to lag system cols, refuse and warn
        columns_to_lag = set(self.lags_to_construct.keys())
        columns_not_to_lag = columns_to_lag.intersection(property_cols)
        if len(columns_not_to_lag) > 0:
            warning_message = ("Some of the requested columns will not be "
                               "lagged, since they are internal to TimeSeriesDataFrame! "
                               "Will not lag: {}".format(columns_not_to_lag))
            columns_to_lag = columns_to_lag - columns_not_to_lag
            warn(warning_message, UserWarning)
        # if asked to lag columns that are not in TSDF, refuse and warn
        columns_not_in_df = columns_to_lag.difference(set(X.columns))
        if len(columns_not_in_df) > 0:
            warning_message = ("Some of the requested columns will not be "
                               "lagged, since they are not present in the input "
                               "TimeSeriesDataFrame.! Will not lag: {}".format(
                                   columns_not_in_df))
            columns_to_lag = columns_to_lag - columns_not_in_df
            warn(warning_message, UserWarning)
        # clean up the dict of arguments by turning values of ints into
        # a singleton list of ints
        lags_to_construct_safe = dict()
        for column, lag_orders in self.lags_to_construct.items():
            if column in columns_to_lag:
                lag_orders_list = lag_orders if isinstance(lag_orders, list) \
                    else [lag_orders]
                lags_to_construct_safe[column] = lag_orders_list
        return lags_to_construct_safe

    def _generate_new_column_names(self) -> List[str]:
        """Generate all new column names from a dictionary of inputs."""
        new_colnames = []
        for colname, lag_orders in self.lags_to_construct.items():
            if isinstance(lag_orders, int):
                lag_orders = [lag_orders]
            for order in lag_orders:
                post_fix = "_lag" if order > 0 else "_lead"
                # append "occurrence" to lag name to match names in "_construct_one_lag..." functions
                if self.lag_option == self.LAG_BY_OCCURRENCE:
                    post_fix = "_occurrence" + post_fix
                post_fix += str(abs(order))
                if self._ts_freq:
                    try:
                        post_fix += self._ts_freq.name
                    except NotImplementedError:
                        post_fix += self._ts_freq.freqstr
                new_colname = colname + post_fix
                new_colnames.append(new_colname)
        return(new_colnames)

    def _check_for_column_overwrites(self, X: TimeSeriesDataFrame) -> None:
        """
        Check for whether existing TSDF columns are getting overwritten.

        Either a warning is printed or an exception is
        raised, depending on settings.
        """
        new_colnames = set(self._generate_new_column_names())
        input_colnames = set(X.columns)
        columns_to_overwrite = input_colnames.intersection(new_colnames)
        if len(columns_to_overwrite) > 0:
            warning_message = ('Some of the columns that are about to be '
                               'created by LagLeadOperator already exist in the input '
                               'TimeSeriesDataFrame: {}. ')
            if self.overwrite_columns:
                warning_message = warning_message.format(columns_to_overwrite)
                warning_message += 'They will be overwritten!'
                warn(warning_message, UserWarning)
            else:
                error_message = warning_message + ('Please set `overwrite_columns` '
                                                   'to `True` to proceed anyways!')
                raise ConfigException(error_message.format(columns_to_overwrite),
                                      reference_code=ReferenceCodes._LAG_LEAD_COLUMN_EXISTS
                                      ).with_generic_msg(error_message.format('[MASKED]'))

    ############################################################################
    # And the below logic handles lag_by_time features on inputs
    # with origin_time
    ############################################################################

    def _check_one_lag_inputs(self,
                              X: TimeSeriesDataFrame,
                              lag_var: str,
                              lag_order: int) -> None:
        """
        Validate that data frame, lag variable and lag order are valid.

        :param X: The data frame to generate lag on.
        :param lag_var: The name of lagging variable.
        :lag_order: the order of a lag.
        :raises: ColumnTypeNotSupportedException, ConfigException,
                 NotTimeSeriesDataFrameException, ClientException
        """
        if not isinstance(lag_var, str):
            raise ColumnTypeNotSupportedException(
                'lag_var must be of type {0}'.format(str),
                reference_code=ReferenceCodes._LAG_LEAD_COLUMN_TYPE_CONSTRUCT,
                has_pii=False)
        if not isinstance(lag_order, int):
            raise ConfigException(
                'lag_order must be of type {0}'.format(int),
                reference_code=ReferenceCodes._LAG_LEAD_LAG_TYPE_CONSTRUCT,
                has_pii=False)
        if not isinstance(X, TimeSeriesDataFrame):
            raise NotTimeSeriesDataFrameException(
                Messages.XFORM_INPUT_IS_NOT_TIMESERIESDATAFRAME, has_pii=False,
                reference_code=ReferenceCodes._LAG_LEAD_NOT_TSDF)

    def _construct_one_lag_by_time_with_origin(self,
                                               X: TimeSeriesDataFrame,
                                               lag_var: str,
                                               lag_order: int) -> TimeSeriesDataFrame:
        """
        Construct a single lag of a single variable.

        Should only be used on an argument with origin_time set.
        Returns a unindexed pandas DataFrame with a single column.
        """
        # check inputs
        self._check_one_lag_inputs(X, lag_var, lag_order)
        if X.origin_time_colname is None:
            error_message = \
                ('This method should only be called on a '
                 'TimeSeriesDataFrame in which `origin_time_colname` is set!')
            raise ClientException(
                error_message,
                reference_code=ReferenceCodes._LAG_LEAD_NO_ORIGIN,
                has_pii=False)
        # prepare pretty lag endings: foo_lagX
        lag_postfix = "_lag" if lag_order > 0 else "_lead"
        lag_postfix += str(abs(lag_order))
        if self._ts_freq:
            try:
                lag_postfix += self._ts_freq.name
            except NotImplementedError:
                lag_postfix += self._ts_freq.freqstr
        # when origin_time is not present, we have to artificially create one
        temp_df = pd.DataFrame(X).reset_index()
        lag_order_freq = cast(int, self._ts_freq)
        temp_df['lag_time'] = (temp_df[X.origin_time_colname] - lag_order_freq * (lag_order - 1))
        true_grain = list(X.grain_colnames)
        index_cols = list(flatten_list([X.time_colname] + true_grain))
        # now turn tdsf into a time series
        ts = X._extract_time_series(lag_var).reset_index()
        left_join_keys = ['lag_time'] + true_grain
        right_join_keys = index_cols
        # join creates all the lags and NaNs in the appropriate places
        temp_df = temp_df[left_join_keys]
        result = temp_df.merge(ts, how='left', left_on=left_join_keys,
                               right_on=right_join_keys)
        df_with_lags = result[[lag_var]]
        df_with_lags.columns = [lag_var + lag_postfix]
        return cast(TimeSeriesDataFrame, df_with_lags)

    def _pre_check_data(self, X: TimeSeriesDataFrame) -> None:
        """
        Pre check data prior to generating lags for all columns.

        :param X: The time series data frame to be checked.
        :raises: NotTimeSeriesDataFrameException, ClientException
        """
        if not isinstance(X, TimeSeriesDataFrame):
            raise NotTimeSeriesDataFrameException(
                Messages.XFORM_INPUT_IS_NOT_TIMESERIESDATAFRAME, has_pii=False,
                reference_code=ReferenceCodes._LAG_LEAD_NOT_TSDF_ALL)

    def _construct_all_lags_by_time_with_origin(self, X: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """Call _construct_one_lag in a loop over lags_to_construct."""
        # quick check that X is indeed a tsdf
        self._pre_check_data(X)
        if X.origin_time_colname is None:
            error_message = ('This method should only be called on a '
                             'TimeSeriesDataFrame in which `origin_time_colname` is set!')
            raise ClientException(error_message, has_pii=False,
                                  reference_code=ReferenceCodes._LAG_LEAD_NO_ORIGIN_ALL)
        tsdf_with_lags = X.copy()
        # make sure we are not lagging columns that should not be lagged
        lags_to_construct_safe = self._check_columns_to_lag(X)
        columns_to_keep = []
        for lag_var, all_lag_orders in lags_to_construct_safe.items():
            for lag_order in all_lag_orders:
                lag = self._construct_one_lag_by_time_with_origin(X, lag_var, lag_order)
                lag_name = lag.columns[0]
                tsdf_with_lags[lag_name] = lag[lag_name].values
                columns_to_keep.append(lag_name)
        # we need to return only lag columns to unify processing
        return cast(TimeSeriesDataFrame, tsdf_with_lags[columns_to_keep])

    ############################################################################
    # And the below logic handles lag_by_occurrence features generation
    # on inputs with horizon_origin
    ############################################################################

    def _construct_one_lag_by_occurrence_with_horizon_origin(self,
                                                             X: TimeSeriesDataFrame,
                                                             lag_var: str,
                                                             lag_order: int) -> TimeSeriesDataFrame:
        """
        Construct a single lag_by_occurrence of a single variable.

        Returns a unindexed pandas DataFrame with a single column.
        """
        # check inputs
        self._check_one_lag_inputs(X, lag_var, lag_order)
        if (TimeSeriesInternal.HORIZON_NAME not in X.columns):
            error_message = \
                ('This method should only be called on a '
                 'TimeSeriesDataFrame in which horizon_origin is set!')
            raise ClientException(
                error_message,
                reference_code=ReferenceCodes._LAG_LEAD_NO_HORIZON,
                has_pii=False)

        # prepare pretty lag endings: foo_occurrence_lagX
        lag_postfix = "_occurrence_lag" if lag_order > 0 else "_occurrence_lead"
        lag_postfix += str(abs(lag_order))
        if self._ts_freq:
            try:
                lag_postfix += self._ts_freq.name
            except NotImplementedError:
                lag_postfix += self._ts_freq.freqstr

        temp_df = pd.DataFrame(X).reset_index()

        true_grain = list(X.grain_colnames)
        index_cols = list(flatten_list([X.time_colname] + true_grain))

        X_temp = X.copy()

        # When TimeSeriesInternal.DUMMY_ORDER_COLUMN column is available,
        # we will rely on this column to remove imputed rows before
        # generating lag_by_occurrence features.
        if (TimeSeriesInternal.DUMMY_ORDER_COLUMN in X.columns):
            if self._in_fit_transform:
                target_dummies_name = MissingDummiesTransformer.get_column_name(TimeSeriesInternal.DUMMY_TARGET_COLUMN)
                X_temp = X[(X[TimeSeriesInternal.DUMMY_ORDER_COLUMN].notnull()) | (X[target_dummies_name] == 0)]
            else:
                X_temp = X[X[TimeSeriesInternal.DUMMY_ORDER_COLUMN].notnull()]

        ts = X_temp._extract_time_series(lag_var).reset_index()
        ts = ts.merge(temp_df[index_cols + list([TimeSeriesInternal.HORIZON_NAME])], how='left',
                      left_on=index_cols, right_on=index_cols)
        true_grain = list(X.grain_colnames) + list([TimeSeriesInternal.HORIZON_NAME])
        index_cols = list(flatten_list([X.time_colname] + true_grain))
        del X_temp
        gc.collect()

        ts.sort_values(by=[X.time_colname], inplace=True, ascending=True)
        ts['temp_seq_record_index'] = ts.groupby(true_grain).cumcount() + 1
        temp_df = temp_df.merge(ts[['temp_seq_record_index'] + index_cols], how='left', left_on=index_cols,
                                right_on=index_cols)
        temp_df['temp_seq_record_index'] = temp_df['temp_seq_record_index'] \
            - (temp_df[TimeSeriesInternal.HORIZON_NAME] - 1) - lag_order
        left_join_keys = ['temp_seq_record_index'] + true_grain
        right_join_keys = ['temp_seq_record_index'] + true_grain

        # join creates all the lags and NaNs in the appropriate places
        temp_df = temp_df[left_join_keys]
        result = temp_df.merge(ts, how='left', left_on=left_join_keys,
                               right_on=right_join_keys)
        df_with_lags = result[[lag_var]]
        df_with_lags.columns = [lag_var + lag_postfix]

        return cast(TimeSeriesDataFrame, df_with_lags)

    def _construct_all_lags_by_occurrence_with_horizon_origin(self, X: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """Call _construct_one_lag in a loop over lags_to_construct."""
        # quick check that X is indeed a tsdf
        self._pre_check_data(X)
        if (TimeSeriesInternal.HORIZON_NAME not in X.columns):
            error_message = ('This method should only be called on a '
                             'TimeSeriesDataFrame in which `horizon_origin` is set!')
            raise ClientException(error_message, has_pii=False,
                                  reference_code=ReferenceCodes._LAG_LEAD_NO_HORIZON_ALL)
        tsdf_with_lags = X.copy()

        # make sure we are not lagging columns that should not be lagged
        lags_to_construct_safe = self._check_columns_to_lag(X)
        columns_to_keep = []
        for lag_var, all_lag_orders in lags_to_construct_safe.items():
            for lag_order in all_lag_orders:
                lag = self._construct_one_lag_by_occurrence_with_horizon_origin(X, lag_var, lag_order)
                lag_name = lag.columns[0]
                tsdf_with_lags[lag_name] = lag[lag_name].values
                columns_to_keep.append(lag_name)
        # we need to return only lag columns to unify processing
        return cast(TimeSeriesDataFrame, tsdf_with_lags[columns_to_keep])

    def _set_lag_option(self, X: TimeSeriesDataFrame) -> None:
        """
        Set lag option such that it is determined in the fit()
        """
        lags_to_construct_safe = self._check_columns_to_lag(X)
        if len(lags_to_construct_safe) > 0:
            for lag_col in self.lags_to_construct.keys():
                target_dummies_name = MissingDummiesTransformer.get_column_name(lag_col)
                if target_dummies_name not in X.columns:
                    num_missing_values = 0
                else:
                    num_missing_values = (X[target_dummies_name].isna() | X[target_dummies_name] == 1).sum()
                if num_missing_values / X.shape[0] < self.SPARSITY_THRESHOLD:
                    # Data is (almost) evenly spaced, we will do lag_by_time
                    self.lag_option = LagLeadOperator.LAG_BY_TIME
                else:
                    # Data is not evenly spaced, we will do lag_by_occurrence
                    self.lag_option = LagLeadOperator.LAG_BY_OCCURRENCE
                    break

    def _cache_trailing_training_data(self, X: TimeSeriesDataFrame) -> 'LagLeadOperator':
        """
        Cache the tail end of the training data.

        When transforming test data, we should not have NaNs at the start
        because we can use tail bits of training data to obtain them.
        """
        # quick check that X is indeed a tsdf
        if not isinstance(X, TimeSeriesDataFrame):
            raise NotTimeSeriesDataFrameException(
                Messages.XFORM_INPUT_IS_NOT_TIMESERIESDATAFRAME, has_pii=False,
                reference_code=ReferenceCodes._LAG_LEAD_NOT_TSDF_CACHE)
        # find largest lag value that needs to be constructed
        lags_to_construct_safe = self._check_columns_to_lag(X)
        if len(lags_to_construct_safe) > 0:
            lags_inverse_dict = invert_dict_of_lists(lags_to_construct_safe)
            max_lag_order = max(lags_inverse_dict.keys())

            # Internal function to get trailing data for a single grain
            def get_trailing_by_grain(gr, Xgr):
                h_max = self.max_horizon_from_key_safe(gr, self.max_horizon)
                last_obs_for_cache = max_lag_order + h_max + 1
                val_series = Xgr.ts_value.sort_index(level=Xgr.time_colname)
                tail_series = val_series.iloc[-last_obs_for_cache:]
                tail_start = (tail_series.index
                              .get_level_values(Xgr.time_colname).min())
                return Xgr[Xgr.time_index >= tail_start]
            # ------------------------------------------------------------
            if self.lag_option == LagLeadOperator.LAG_BY_OCCURRENCE:
                for lag_col in self.lags_to_construct.keys():
                    target_dummies_name = MissingDummiesTransformer.get_column_name(lag_col)
                    # For generating lag_by_occurrence features, we need to
                    # remove fake imputed rows before generating cache data
                    X = X[X[target_dummies_name].notna() & X[target_dummies_name] == 0]

            # take last max_lag_order obs per grain
            if X.grain_colnames is not None:
                self._cache = X.groupby_grain().apply(
                    lambda Xgr: get_trailing_by_grain(Xgr.name, Xgr))
            else:
                self._cache = get_trailing_by_grain('', X)

            # For generating lag_by_time features, if cache contains the
            # missing value, it will result in the degradation of
            # a shape of transformed data on the data set
            # missing y values.
            # We backfill these values if backfill_cache is true.
            if(self.lag_option == LagLeadOperator.LAG_BY_TIME):
                if self._cache is not None and self.backfill_cache:
                    ts_imputer = TimeSeriesImputer(input_column=self._cache.ts_value_colname,
                                                   option='fillna',
                                                   method='bfill',
                                                   freq=self._ts_freq)
                    self._cache = ts_imputer.transform(self._cache)
        else:
            self._cache = None

        return self

    ############################################################################
    # Last, we have publicly facing fit and predict methods
    ############################################################################

    # fit method performs caching of tail bits of training data, this way
    # lags on test data are populated with non-missing values from train
    @function_debug_log_wrapped('info')
    def fit(self, X: TimeSeriesDataFrame, y: Optional[Any] = None) -> 'LagLeadOperator':
        """
        Fit the lag/lead transform.

        This method performs caching of tail bits of training data, this way
        lags on test data are populated with non-missing values from train

        :param X: Input data
        :type X: TimeSeriesDataFrame

        :param y: Ignored. Included for pipeline compatibility

        :return: Fitted transform
        :rtype: LagLeadOperator
        """
        self._ts_freq = X.infer_freq(return_freq_string=False)
        self._set_lag_option(X)
        self._check_for_column_overwrites(X)
        self._cache_trailing_training_data(X)
        self._is_fit = True

        return self

    @function_debug_log_wrapped('info')
    def transform(self, X: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """
        Construct lag columns in TimeSeriesDataFrame X.

        :param X: Input data
        :type X: TimeSeriesDataFrame

        :return: Data frame with lag/lead columns
        :rtype: TimeSeriesDataFrame
        """
        if not self._is_fit:
            error_message = ("For the LagOperator to work correctly, fit() "
                             "must be called before transform()!")
            raise ClientException(error_message, has_pii=False,
                                  reference_code=ReferenceCodes._LAG_LEAD_NO_FIT)
        # logic:
        #   1) create copy of input data
        #   2) attempt to prepend the cache to it (will fail for training data)
        #   3) call method to do lags in a loop
        #   4) left join back to original data to trim off the early rows

        output = X.copy()
        # this should work without errors when applied to test data
        # under the assumption that test comes after train :)
        try:
            temp_output = pd.concat([self._cache, output]).copy()
        # exception will be thrown when applied to train data since TSDF
        # will not allow to prepend a part of it to itself
        except DuplicatedIndexException:
            temp_output = output.copy()

        if self.lag_option == LagLeadOperator.LAG_BY_OCCURRENCE:
            if TimeSeriesInternal.HORIZON_NAME not in X.columns:
                temp_output = MaxHorizonFeaturizer(self.max_horizon).fit_transform(temp_output)
            # actual lags implemented in a separate internal method
            interim_output = self._construct_all_lags_by_occurrence_with_horizon_origin(temp_output)

            # this join makes sure that all rows that were not in the input TSDF
            # get eliminated by left join semantics
            # small step: avoiding duplicating columns
            # must take feature columns from right
            feature_columns = interim_output.columns
            non_feature_columns = output.columns.difference(feature_columns)
            # also suppress warnings from joins
            filterwarnings('ignore')
            result = output[non_feature_columns].merge(
                interim_output[feature_columns], how='left',
                left_index=True, right_index=True)
            filterwarnings('default')
            result.sort_index(level=[1, 0], inplace=True)
            # we need to do a little more work if dropna is True
            # don't want to drop rows where NaNs are not caused by the LagOperator
            if self.dropna:
                notnull_by_column = result[feature_columns].notnull().values
                not_null_all_cols = np.apply_along_axis(all, 1, notnull_by_column)
                result = result[not_null_all_cols]

        if(self.lag_option == LagLeadOperator.LAG_BY_TIME):
            if X.origin_time_colname is None:
                temp_output = self.create_origin_times(
                    temp_output, self.max_horizon, freq=self._ts_freq,
                    origin_time_colname=self.origin_time_colname)
            # Set the flag for train and test set for backwards compatibility only
            # Can be safely deleted after the next stable SDK is rolled out.
            IN_FIT_TRANSFORM = '_in_fit_transform'
            if not hasattr(self, IN_FIT_TRANSFORM):
                setattr(self, IN_FIT_TRANSFORM, False)

            # actual lags implemented in a separate internal method
            interim_output = self._construct_all_lags_by_time_with_origin(temp_output)

            # this join makes sure that all rows that were not in the input TSDF
            # get eliminated by left join semantics
            # small step: avoiding duplicating columns
            # must take feature columns from right
            feature_columns = interim_output.columns
            non_feature_columns = output.columns.difference(feature_columns)
            # also suppress warnings from joins
            filterwarnings('ignore')
            result = output[non_feature_columns].merge(
                interim_output[feature_columns], how='left',
                left_index=True, right_index=True)
            filterwarnings('default')
            result.sort_index(level=[1, 0], inplace=True)
            # we need to do a little more work if dropna is True
            # don't want to drop rows where NaNs are not caused by the LagOperator
            if self.dropna:
                notnull_by_column = result[feature_columns].notnull().values
                not_null_all_cols = np.apply_along_axis(all, 1, notnull_by_column)
                result = result[not_null_all_cols]

        return cast(TimeSeriesDataFrame, result)

    @function_debug_log_wrapped('info')
    def fit_transform(
            self,
            X: TimeSeriesDataFrame,
            y: Optional[np.ndarray] = None,
            **fit_params: Any) -> TimeSeriesDataFrame:
        """ When fit_transform() is called, perform it and set the '_in_fit_transform' flag to False.
        This flag signals that we are in the test set. This is needed for generating lags by occurrence.
        """
        self._in_fit_transform = True
        rv = super(LagLeadOperator, self).fit_transform(X, y, **fit_params)  # type: TimeSeriesDataFrame
        self._in_fit_transform = False
        return rv

    def preview_column_names(self, tsdf: TimeSeriesDataFrame, with_origin: bool = False) -> List[str]:
        """
        Get the lag lead features names that would be made if the transform were applied to X.

        :param tsdf: The TimeSeriesDataFrame to generate column names for.
        :type tsdf: TimeSeriesDataFrame
        :param with_origin: Return 'origin' column name if it was created.
        :type with_origin: bool

        :return: lag lead feature names
        :rtype: list of strings

        """
        self._ts_freq = tsdf.infer_freq(return_freq_string=False)
        # set appropriate lag_by option if the function is called directly
        if not self._is_fit:
            self._set_lag_option(tsdf)
        new_cols = self._generate_new_column_names()
        if with_origin:
            new_cols.append(self.origin_time_colname)
        return new_cols
