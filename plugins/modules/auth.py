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
module: community.openstack.auth
short_description: Module to manage OpenStack authentication
version_added: "2.9"
author: "Fabien Dupont <fdupont@redhat.com>"
description: This module allows to connect to OpenStack API

options:
"""

EXAMPLES = """

"""

RETURN = """
auth_token:
    description: OpenStack API authentication token
    returned: success
    type: str
service_catalog:
    description: A dictionary of available API endpoints
    returned: success
    type: dict
"""

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.openstack.module_utils.sdk import openstacksdk

def run_module():
    argument_spec = {
        'access_token_endpoint': {
            'description': ('OpenID Connect Provider Token Endpoint. Note that'
                            'if a discovery document is being passed this'
                            'option will override the endpoint provided by the'
                            'server in the discovery document.'),
        },
        'access_token_type': {
            'description': ('OAuth 2.0 Authorization Server Introspection'
                            'token type, it is used to decide which type of'
                            'token will be used when processing token'
                            'introspection.'),
            'choices': ['access_token', 'id_token']
        },
        'api_timeout': {
            'description': ('How long should the socket layer wait before'
                            'timing out for API calls.'),
            'type': 'int',
        },
        'auth_type': {
            'description': 'Authentication type',
            'choices': [
                'cloud-config', 'v3oidcpassword', 'v3password', 'v3token', 'v3tokenlessauth', 'v3totp'
            ],
            'default': 'cloud-config',
        },
        'auth_url': {
            'description': 'Authentication URL',
        },
        'ca_cert_file': {
            'description': ('A path to a CA Cert bundle that can be used as'
                            'part of verifying SSL API requests.'),
        },
        'client_id': {
            'description': 'OAuth 2.0 Client ID',
        },
        'client_secret': {
            'OAuth 2.0 Client Secret',
        },
        'cloud': {
            'description': 'Cloud config name',
        },
        'discovery_endpoint': {
            'description': ('OpenID Connect Discovery Document URL. The'
                            'discovery document will be used to obtain the'
                            'values of the access token endpoint and the'
                            'authentication endpoint. This URL should look'
                            'like https://idp.example.org/.well-known/openid-configuration'),
        },
        'domain_id': {
            'description': 'Domain ID to scope to',
        },
        'domain_name': {
            'description': 'Domain name to scope to',
        },
        'identity_interface': {
            'description': 'Identity service interface',
            'choices': ['public', 'internal', 'admin'],
            'default': 'public'
        },
        'identify_provider': {
            'description': 'Identity provider\'s name',
        },
        'identity_provider_url': {
            'description': ('An Identity Provider URL, where the SAML2'
                            'authentication request will be sent.'),
        },
        'openid_scope': {
            'description': ('OpenID Connect scope that is requested from'
                            'authorization server. Note that the OpenID'
                            'Connect specification states that \'openid\' must'
                            'be always specified.'),
        },
        'passcode': {
            'description': 'User`s TOTP passcode',
        },
        'password': {
            'description': 'Password',
        },
        'project_id': {
            'description': 'Project ID to scope to',
        },
        'project_name': {
            'description': 'Project name to scope to',
        },
        'project_domain_id': {
            'description': 'Domain ID containing project',
        },
        'project_domain_name': {
            'description': 'Domain name containing project',
        },
        'protocol': {
            'description': 'Protocol for federated plugin',
        },
        'region_name': {
            'description': 'Region name',
            'required': True,
        },
        'system_scope': {
            'description': 'Scope for system operations',
        },
        'token_id': {
            'description': 'Token to authenticate with',
        },
        'trust_id': {
            'description': 'Trust ID',
        },
        'user_id': {
            'description': 'User ID',
        },
        'username': {
            'description': 'Username',
        },
        'user_domain_id': {
            'description': 'Domain ID containing user',
        },
        'user_domain_name': {
            'description': 'Domain name containing user',
        },
        'validate_certs': {
            'description': ('Whether or not SSL API requests should be'
                            'verified.'),
            'type': 'bool',
            'default': False
        },
        'x509_key_file': {
            'description': ('A path to a client key to use as part of the SSL'
                            'token less authentication.',
        },
    }        

    required_if = [
        ['auth_type', 'cloud-config', ['cloud']],

        ['auth_type', 'v3applicationcredential', ['application_credential_secret', 'auth_url']],
        ['auth_type', 'v3applicationcredential', ['domain_id', 'domain_name'], True],
        ['auth_type', 'v3applicationcredential', ['project_domain_id', 'project_domain_name'], True],
        ['auth_type', 'v3applicationcredential', ['project_id', 'project_name'], True],
        ['auth_type', 'v3applicationcredential', ['user_domain_id', 'user_domain_name'], True],
        ['auth_type', 'v3applicationcredential', ['user_id', 'username'], True],
        ['auth_type', 'v3applicationcredential', ['application_credential_id', 'application_credential_name'], True],

        ['auth_type', 'v3oidcpassword', ['auth_url', 'access_token_endpoint', 'access_token_type', 'client_id', 'client_secret', 'discovery_endpoint', 'identity_provider', 'openid_scope', 'password', 'protocol', 'username']],
        ['auth_type', 'v3oidcpassword', ['domain_id', 'domain_name'], True],
        ['auth_type', 'v3oidcpassword', ['project_domain_id', 'project_domain_name'], True],
        ['auth_type', 'v3oidcpassword', ['project_id', 'project_name'], True],

        ['auth_type', 'v3samlpassword', ['auth_url', 'identity_provider', 'identity_provider_url', 'username', 'password']],
        ['auth_type', 'v3samlpassword', ['domain_id', 'domain_name'], True],
        ['auth_type', 'v3samlpassword', ['project_domain_id', 'project_domain_name'], True],
        ['auth_type', 'v3samlpassword', ['project_id', 'project_name'], True],

        ['auth_type', 'v3password', ['auth_url', 'password']],
        ['auth_type', 'v3password', ['domain_id', 'domain_name'], True],
        ['auth_type', 'v3password', ['project_domain_id', 'project_domain_name'], True],
        ['auth_type', 'v3password', ['project_id', 'project_name'], True],
        ['auth_type', 'v3password', ['user_domain_id', 'user_domain_name'], True],
        ['auth_type', 'v3password', ['user_id', 'username'], True],

        ['auth_type', 'v3token', ['auth_url', 'token']],
        ['auth_type', 'v3token', ['domain_id', 'domain_name'], True],
        ['auth_type', 'v3token', ['project_domain_id', 'project_domain_name'], True],
        ['auth_type', 'v3token', ['project_id', 'project_name'], True],

        ['authtype', 'v3tokenlessauth', ['auth_url', 'x509_key_file']],
        ['authtype', 'v3tokenlessauth', ['domain_id', 'domain_name'], True],
        ['authtype', 'v3tokenlessauth', ['project_domain_id', 'project_domain_name'], True],
        ['authtype', 'v3tokenlessauth', ['project_id', 'project_name'], True],

        ['authtype', 'v3totp', ['auth_url', 'passcode']],
        ['authtype', 'v3totp', ['domain_id', 'domain_name'], True],
        ['authtype', 'v3totp', ['project_domain_id', 'project_domain_name'], True],
        ['authtype', 'v3totp', ['project_id', 'project_name'], True],
        ['authtype', 'v3totp', ['user_domain_id', 'user_domain_name'], True],
        ['authtype', 'v3totp', ['user_id', 'username'], True],
    ]

    optional_if = [
        ['auth_type', 'v3applicationcredential', ['system_scope', 'trust_id']],
        ['auth_type', 'v3password', ['system_scope', 'trust_id']],
        ['auth_type', 'v3samlpassword', ['system_scope', 'trust_id']],
        ['auth_type', 'v3token', ['system_scope', 'trust_id']],
        ['auth_type', 'v3totp', ['system_scope', 'trust_id']],
    ]

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=required_if,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    # Create the connection args with standard args
    connect_args = {
        'interface': module.params['interface'],
        'region_name': module.params['region_name'],
        'verify': module.params['validate_certs'],
    }
    if 'api_timeout' in module.params:
        connect_args['api_timeout']: module.params['api_timeout']
    if 'validate_certs' in module.params:
        if 'ca_cert_file' in module.params:
            connect_args['cacert']: module.params['ca_cert_file']

    # Build the authentication args
    auth = {}
    if module.params['auth_type'] != 'cloud-config':
        auth['auth_type'] = module.params['auth_type']
    for req in required_if:
        next if req[1] != module.params['auth_type']
        for key in req[2]:
            if key in module.params:
                auth[key] = modules.params[key]

    # Load 
    sdk = import_openstacksdk(module)

    try:
        conn = sdk.connect(connect_args, **auth)
    except sdk.exceptions.SDKException as e:
        module.fail_json(msg=str(e))

    try:
        module.exit_json(
            changed=False,
            ansible_facts=dict(
                auth_token=conn.auth_token,
                service_catalog=conn.service_catalog
            )
        )
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())

def main():
    run_module()

if __name__ == '__main__':
    main()
