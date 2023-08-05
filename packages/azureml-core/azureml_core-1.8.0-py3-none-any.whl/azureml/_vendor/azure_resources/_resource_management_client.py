# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.service_client import SDKClient
from msrest import Serializer, Deserializer

from ._configuration import ResourceManagementClientConfiguration
from .operations import Operations
from .operations import DeploymentsOperations
from .operations import ProvidersOperations
from .operations import ResourcesOperations
from .operations import ResourceGroupsOperations
from .operations import TagsOperations
from .operations import DeploymentOperations
from . import models


class ResourceManagementClient(SDKClient):
    """Provides operations for working with resources and resource groups.

    :ivar config: Configuration for client.
    :vartype config: ResourceManagementClientConfiguration

    :ivar operations: Operations operations
    :vartype operations: azure.mgmt.resource.resources.v2019_10_01.operations.Operations
    :ivar deployments: Deployments operations
    :vartype deployments: azure.mgmt.resource.resources.v2019_10_01.operations.DeploymentsOperations
    :ivar providers: Providers operations
    :vartype providers: azure.mgmt.resource.resources.v2019_10_01.operations.ProvidersOperations
    :ivar resources: Resources operations
    :vartype resources: azure.mgmt.resource.resources.v2019_10_01.operations.ResourcesOperations
    :ivar resource_groups: ResourceGroups operations
    :vartype resource_groups: azure.mgmt.resource.resources.v2019_10_01.operations.ResourceGroupsOperations
    :ivar tags: Tags operations
    :vartype tags: azure.mgmt.resource.resources.v2019_10_01.operations.TagsOperations
    :ivar deployment_operations: DeploymentOperations operations
    :vartype deployment_operations: azure.mgmt.resource.resources.v2019_10_01.operations.DeploymentOperations

    :param credentials: Credentials needed for the client to connect to Azure.
    :type credentials: :mod:`A msrestazure Credentials
     object<msrestazure.azure_active_directory>`
    :param subscription_id: The ID of the target subscription.
    :type subscription_id: str
    :param str base_url: Service URL
    """

    def __init__(
            self, credentials, subscription_id, base_url=None):

        self.config = ResourceManagementClientConfiguration(credentials, subscription_id, base_url)
        super(ResourceManagementClient, self).__init__(self.config.credentials, self.config)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self.api_version = '2019-10-01'
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.operations = Operations(
            self._client, self.config, self._serialize, self._deserialize)
        self.deployments = DeploymentsOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.providers = ProvidersOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.resources = ResourcesOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.resource_groups = ResourceGroupsOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.tags = TagsOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.deployment_operations = DeploymentOperations(
            self._client, self.config, self._serialize, self._deserialize)
