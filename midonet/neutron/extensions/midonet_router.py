# Copyright (C) 2014 Midokura SARL
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron.api import extensions
from neutron.api.v2 import attributes as attrs
from neutron.extensions import l3

EXTENDED_ATTRIBUTES_2_0 = {
    'routers': {
        'inbound_filter_id': {'allow_post': True, 'allow_put': True,
            'validate': {'type:uuid_or_none': None},
            'is_visible': True},
        'load_balancer_id': {'allow_post': True, 'allow_put': False,
            'validate': {'type:uuid_or_none': None},
            'is_visible': True},
        'outbound_filter_id': {'allow_post': True, 'allow_put': True,
            'validate': {'type:uuid_or_none': None},
            'is_visible': True},
    }
}


class Midonet_router(extensions.ExtensionDescriptor):

    @classmethod
    def get_name(cls):
        return "Midonet Router Extension"

    @classmethod
    def get_alias(cls):
        return "midonet-router"

    @classmethod
    def get_description(cls):
        return "Router abstraction for basic router-related features"

    @classmethod
    def get_namespace(cls):
        return "http://docs.openstack.org/ext/midonet-router/api/v1.0"

    @classmethod
    def get_updated(cls):
        return "2013-03-28T10:00:00-00:00"

    @classmethod
    def get_resources(cls):
        return []

    @classmethod
    def get_extended_resources(cls, version):
        if version == "2.0":
            return dict(EXTENDED_ATTRIBUTES_2_0.items())
        else:
            return {}
