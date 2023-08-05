# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 2.3.33.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GlusterFs(Model):
    """GlusterFs.

    :param server_address: The server address of one of the servers that hosts
     the GlusterFS. Can be either the IP address
     or server name.
    :type server_address: str
    :param volume_name: The name of the created GlusterFS volume.
    :type volume_name: str
    """

    _attribute_map = {
        'server_address': {'key': 'serverAddress', 'type': 'str'},
        'volume_name': {'key': 'volumeName', 'type': 'str'},
    }

    def __init__(self, server_address=None, volume_name=None):
        super(GlusterFs, self).__init__()
        self.server_address = server_address
        self.volume_name = volume_name
