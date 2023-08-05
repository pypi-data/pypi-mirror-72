# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains Azure Machine Learning exception classes."""
from ._azureml_exception import TrainingException
from ._azureml_exception import SnapshotException
from ._azureml_exception import ExperimentExecutionException
from ._azureml_exception import ProjectSystemException
from ._azureml_exception import RunEnvironmentException
from ._azureml_exception import WorkspaceException
from ._azureml_exception import ComputeTargetException
from ._azureml_exception import RunConfigurationException
from ._azureml_exception import WebserviceException
from ._azureml_exception import ModelNotFoundException
from ._azureml_exception import ModelPathNotFoundException
from ._azureml_exception import DiscoveryUrlNotFoundException
from ._azureml_exception import ActivityFailedException
from ._azureml_exception import AuthenticationException
from ._azureml_exception import UserErrorException
from ._azureml_exception import DatasetTimestampMissingError
from azureml._restclient.exceptions import ServiceException
from azureml._common.exceptions import AzureMLException
from azureml._base_sdk_common import __version__ as VERSION

__version__ = VERSION

__all__ = [
    "ActivityFailedException",
    "AuthenticationException",
    "AzureMLException",
    "ComputeTargetException",
    "DatasetTimestampMissingError",
    "DiscoveryUrlNotFoundException",
    "ExperimentExecutionException",
    "ModelNotFoundException",
    "ModelPathNotFoundException",
    "ProjectSystemException",
    "RunConfigurationException",
    "RunEnvironmentException",
    "ServiceException",
    "SnapshotException",
    "TrainingException",
    "UserErrorException",
    "WebserviceException",
    "WorkspaceException"
]
