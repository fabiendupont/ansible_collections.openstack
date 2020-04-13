# OpenStack Collection for Ansible

<img src="https://img.shields.io/badge/Python-v3.6+-blue.svg">
<img src="https://img.shields.io/badge/Ansible-v2.9-blue.svg">
<img src="https://img.shields.io/badge/License-GPL-v3.0-blue.svg">
[![CI](https://github.com/ansible-collections/openstack/workflows/CI/badge.svg?event=push)](https://github.com/ansible-collections/openstack/actions)
[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/openstack)](https://codecov.io/gh/ansible-collections/openstack)

This repository hosts the `community.openstack` Ansible Collection.

The collection includes a variety of Ansible content to help automate the management of resources in OpenStack.

## Included content


## Installation and usage

### Installing the collection from Ansible Galaxy

Before using the OpenStack collection, you need to install it with the Ansible Galaxy CLI:

```
$ ansible-galaxy collection install community.openstack
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy colection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: community.openstack
    version: 0.1.0
```

### Installing the OpenStack Python SDK

Content in this collection requires the [OpenStack Python SDK]() to interact with OpenStack's APIs. You can install with:

```
$ pip3 install openstacksdk
```

### Using modules from OpenStack Collection in your playbooks

You can either call modules byt their Fully Qualified Collection Namespace (FQCN), like `community.openstack.network_create`, or you can call modules by their short name if you list the `community.openstack` collection in the playbook's `collections`, like so:

```yaml
---
- hosts: localhost
  gather_facts: false
  connection: local

  collections:
    - community.openstack

  tasks:
    - name: Authenticate against OpenStack
      auth_login:
        [...]
      register: openstack_auth

    - name: Read the network object
      network_read:
        auth: "{{ openstack_auth }}"
        id: "01234567-89ab-cdef-0123-456789ab-cdef"
      register: network_object

    - name: Delete authentication
      auth_logout:
        id: "{{ openstack_auth.id }}"
```
