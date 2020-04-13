import sys

from ansible.module_utils import basic
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.openstack.tests.unit.plugins.module_utils.utils import AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args

from ansible_collections.community.openstack.plugins.module_utils.sdk import openstacksdk

class TestSDK(ModuleTestCase):

    def test_sdk_openstacksdk_module_absent(self):
        basic._load_params = lambda: {}
        module = AnsibleModule(argument_spec={})
        sys.modules['openstack'] = None
        with self.assertRaises(AnsibleFailJson):
            self.assertRaises(ImportError, openstacksdk, module)
