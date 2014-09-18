# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

from midonet.neutron.extensions import midonet_router
from neutron.extensions import l3
from neutron.db import db_base_plugin_v2 as base_db
from neutron.openstack.common import importutils
from neutron.openstack.common import uuidutils
from neutron.tests.unit import test_db_plugin
from neutron.tests.unit import test_l3_plugin as test_l3
from oslo.config import cfg
from webob import exc

_uuid = uuidutils.generate_uuid

MIDOKURA_EXT_PATH = "midonet.neutron.extensions"
NEUTRON_EXT_PATH = "neutron.extensions"

class MidonetRouterTestExtensionManager(object):

    def get_resources(self):
        l3.RESOURCE_ATTRIBUTE_MAP['routers'].update(
            midonet_router.EXTENDED_ATTRIBUTES_2_0['routers'])
        return l3.L3.get_resources()

    def get_actions(self):
        return []

    def get_request_extensions(self):
        return []


class MidonetRouterTestPlugin(base_db.NeutronDbPluginV2):

    supported_extension_aliases = ['midonet-router', 'router']


class MidonetRouterExtTestCase(object):

    fmt = 'json'

    def setUp(self):
        mido_extensions_path = importutils.import_module(MIDOKURA_EXT_PATH).__file__
        neutron_extensions_path = importutils.import_module(NEUTRON_EXT_PATH).__file__
        cfg.CONF.set_override('api_extensions_path',
                              os.path.dirname(mido_extensions_path) + ":" + os.path.dirname(neutron_extensions_path))
        plugin = (__name__ + '.MidonetRouterTestPlugin')
        ext_mgr = MidonetRouterTestExtensionManager()
        super(MidonetRouterExtTestCase, self).setUp(plugin=plugin, ext_mgr=ext_mgr)

    def test_inbound_is_uuid(self):
        """Test if new attributes for router are exposed.
        """
        data = {'router': {'name': 'router1',
                           'admin_state_up': True,
                           'tenant_id': _uuid(),
                           'inbound_filter_id': 'foo'}}
        req = self.new_create_request('routers', data, fmt=self.fmt)
        res = req.get_response(self.api)

        self.assertEqual(exc.HTTPBadRequest.code, res.status_int)
        body = self.deserialize(self.fmt, res)
        self.assertIn('NeutronError', body)
        message = body['NeutronError']['message']
        self.assertIn("'foo' is not a valid UUID", message)
