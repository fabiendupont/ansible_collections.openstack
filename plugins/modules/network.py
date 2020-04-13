#!/usr/bin/env python

# Copyright: (c) 2020, Fabien Dupont <fdupont@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community"
}

DOCUMENTATION = """
---
module: community.openstack.network
short_description: Module to manage OpenStack network
version_added: "2.10"
author: "Fabien Dupont <fdupont@redhat.com>"
description:
    - "This module allows managing network in OpenStack"
    - "Exposes the features of https://docs.openstack.org/api-ref/network/v2/index.html"

options:
    auth_token: 
"""

EXAMPLES = """

"""

RETURN = """
network:
    description: Dictionary describing the network.
    returned: On success when I(state) is 'present'.
    type: complex
    contains:
        id:
            description: Network ID.

"""

from ansible.module_utils.basic import AnsibleModule
from ansible.community.openstack.module_utils import openstack_argument_spec, openstack_cloud_from_module

def run_module():
    module_args = dict(
        auth_token=dict(type='str', required=False),
        
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mod:
        module.exit_json(**result)

    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'


def main():
    run_module()

if __name__ == '__main__':
    main()
