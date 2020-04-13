# Copyright (c) 2020 Fabien Dupont <fdupont@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import importlib
import os

from ansible.module_utils.basic import missing_required_lib

def openstacksdk(module):
    try:
        import importlib
        return importlib.import_module('openstack')
    except ImportError:
        module.fail_json(msg=missing_required_lib('openstack'))

