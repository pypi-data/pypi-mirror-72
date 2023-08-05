# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains functionality for representing data in a tabular format by parsing the provided file or list of files.

For more information, see the article [Add & register
datasets](https://docs.microsoft.com/azure/machine-learning/how-to-create-register-datasets).
To get started working with a tabular dataset, see https://aka.ms/tabulardataset-samplenotebook.
"""

import warnings
from datetime import datetime, timedelta
from azureml.data.constants import _PUBLIC_API, _DATASET_PROP_TIMESTAMP_FINE, _DATASET_PROP_TIMESTAMP_COARSE, \
    _DEPRECATED_TIMESTAMP_NAME, _DEPRECATED_PARTITION_TIMESTAMP_NAME, _ACTION_TYPE_PROFILE, \
    _LEGACY_DATASET_ID, _TIMESERIES_WITH_TIMESTAMP_COLUMN_ACTIVITY, \
    _TIMESERIES_BEFORE_ACTIVITY, _TIMESERIES_AFTER_ACTIVITY, _TIMESERIES_BETWEEN_ACTIVITY, \
    _TIMESERIES_RECENT_ACTIVITY, _HALF_SECOND
from azureml.data.dataset_error_handling import _validate_has_data, _validate_has_columns, _try_execute
from azureml.data.abstract_dataset import AbstractDataset
from azureml.data._dataprep_helper import dataprep, get_dataflow_for_execution, get_dataflow_with_meta_flags
from azureml.data._dataset_rest_helper import _restclient, _custom_headers
from azureml.data._loggerfactory import track, _LoggerFactory, collect_datasets_usage
from azureml._base_sdk_common._docstring_wrapper import experimental


_logger = None


def _get_logger():
    global _logger
    if _logger is None:
        _logger = _LoggerFactory.get_logger(__name__)
    return _logger


class TabularDataset(AbstractDataset):
    """Represents a tabular dataset to use in Azure Machine Learning.

    A TabularDataset defines a series of lazily-evaluated, immutable operations to load data from the
    data source into tabular representation. Data is not loaded from the source until TabularDataset
    is asked to deliver data.

    TabularDataset is created using methods like
    :func:`azureml.data.dataset_factory.TabularDatasetFactory.from_delimited_files` from the
    :class:`azureml.data.dataset_factory.TabularDatasetFactory` class.

    For more information, see the article `Add & register
    datasets <https://docs.microsoft.com/azure/machine-learning/how-to-create-register-datasets>`_.
    To get started working with a tabular dataset, see https://aka.ms/tabulardataset-samplenotebook.

    .. remarks::

        A TabularDataset can be created from CSV, TSV, Parquet files, or SQL query using the ``from_*``
        methods of the :class:`azureml.data.dataset_factory.TabularDatasetFactory` class. You can
        perform subsetting operations on a TabularDataset like splitting, skipping, and filtering records.
        The result of subsetting is always one or more new TabularDataset objects.

        You can also convert a TabularDataset into other formats like a pandas DataFrame.
        The actual data loading happens when TabularDataset is asked to deliver the data into another
        storage mechanism (e.g. a Pandas Dataframe, or a CSV file).

        TabularDataset can be used as input of an experiment run. It can also be registered to workspace
        with a specified name and be retrieved by that name later.
    """

    def __init__(self):
        """Initialize a TabularDataset object.

        This constructor is not supposed to be invoked directly. Dataset is intended to be created using
        :class:`azureml.data.dataset_factory.TabularDatasetFactory` class.
        """
        super().__init__()

    @property
    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def timestamp_columns(self):
        """Return the timestamp columns.

        :return: The column names for timestamp (used to be referred as fine_grain_timestamp) and partition_timestamp
            (used to be referred as coarse grain timestamp) defined for the dataset.
        :rtype: (str, str)
        """
        timestamp = self._properties.get(_DATASET_PROP_TIMESTAMP_FINE, None)
        partition_timestamp = self._properties.get(_DATASET_PROP_TIMESTAMP_COARSE, None)
        return (timestamp, partition_timestamp)

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def with_timestamp_columns(self, timestamp=None, partition_timestamp=None, validate=False, **kwargs):
        """Define timestamp columns for the dataset.

        .. remarks::

            The method defines columns to be used as timestamps. Timestamp columns on a dataset make it possible
            to treat the data as time-series data and enable additional capabilities. When a dataset has
            both ``timestamp (used to be referred as fine_grain_timestamp)`` and ``partition_timestamp (used to be
            referred as coarse grain timestamp)`` specified, the two columns should represent the same timeline.

        :param timestamp: The name of column as timestamp (used to be referred as fine_grain_timestamp) (optional).
            The default is None(clear).
        :type timestamp: str
        :param partition_timestamp: The name of column partition_timestamp (used to be referred as coarse grain
            timestamp) (optional). The default is None(clear).
        :type partition_timestamp: str
        :param validate: Indicates whether to validate if specified columns exist in dataset. The default is False.
            Validation requires that the data source is accessible from the current compute.
        :type validate: bool
        :return: Returns a new TabularDataset with timestamp columns defined.
        :rtype: azureml.data.TabularDataset
        """
        fine_grain_timestamp = kwargs.get(_DEPRECATED_TIMESTAMP_NAME, None)
        coarse_grain_timestamp = kwargs.get(_DEPRECATED_PARTITION_TIMESTAMP_NAME, None)
        if fine_grain_timestamp:
            warnings.warn("fine_grain_timestamp is deprecated, use timestamp.", DeprecationWarning)
        if coarse_grain_timestamp:
            warnings.warn("coarse_grain_timestamp is deprecated, use partition_timestamp.", DeprecationWarning)
        if (timestamp or partition_timestamp) and (fine_grain_timestamp or coarse_grain_timestamp):
            raise ValueError('fine_grain_timestamp and coarse_grain_timestamp have been replaced by timestamp and '
                             'partition_timestamp parameters and cannot be used together.')
        if not timestamp and partition_timestamp:
            raise ValueError('partition_timestamp can be assigned only if timestamp is assigned.')
        if timestamp and timestamp == partition_timestamp:
            raise ValueError('partition_timestamp cannot be the same as timestamp.')
        if not fine_grain_timestamp and coarse_grain_timestamp:
            raise ValueError('coarse_grain_timestamp can be assigned only if fine_grain_timestamp is assigned.')
        if fine_grain_timestamp and fine_grain_timestamp == coarse_grain_timestamp:
            raise ValueError('coarse_grain_timestamp cannot be the same as fine_grain_timestamp.')
        if validate:
            self._validate_timestamp_columns([fine_grain_timestamp, coarse_grain_timestamp])
        if timestamp:
            fine_grain_timestamp = timestamp
            coarse_grain_timestamp = partition_timestamp

        if self._registration and self._registration.workspace:
            collect_datasets_usage(_get_logger(), _TIMESERIES_WITH_TIMESTAMP_COLUMN_ACTIVITY,
                                   [self], self._registration.workspace, "N/A")

        dataset = TabularDataset._create(self._dataflow, self._properties, telemetry_info=self._telemetry_info)

        if fine_grain_timestamp:
            dataset._properties[_DATASET_PROP_TIMESTAMP_FINE] = fine_grain_timestamp
        else:
            if _DATASET_PROP_TIMESTAMP_FINE in self._properties:
                del dataset._properties[_DATASET_PROP_TIMESTAMP_FINE]

        if coarse_grain_timestamp:
            dataset._properties[_DATASET_PROP_TIMESTAMP_COARSE] = coarse_grain_timestamp
        else:
            if _DATASET_PROP_TIMESTAMP_COARSE in self._properties:
                del dataset._properties[_DATASET_PROP_TIMESTAMP_COARSE]
        return dataset

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def to_pandas_dataframe(self, on_error='null', out_of_range_datetime='null'):
        """Load all records from the dataset into a pandas DataFrame.

        :param on_error: How to handle any error values in the dataset, such as those produced by an error while
            parsing values. Valid values are 'null' which replaces them with null; and 'fail' which will result in
            an exception.
        :param out_of_range_datetime: How to handle date-time values that are outside the range supported by Pandas.
            Valid values are 'null' which replaces them with null; and 'fail' which will result in an exception.
        :return: Returns a pandas DataFrame.
        :rtype: pandas.DataFrame
        """
        dataflow = get_dataflow_for_execution(self._dataflow, 'to_pandas_dataframe', 'TabularDataset')
        df = _try_execute(lambda: dataflow.to_pandas_dataframe(on_error=on_error,
                                                               out_of_range_datetime=out_of_range_datetime),
                          'to_pandas_dataframe',
                          None if self.id is None else {'id': self.id, 'name': self.name, 'version': self.version})
        fine_grain_timestamp = self._properties.get(_DATASET_PROP_TIMESTAMP_FINE, None)

        if fine_grain_timestamp is not None and df.empty is False:
            df.set_index(fine_grain_timestamp, drop=False, inplace=True)
            df.index.rename(None, inplace=True)
        return df

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def to_spark_dataframe(self):
        """Load all records from the dataset into a Spark DataFrame.

        :return: Returns a Spark DataFrame.
        :rtype: pyspark.sql.DataFrame
        """
        dataflow = get_dataflow_for_execution(self._dataflow, 'to_spark_dataframe', 'TabularDataset')
        return _try_execute(dataflow.to_spark_dataframe,
                            'to_spark_dataframe',
                            None if self.id is None else {'id': self.id, 'name': self.name, 'version': self.version})

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def skip(self, count):
        """Skip records from top of the dataset by the specified count.

        :param count: The number of records to skip.
        :type count: int
        :return: Returns a new TabularDataset object representing a dataset with records skipped.
        :rtype: azureml.data.TabularDataset
        """
        return TabularDataset._create(
            self._dataflow.skip(count), self._properties, telemetry_info=self._telemetry_info)

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def take(self, count):
        """Take a sample of records from top of the dataset by the specified count.

        :param count: The number of records to take.
        :type count: int
        :return: Returns a new TabularDataset object representing the sampled dataset.
        :rtype: azureml.data.TabularDataset
        """
        return TabularDataset._create(
            self._dataflow.take(count), self._properties, telemetry_info=self._telemetry_info)

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def take_sample(self, probability, seed=None):
        """Take a random sample of records in the dataset approximately by the probability specified.

        :param probability: The probability of a record being included in the sample.
        :type probability: float
        :param seed: Optional seed to use for the random generator.
        :type seed: int
        :return: Returns a new TabularDataset object representing the sampled dataset.
        :rtype: azureml.data.TabularDataset
        """
        return TabularDataset._create(
            self._dataflow.take_sample(probability, seed), self._properties, telemetry_info=self._telemetry_info)

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def random_split(self, percentage, seed=None):
        """Split records in the dataset into two parts randomly and approximately by the percentage specified.

        The first dataset contains approximately ``percentage`` of the total records and the second dataset the
        remaining records.

        :param percentage: The approximate percentage to split the dataset by. This must be a number between
            0.0 and 1.0.
        :type percentage: float
        :param seed: Optional seed to use for the random generator.
        :type seed: int
        :return: Returns a tuple of new TabularDataset objects representing the two datasets after the split.
        :rtype: (azureml.data.TabularDataset, azureml.data.TabularDataset)
        """
        dataflow1, dataflow2 = self._dataflow.random_split(percentage, seed)
        return (
            TabularDataset._create(dataflow1, self._properties, telemetry_info=self._telemetry_info),
            TabularDataset._create(dataflow2, self._properties, telemetry_info=self._telemetry_info)
        )

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def keep_columns(self, columns, validate=False):
        """Keep the specified columns and drops all others from the dataset.

        If a timeseries column is dropped, the corresponding capabilities will be dropped for the
        returned dataset as well.

        :param columns: The name or a list of names for the columns to keep.
        :type columns: str or builtin.list[str]
        :param validate: Indicates whether to validate if data can be loaded from the returned dataset.
            The default is False. Validation requires that the data source is accessible from current compute.
        :type validate: bool
        :return: Returns a new TabularDataset object with only the specified columns kept.
        :rtype: azureml.data.TabularDataset
        """
        dataflow = self._dataflow.keep_columns(columns, validate_column_exists=False)

        if validate:
            _validate_has_data(dataflow,
                               ('Cannot load any data from the dataset with only columns {} kept. Make sure the '
                                'specified columns exist in the current dataset.')
                               .format(columns if isinstance(columns, list) else [columns]))

        dataset = TabularDataset._create(dataflow, self._properties, telemetry_info=self._telemetry_info)

        if isinstance(columns, str):
            columns = [columns]

        ts_cols = self.timestamp_columns
        trait_dropped = None

        if ts_cols[0] is not None:
            if ts_cols[0] not in columns:
                dataset = dataset.with_timestamp_columns(None)
                trait_dropped = 'fine_grain_timestamp, coarse_grain_timestamp'
            elif ts_cols[1] is not None and ts_cols[1] not in columns:
                dataset = dataset.with_timestamp_columns(ts_cols[0])
                trait_dropped = 'coarse_grain_timestamp'

        if trait_dropped is not None:
            _get_logger().info('Dropping trait ({0}) on dataset (id={1}) during keep_columns.'
                               .format(trait_dropped, self.id))

        return dataset

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def drop_columns(self, columns):
        """Drop the specified columns from the dataset.

        If a timeseries column is dropped, the corresponding capabilities will be dropped for the
        returned dataset as well.

        :param columns: The name or a list of names for the columns to drop.
        :type columns: str or builtin.list[str]
        :return: Returns a new TabularDataset object with the specified columns dropped.
        :rtype: azureml.data.TabularDataset
        """
        dataset = TabularDataset._create(
            self._dataflow.drop_columns(columns), self._properties, telemetry_info=self._telemetry_info)

        if isinstance(columns, str):
            columns = [columns]

        ts_cols = self.timestamp_columns
        trait_dropped = None

        if ts_cols[0] is not None:
            if ts_cols[0] in columns:
                dataset = dataset.with_timestamp_columns(None)
                trait_dropped = 'fine_grain_timestamp, coarse_grain_timestamp'
            elif ts_cols[1] is not None and ts_cols[1] in columns:
                dataset = dataset.with_timestamp_columns(ts_cols[0])
                trait_dropped = 'coarse_grain_timestamp'

        if trait_dropped is not None:
            _get_logger().info('Dropping trait ({0}) on dataset (id={1}) during drop_columns.'
                               .format(trait_dropped, self.id))

        return dataset

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def to_parquet_files(self):
        """Convert the current dataset into a FileDataset containing Parquet files.

        The resulting dataset will contain one or more Parquet files, each corresponding to a partition of data
        from the current dataset. These files are not materialized until they are downloaded or read from.

        :return: Returns a new FileDataset object with a set of Parquet files containing the data in this dataset.
        :rtype: azureml.data.FileDataset
        """
        from azureml.data.file_dataset import FileDataset
        parquet_dataflow = self._dataflow.to_parquet_streams()
        parquet_dataflow = get_dataflow_with_meta_flags(parquet_dataflow, file_projection='parquet')
        return FileDataset._create(parquet_dataflow, telemetry_info=self._telemetry_info)

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def to_csv_files(self, separator=','):
        """Convert the current dataset into a FileDataset containing CSV files.

        The resulting dataset will contain one or more CSV files, each corresponding to a partition of data
        from the current dataset. These files are not materialized until they are downloaded or read from.

        :param separator: The separator to use to separate values in the resulting file.
        :type separator: str
        :return: Returns a new FileDataset object with a set of CSV files containing the data in this dataset.
        :rtype: azureml.data.FileDataset
        """
        from azureml.data.file_dataset import FileDataset
        csv_dataflow = self._dataflow.to_csv_streams(separator=separator)
        csv_dataflow = get_dataflow_with_meta_flags(csv_dataflow, file_projection='csv')
        return FileDataset._create(csv_dataflow, telemetry_info=self._telemetry_info)

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def time_before(self, end_time, include_boundary=True):
        """Filter TabularDataset with time stamp columns before a specified end time.

        :param end_time: Upper bound for filtering data.
        :type end_time: datetime.datetime
        :param include_boundary: Indicate if the row associated with the boundary time (``end_time``) should be
            included.
        :type include_boundary: bool
        :return: A TabularDataset with the new filtered dataset.
        :rtype: azureml.data.TabularDataset
        """
        if self._registration and self._registration.workspace:
            collect_datasets_usage(_get_logger(), _TIMESERIES_BEFORE_ACTIVITY,
                                   [self], self._registration.workspace, "N/A")

        return self._time_filter(self.time_before.__name__,
                                 upper_bound=end_time, include_boundary=include_boundary)

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def time_after(self, start_time, include_boundary=True):
        """Filter TabularDataset with time stamp columns after a specified start time.

        :param start_time: The lower bound for filtering data.
        :type start_time: datetime.datetime
        :param include_boundary: Indicate if the row associated with the boundary time (``start_time``) should be
            included.
        :type include_boundary: bool
        :return: A TabularDataset with the new filtered dataset.
        :rtype: azureml.data.TabularDataset
        """
        if self._registration and self._registration.workspace:
            collect_datasets_usage(_get_logger(), _TIMESERIES_AFTER_ACTIVITY,
                                   [self], self._registration.workspace, "N/A")

        return self._time_filter(self.time_after.__name__,
                                 lower_bound=start_time, include_boundary=include_boundary)

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def time_recent(self, time_delta, include_boundary=True):
        """Filter TabularDataset to contain only the specified duration (amount) of recent data.

        :param time_delta: The duration (amount) of recent data to retrieve.
        :type time_delta: datetime.timedelta
        :param include_boundary: Indicate if the row associated with the boundary time (``time_delta``)
            should be included.
        :type include_boundary: bool
        :return: A TabularDataset with the new filtered dataset.
        :rtype: azureml.data.TabularDataset
        """
        if self._registration and self._registration.workspace:
            collect_datasets_usage(_get_logger(), _TIMESERIES_RECENT_ACTIVITY,
                                   [self], self._registration.workspace, "N/A")

        start_time = datetime.now() - time_delta
        return self._time_filter(self.time_recent.__name__,
                                 lower_bound=start_time, include_boundary=include_boundary)

    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def time_between(self, start_time, end_time, include_boundary=True):
        """Filter TabularDataset between a specified start and end time.

        :param start_time: The Lower bound for filtering data.
        :type start_time: datetime.datetime
        :param end_time: The upper bound for filtering data.
        :type end_time: datetime.datetime
        :param include_boundary: Indicate if the row associated with the boundary time (``start_end`` and
            ``end_time``) should be included.
        :type include_boundary: bool
        :return: A TabularDataset with the new filtered dataset.
        :rtype: azureml.data.TabularDataset
        """
        if self._registration and self._registration.workspace:
            collect_datasets_usage(_get_logger(), _TIMESERIES_BETWEEN_ACTIVITY,
                                   [self], self._registration.workspace, "N/A")

        return self._time_filter(self.time_between.__name__,
                                 lower_bound=start_time, upper_bound=end_time, include_boundary=include_boundary)

    @experimental
    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'})
    def submit_profile_run(self, compute_target, experiment):
        """Submit an experimentation run to calculate data profile.

        A data profile can be very useful to understand the input data, identify anomalies and missing values
        by providing useful information about the data like column type, missing values, etc.

        :param compute_target: The compute target to run the
            profile calculation experiment on. Specify 'local' to use local compute.
            See https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.computetarget
            for more information on compute targets.
        :type compute_target: str or azureml.core.compute.ComputeTarget
        :param experiment: The experiment object.
            See https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.experiment.experiment
            for more information on experiments.
        :type experiment: azureml.core.experiment.Experiment
        :return: An object of type DatasetProfileRun class.
        :rtype: azureml.dataset_profile_run.DatasetProfileRun
        """
        from azureml.core import Experiment, ComputeTarget

        if not (isinstance(compute_target, ComputeTarget) or isinstance(compute_target, str)):
            raise TypeError('Invalid type. compute_target should be either of type ComputeTarget or string but '
                            'was found to be of type {0}.'.format(type(compute_target)))

        if not isinstance(experiment, Experiment):
            raise TypeError('Invalid type. experiment should be of type azureml.core.Experiment but '
                            'was found to be of type {0}.'.format(type(experiment)))

        from azureml.data.dataset_profile_run_config import DatasetProfileRunConfig
        dprc = DatasetProfileRunConfig(self, compute_target=compute_target)
        profile_run = experiment.submit(dprc)
        profile_run.run.wait_for_completion(raise_on_error=True, wait_post_processing=True)
        return profile_run

    @experimental
    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'})
    def get_profile(self, workspace=None):
        """Get data profile from the latest profile run submitted for this or the same dataset in the workspace.

        :param workspace: The workspace where profile run was submitted. Defaults to the workspace of this dataset.
            Required if dataset is not associated to a workspace.
            See https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.workspace.workspace
            for more information on workspaces.
        :type workspace: azureml.core.Workspace
        :return: Profile result from the latest profile run of type DatasetProfile.
        :rtype: azureml.dataset_profile.DatasetProfile
        """
        workspace = self._ensure_workspace(workspace)
        saved_dataset_id = self._ensure_saved(workspace)

        # arguments [{'generate_preview': 'True', 'row_count': '1000'}] are added to ensure
        # that requestHash is same. The GenerateProfileWithPreview API add these arguments on service side.
        # If any changes are made there, this should also be changed.
        from azureml._restclient.models import ActionRequestDto
        request_dto = ActionRequestDto(
            action_type=_ACTION_TYPE_PROFILE,
            saved_dataset_id=saved_dataset_id,
            arguments={'generate_preview': 'True', 'row_count': '1000'})

        action_result_dto = _restclient(workspace).dataset.get_action_result(
            workspace.subscription_id,
            workspace.resource_group,
            workspace.name,
            dataset_id=_LEGACY_DATASET_ID,
            request=request_dto,
            custom_headers=_custom_headers)
        result_artifact_ids = action_result_dto.result_artifact_ids
        if result_artifact_ids is None or len(result_artifact_ids) == 0:
            raise RuntimeError('Unable to fetch profile results. Please submit a new profile run.')
        result_artifact = result_artifact_ids[0]
        from azureml._restclient.artifacts_client import ArtifactsClient
        content = ArtifactsClient(workspace.service_context).download_artifact_contents_to_string(
            *result_artifact.split("/", 2))
        try:
            from azureml.data.dataset_profile import DatasetProfile
            profile = DatasetProfile(saved_dataset_id, action_result_dto.run_id, action_result_dto.experiment_name,
                                     workspace, dataprep().DataProfile._from_json(content))
        except Exception:
            errorMsg = 'Unable to fetch profile since profile result is corrupted. Please submit a new profile run.'
            _get_logger().error(errorMsg)
            raise RuntimeError(errorMsg)

        return profile

    @experimental
    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'})
    def get_profile_runs(self, workspace=None):
        """Return previous profile runs associated with this or same dataset in the workspace.

        :param workspace: The workspace where profile run was submitted. Defaults to the workspace of this dataset.
            Required if dataset is not associated to a workspace.
            See https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.workspace.workspace
            for more information on workspaces.
        :type workspace: azureml.core.Workspace
        :return: iterator object of type azureml.core.Run.
        :rtype: iter(azureml.core.Run)
        """
        workspace = self._ensure_workspace(workspace)
        from azureml._restclient.models import ActionRequestDto
        request_dto = ActionRequestDto(
            action_type=_ACTION_TYPE_PROFILE,
            saved_dataset_id=self._ensure_saved(workspace),
            arguments={'generate_preview': 'True', 'row_count': '1000'})

        continuation_token = None
        paginated_action_dto_list = []
        index = 0

        while index == 0 or continuation_token is not None:
            paginated_action_dto = _restclient(workspace).dataset.list_actions_from_request(
                workspace.subscription_id,
                workspace.resource_group,
                workspace.name,
                dataset_id=_LEGACY_DATASET_ID,
                request=request_dto,
                count=1000,
                custom_headers=_custom_headers,
                continuation_token=continuation_token)

            index = index + 1
            for item in paginated_action_dto.value:
                paginated_action_dto_list.append(item)
            continuation_token = paginated_action_dto.continuation_token

        if not paginated_action_dto_list:
            raise RuntimeError('Unable to find any run information. Please submit a new profile run.')

        run_list = []
        for item in paginated_action_dto_list:
            flag = True
            # This is done to ensure backward compatibility. Earlier we do not persist
            # run_id for local runs. Hence for older runs run_id is empty.
            if item.run_id is None:
                continue
            from azureml.core import Experiment, get_run
            experiment = Experiment(workspace, item.experiment_name)
            try:
                run = get_run(experiment, item.run_id)
            except Exception:
                flag = False
            if flag:
                run_list.append(run)

        return iter(run_list)

    def _time_filter(self, method, lower_bound=None, upper_bound=None, include_boundary=True):
        exception_message = 'Cannot perform time-series filter `{}` on dataset without timestamp columns defined.' \
                            '\nPlease use `with_timestamp_columns` to enable time-series capabilities'.format(method)

        from azureml.exceptions import DatasetTimestampMissingError
        if self._properties is None \
                or _DATASET_PROP_TIMESTAMP_FINE not in self._properties \
                or self._properties[_DATASET_PROP_TIMESTAMP_FINE] is None:
            raise DatasetTimestampMissingError(error_details=exception_message)

        col_fine_timestamp = self._properties[_DATASET_PROP_TIMESTAMP_FINE]
        col_coarse_timestamp = None
        if _DATASET_PROP_TIMESTAMP_COARSE in self._properties \
                and self._properties[_DATASET_PROP_TIMESTAMP_COARSE] is not None:
            col_coarse_timestamp = self._properties[_DATASET_PROP_TIMESTAMP_COARSE]

        # validate column type are datetime
        self._validate_timestamp_columns([col_fine_timestamp, col_coarse_timestamp])

        dataflow = self._dataflow

        # base filter, will enrich filters in following steps.
        from azureml.dataprep import Expression
        col_coarse_result = None

        # coarse timestamp may not be assigned.
        if col_coarse_timestamp:
            col_coarse_filters = Expression(dataflow[col_coarse_timestamp] is not None)
            if lower_bound:
                # Floor the lower boundary to the second
                lower_bound = lower_bound.replace(microsecond=0)
                filter_coarse_lower = dataflow[col_coarse_timestamp] >= lower_bound if include_boundary \
                    else dataflow[col_coarse_timestamp] > lower_bound
                col_coarse_filters &= filter_coarse_lower

            if upper_bound:
                # Strip milliseconds and microseconds from the timestamp
                microsecond = upper_bound.microsecond
                if microsecond > _HALF_SECOND:
                    # Round to nearest second
                    upper_bound = upper_bound + timedelta(seconds=1)
                upper_bound = upper_bound.replace(microsecond=0)
                filter_coarse_upper = dataflow[col_coarse_timestamp] <= upper_bound if include_boundary \
                    else dataflow[col_coarse_timestamp] < upper_bound
                col_coarse_filters &= filter_coarse_upper
            col_coarse_result = dataflow.filter(col_coarse_filters)

        col_fine_filters = Expression(dataflow[col_fine_timestamp] is not None)
        # fine timestamp is guaranteed to be there.
        if lower_bound:
            # Floor the lower boundary to the second
            lower_bound = lower_bound.replace(microsecond=0)
            filter_fine_lower = dataflow[col_fine_timestamp] >= lower_bound if include_boundary \
                else dataflow[col_fine_timestamp] > lower_bound
            col_fine_filters &= filter_fine_lower

        if upper_bound:
            # Strip milliseconds and microseconds from the timestamp
            microsecond = upper_bound.microsecond
            if microsecond > _HALF_SECOND:
                # Round to nearest second
                upper_bound = upper_bound + timedelta(seconds=1)
            upper_bound = upper_bound.replace(microsecond=0)
            filter_fine_upper = dataflow[col_fine_timestamp] <= upper_bound if include_boundary \
                else dataflow[col_fine_timestamp] < upper_bound
            col_fine_filters &= filter_fine_upper

        result = col_coarse_result.filter(col_fine_filters) if col_coarse_result else dataflow.filter(col_fine_filters)

        return TabularDataset._create(result, self._properties, telemetry_info=self._telemetry_info)

    def _validate_timestamp_columns(self, columns_list):
        FieldType = dataprep().api.engineapi.typedefinitions.FieldType
        columns = list(filter(lambda col: col is not None, columns_list))
        _validate_has_columns(self._dataflow, columns, [FieldType.DATE for c in columns])

    def _ensure_workspace(self, workspace):
        if workspace is not None:
            return workspace
        if self._registration is None or self._registration.workspace is None:
            raise RuntimeError(
                'The dataset does not belong to a workspace. Please pass in the workspace from argument.')
        return self._registration.workspace
