#!/usr/bin/python
# Copyright: (c) 2019, DellEMC

"""Ansible module for Gathering information about DellEMC Isilon"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_isilon_gatherfacts

version_added: '2.7'

short_description: Gathering information about DellEMC Isilon Storage

description:
- Gathering information about DellEMC Isilon Storage System includes
  Get attributes of the Isilon cluster,
  Get list of access zones in an Isilon cluster,
  Get list of nodes in an Isilon cluster,
  Get list of authentication providers for an access zone,
  Get list of users and groups for an access zone.

extends_documentation_fragment:
  - dellemc_isilon.dellemc_isilon

author:
- Ambuj Dubey (ambuj.dubey@dell.com)

options:
  access_zone:
    description:
    - The access zone. If no Access Zone is specified, the 'System' access
      zone would be taken by default.
    default: 'System'
    type: str
  gather_subset:
    description:
    - List of string variables to specify the Isilon Storage System entities
      for which information is required.
    - List of all Isilon Storage System entities supported by the module -
    - attributes
    - access_zones
    - nodes
    - providers
    - users
    - groups
    - The list of attributes, access_zones and nodes is for the entire Isilon
      cluster
    - The list of providers, users and groups is specific to the specified
      access zone
    required: True
    choices: [attributes, access_zones, nodes, providers, users, groups]
    type: list
  '''

EXAMPLES = r'''
  - name: Get attributes of the Isilon cluster
    dellemc_isilon_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{isilonport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - attributes

  - name: Get access_zones of the Isilon cluster
    dellemc_isilon_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{isilonport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - access_zones

  - name: Get nodes of the Isilon cluster
    dellemc_isilon_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{isilonport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - nodes

  - name: Get list of authentication providers for an access zone of the
          Isilon cluster
    dellemc_isilon_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{isilonport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - providers

  - name: Get list of users for an access zone of the Isilon cluster
    dellemc_isilon_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{isilonport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - users

  - name: Get list of groups for an access zone of the Isilon cluster
    dellemc_isilon_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{isilonport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - groups
'''

RETURN = r''' '''

import logging
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell \
    import dellemc_ansible_isilon_utils as utils
import re

LOG = utils.get_logger('dellemc_isilon_gatherfacts',
                       log_devel=logging.INFO)
HAS_ISILON_SDK = utils.has_isilon_sdk()
ISILON_SDK_VERSION_CHECK = utils.isilon_sdk_version_check()


class IsilonGatherFacts(object):
    """Class with Gather Fact operations"""

    def __init__(self):
        """Define all the parameters required by this module"""

        self.module_params = utils \
            .get_isilon_management_host_parameters()
        self.module_params.update(get_isilon_gatherfacts_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=False
                                    )

        if HAS_ISILON_SDK is False:
            self.module.fail_json(msg='Ansible modules for Isilon '
                                      'require the Isilon python library'
                                      ' to be installed. Please install'
                                      ' the library before using these '
                                      'modules.')

        if ISILON_SDK_VERSION_CHECK and \
                not ISILON_SDK_VERSION_CHECK['supported_version']:
            err_msg = ISILON_SDK_VERSION_CHECK['unsupported_version_message']
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

        self.api_client = utils.get_isilon_connection(self.module.params)
        self.isi_sdk = utils.get_isilon_sdk()
        LOG.info('Got python SDK instance for provisioning on Isilon ')

        self.cluster_api = self.isi_sdk.ClusterApi(self.api_client)
        self.zone_api = self.isi_sdk.ZonesApi(self.api_client)
        self.auth_api = self.isi_sdk.AuthApi(self.api_client)

    def get_attributes_list(self):
        """Get the list of attributes of a given Isilon Storage"""
        try:
            config = (self.cluster_api.get_cluster_config()).to_dict()
            ips = self.cluster_api.get_cluster_external_ips()
            external_ip_str = ','.join(ips)
            external_ips = {"External IPs": external_ip_str}
            logon_msg = (self.cluster_api.get_cluster_identity()).to_dict()
            contact_info = (self.cluster_api.get_cluster_owner()).to_dict()
            cluster_version = (self.cluster_api.get_cluster_version())\
                .to_dict()
            attribute = {"Config": config, "Contact_Info": contact_info,
                         "External_IP": external_ips,
                         "Logon_msg": logon_msg,
                         "Cluster_Version": cluster_version}
            LOG.info("Got Attributes of Isilon cluster %s",
                     self.module.params['onefs_host'])
            return attribute
        except Exception as e:
            error_msg = (
                'Get Attributes List for Isilon cluster: {0} failed'
                ' with error: {1}' .format(
                    self.module.params['onefs_host'],
                    self.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_access_zones_list(self):
        """Get the list of access_zones of a given Isilon Storage"""
        try:
            access_zones_list = (self.zone_api.list_zones()).to_dict()
            LOG.info("Got Access zones from Isilon cluster %s",
                     self.module.params['onefs_host'])
            return access_zones_list
        except Exception as e:
            error_msg = (
                'Get Access zone List for Isilon cluster: {0} failed'
                'with error: {1}' .format(
                    self.module.params['onefs_host'],
                    self.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_nodes_list(self):
        """Get the list of nodes of a given Isilon Storage"""
        try:
            nodes_list = (self.cluster_api.get_cluster_nodes()).to_dict()
            LOG.info('Got Nodes from Isilon cluster  %s',
                     self.module.params['onefs_host'])
            return nodes_list
        except Exception as e:
            error_msg = (
                'Get Nodes List for Isilon cluster: {0} failed with'
                'error: {1}' .format(
                    self.module.params['onefs_host'],
                    self.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_providers_list(self, access_zone):
        """Get the list of authentication providers for an access zone of a
        given Isilon Storage"""
        try:
            providers_list = (self.auth_api
                              .get_providers_summary(zone=access_zone))\
                .to_dict()
            LOG.info('Got authentication Providers from Isilon cluster %s',
                     self.module.params['onefs_host'])
            return providers_list
        except Exception as e:
            error_msg = (
                'Get authentication Providers List for Isilon'
                ' cluster: {0} and access zone: {1} failed with'
                ' error: {2}' .format(
                    self.module.params['onefs_host'],
                    access_zone,
                    self.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_users_list(self, access_zone):
        """Get the list of users for an access zone of a given Isilon
        Storage"""
        try:
            users_list = (self.auth_api.list_auth_users(zone=access_zone))\
                .to_dict()
            LOG.info('Got Users from Isilon cluster %s',
                     self.module.params['onefs_host'])
            return users_list
        except Exception as e:
            error_msg = (
                'Get Users List for Isilon cluster: {0} and access zone: {1} '
                'failed with error: {2}' .format(
                    self.module.params['onefs_host'],
                    access_zone,
                    self.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_groups_list(self, access_zone):
        """Get the list of groups for an access zone of a given Isilon
        Storage"""
        try:
            group_list = (
                self.auth_api.list_auth_groups(
                    zone=access_zone)).to_dict()
            LOG.info('Got Groups from Isilon cluster %s',
                     self.module.params['onefs_host'])
            return group_list
        except Exception as e:
            error_msg = ('Get Group List for Isilon cluster: {0} and'
                         'access zone: {1} failed with error: {2}'.format(
                             self.module.params['onefs_host'],
                             access_zone,
                             self.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def determine_error(self, error_obj):
        '''Format the error object'''
        if isinstance(error_obj, utils.ApiException):
            error = re.sub("[\n \"]+", ' ', str(error_obj.body))
        else:
            error = str(error_obj)
        return error

    def perform_module_operation(self):
        """Perform different actions on Gatherfacts based on user parameter
        chosen in playbook
        """
        access_zone = self.module.params['access_zone']
        subset = self.module.params['gather_subset']
        if not subset:
            self.module.fail_json(msg="Please specify gather_subset")

        attributes = []
        access_zones = []
        nodes = []
        providers = []
        users = []
        groups = []
        if 'attributes' in str(subset):
            attributes = self.get_attributes_list()
        if 'access_zones' in str(subset):
            access_zones = self.get_access_zones_list()
        if 'nodes' in str(subset):
            nodes = self.get_nodes_list()
        if 'providers' in str(subset):
            providers = self.get_providers_list(access_zone)
        if 'users' in str(subset):
            users = self.get_users_list(access_zone)
        if 'groups' in str(subset):
            groups = self.get_groups_list(access_zone)
        self.module.exit_json(
            Attributes=attributes,
            AccessZones=access_zones,
            Nodes=nodes,
            Providers=providers,
            Users=users,
            Groups=groups)


def get_isilon_gatherfacts_parameters():
    """This method provide parameter required for the ansible gatherfacts
        modules on Isilon"""
    return dict(
        access_zone=dict(required=False, type='str',
                         default='System'),
        gather_subset=dict(type='list', required=True,
                           choices=['attributes',
                                    'access_zones',
                                    'nodes',
                                    'providers',
                                    'users',
                                    'groups'
                                    ]),
    )


def main():
    """Create Isilon GatherFacts object and perform action on it
        based on user input from playbook"""
    obj = IsilonGatherFacts()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
