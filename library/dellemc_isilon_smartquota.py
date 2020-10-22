#!/usr/bin/python
# Copyright: (c) 2020, DellEMC
""" Ansible module for managing Smart Quota on Isilon"""
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: dellemc_isilon_smartquota

version_added: '2.7'

short_description: Manage Smart Quotas on Isilon

description:
- Managing Smart Quotas on Isilon storage system includes getting details,
  modifying, creating and deleting Smart Quotas.

extends_documentation_fragment:
  - dellemc_isilon.dellemc_isilon

author:
- P Srinivas Rao (@srinivas-rao5) srinivas_rao5@dell.com

options:
  path:
    description:
    - The path on which the quota will be imposed.
    - For system access zone, the path is absolute. For all other access
      zones, the path is a relative path from the base of the access zone.
    type: str
    required: True
  quota_type:
    description:
    - The type of quota which will be imposed on path.
    type: str
    required: True
    choices: ['user', 'group', 'directory']
  user_name:
    description:
    - The name of the user account for which
      quota operations will be performed.
    type: str
  group_name:
    description:
    - The name of the group for which quota operations will be performed.
    type: str
  access_zone:
    description:
    - This option mentions the zone in which user/group exists.
    - For non system access zone, path relative to non system Access Zone's
      base directory has to be given.
    - For system access zone, absolute path has to be given.
    type: str
    default: 'system'
  provider_type:
    description:
    - This option defines the type which is used to
      authenticate the user/group.
    - If the provider_type is 'ads' then domain name of the Active
      Directory Server has to be mentioned in the user_name.
      The format for the user_name should be 'DOMAIN_NAME\user_name'
      or "DOMAIN_NAME\\user_name".
    - This option acts as a filter for all operations except creation.
    type: str
    default: 'local'
    choices: [ 'local', 'file', 'ldap', 'ads']
  quota:
    description:
    - Specifies Smart Quota parameters.
    type: dict
    suboptions:
      include_snapshots:
        description:
        - Whether to include the snapshots in the quota or not.
        type: bool
        default: False
      include_overheads:
        description:
        - Whether to include the data protection overheads
          in the quota or not.
        - If not passed during quota creation then quota will be created
          excluding the overheads.
        type: bool
      advisory_limit_size:
        description:
        - The threshold value after which the advisory notification
          will be sent.
        type: int
      soft_limit_size:
        description:
        - Threshold value after which soft limit exceeded notification
          will be sent and soft_grace period will start.
        - Write access will be restricted after grace period expires.
        - Both soft_grace_period and soft_limit_size are required to modify
          soft threshold for the quota.
        type: int
      soft_grace_period:
        description:
        - Grace Period after the soft limit for quota is exceeded.
        - After the grace period, the write access to the quota will be
          restricted.
        - Both soft_grace_period and soft_limit_size are required to modify
          soft threshold for the quota.
        type: int
      period_unit:
        description:
        - Unit of the time period for soft_grace_period.
        - For months the number of days is assumed to be 30 days.
        - This parameter is required only if the soft_grace_period,
          is specified.
        type: str
        choices: ['days', 'weeks', 'months']
      hard_limit_size:
        description:
        - Threshold value after which hard limit exceeded
          notification will be sent.
        - Write access will be restricted after hard limit is exceeded.
        type: int
      cap_unit:
        description:
        - Unit of storage for the hard, soft and advisory limits.
        - This parameter is required if any of the hard, soft or advisory
          limits is specified.
        type: str
        choices: ['GB', 'TB']
  state:
    description:
    - Define whether the Smart Quota should exist or not.
    - present - indicates that the Smart Quota should exist on the system.
    - absent - indicates that the Smart Quota should not exist on the system.
    choices: ['absent', 'present']
    type: str
    required: True

notes:
- To perform any operation, path, quota_type and state are
  mandatory parameters.
- There can be two quotas for each type per directory, one with snapshots
  included, and one without snapshots included.
- Once the limits are assigned then the quota can't be converted to
  accounting only modification to the threshold limits is permitted.
'''
EXAMPLES = r'''

  - name: Create a Quota for a User excluding snapshot.
    dellemc_isilon_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "{{path}}"
      quota_type: "user"
      user_name: "{{user_name}}"
      access_zone: "{{access_zone}}"
      provider_type: "{{provider_type}}"
      quota:
        include_overheads: False
        advisory_limit_size: "{{advisory_limit_size}}"
        soft_limit_size: "{{soft_limit_size}}"
        soft_grace_period: "{{soft_grace_period}}"
        period_unit: "{{period_unit}}"
        hard_limit_size: "{{hard_limit_size}}"
        cap_unit: "{{cap_unit}}"
      state: "present"

  - name: Create a Quota for a Directory for accounting includes snapshots and data protection overheads.
    dellemc_isilon_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "{{path}}"
      quota_type: "directory"
      provider_type: "{{provider_type}}"
      quota:
        include_snapshots: "True"
        include_overheads: "True"
      state: "present"

  - name: Get a Quota Details for a Group
    dellemc_isilon_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "{{path}}"
      quota_type: "group"
      group_name: "{{user_name}}"
      access_zone: "{{access_zone}}"
      provider_type: "{{provider_type}}"
      quota:
        include_snapshots: "True"
      state: "present"

  - name: Update Quota for a User
    dellemc_isilon_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "{{path}}"
      quota_type: "user"
      user_name: "{{user_name}}"
      access_zone: "{{access_zone}}"
      provider_type: "{{provider_type}}"
      quota:
        include_snapshots: "{{include_snapshots}}"
        include_overheads: "{{include_overheads}}"
        advisory_limit_size: "{{new_advisory_limit_size}}"
        hard_limit_size: "{{new_hard_limit_size}}"
        cap_unit: "{{cap_unit}}"
      state: "present"

  - name: Delete a Quota for a Directory
    dellemc_isilon_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "{{path}}"
      quota_type: "{{user_quota_type}}"
      quota:
        include_snapshots: "True"
      state: "absent"
'''
RETURN = r'''
changed:
    description: Whether or not the resource has changed
    returned: always
    type: bool
    sample: True

quota_details:
    description: The quota details.
    type: complex
    returned: When Quota exists.
    contains:
        id:
            description:
                - The ID of the Quota.
            type: str
            sample: "2nQKAAEAAAAAAAAAAAAAQIMCAAAAAAAA"
        enforced:
            description:
                - Whether the limits are enforced on Quota or not.
            type: bool
            sample: True
        thresholds:
            description:
                - Includes information about all the limits imposed on quota.
                - The limits are mentioned in bytes and soft_grace is in seconds.
            type: dict
            sample: {
                    "advisory": 3221225472,
                    "advisory(GB)": "3.0",
                    "advisory_exceeded": false,
                    "advisory_last_exceeded": 0,
                    "hard": 6442450944,
                    "hard(GB)": "6.0",
                    "hard_exceeded": false,
                    "hard_last_exceeded": 0,
                    "soft": 5368709120,
                    "soft(GB)": "5.0",
                    "soft_exceeded": false,
                    "soft_grace": 3024000,
                    "soft_last_exceeded": 0
                }
        type:
            description:
                - The type of Quota.
            type: str
            sample: "directory"
        usage:
            description:
                - The Quota usage.
            type: dict
            sample: {
                    "inodes": 1,
                    "logical": 0,
                    "physical": 2048
                }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell \
    import dellemc_ansible_isilon_utils as utils
import re

LOG = utils.get_logger('dellemc_isilon_smartquota',
                       log_devel=utils.logging.INFO)
HAS_ISILON_SDK = utils.has_isilon_sdk()
ISILON_SDK_VERSION_CHECK = utils.isilon_sdk_version_check()


class IsilonSmartQuota(object):
    """Class with Smart Quota operations"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.module_params = utils.get_isilon_management_host_parameters()
        self.module_params.update(get_isilon_smartquota_parameters())
        mut_ex_args = [['group_name', 'user_name']]
        req_if_args = [
            ['quota_type', 'user', ['user_name']],
            ['quota_type', 'group', ['group_name']]
        ]

        # initialize the ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=False,
                                    mutually_exclusive=mut_ex_args,
                                    required_if=req_if_args)

        # result is a dictionary that contains changed status and
        # smart quota details
        self.result = {"changed": False}
        if HAS_ISILON_SDK is False:
            self.module.fail_json(
                msg="Ansible modules for Isilon require the isilon "
                    "python library to be installed. Please install"
                    " the library  before using these modules.")

        if ISILON_SDK_VERSION_CHECK and \
                not ISILON_SDK_VERSION_CHECK['supported_version']:
            err_msg = ISILON_SDK_VERSION_CHECK['unsupported_version_message']
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

        self.api_client = utils.get_isilon_connection(self.module.params)
        self.auth_api_instance = utils.isi_sdk.AuthApi(self.api_client)
        self.zone_summary_api = utils.isi_sdk.ZonesSummaryApi(
            self.api_client)
        self.quota_api_instance = utils.isi_sdk.QuotaApi(self.api_client)

        LOG.info('Got the isi_sdk instance for Smart Quota Operations')

    def get_zone_base_path(self, access_zone):
        """
        Get the base path of the Access Zone.
        :param access_zone: Name of the Access Zone.
        :return: Base Path of the Access Zone.
        """
        try:
            zone_path = (self.zone_summary_api.
                         get_zones_summary_zone(access_zone)).to_dict()
            zone_base_path = zone_path['summary']['path']
            LOG.info("Successfully got zone_base_path for %s is %s",
                     access_zone, zone_base_path)
            return zone_base_path
        except Exception as e:
            error_message = 'Unable to fetch base path of Access Zone %s' \
                            ',failed with error: %s' \
                            % (access_zone, determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create(self, path, quota_type, zone,
               quota_dict, persona=None):
        """
        Create a Smart Quota.
        :param path: The path for which quota has to be created.
        :param quota_type: The type of the quota.
        :param zone: The zone in which user/group exists.
        :param quota_dict: Threshold limits dictionary containing all limits.
        :param persona: User/Group object.
        :return: Quota Id.
        """
        if quota_dict:
            threshold_obj = utils.isi_sdk.QuotaQuotaThresholds(
                quota_dict['advisory'], hard=quota_dict['hard'],
                soft=quota_dict['soft'],
                soft_grace=quota_dict['soft_grace'])
        else:
            threshold_obj = utils.isi_sdk.QuotaQuotaThresholds()

        enforced = False
        if quota_dict and (quota_dict['hard'] or quota_dict['soft']
                           or quota_dict['advisory']):
            enforced = True

        # if not passed during creation of Quota
        # Set include_overheads as False
        if quota_dict is None or quota_dict['include_overheads'] is None:
            include_overhead = False
        else:
            include_overhead = quota_dict['include_overheads']
        if quota_dict is None or quota_dict['include_snapshots'] is None:
            include_snapshots = False
        else:
            include_snapshots = quota_dict['include_snapshots']

        quota_params_obj = utils.isi_sdk.QuotaQuotaCreateParams(
            include_snapshots=include_snapshots, path=path,
            enforced=enforced,
            persona=persona,
            thresholds_include_overhead=include_overhead,
            thresholds=threshold_obj, type=quota_type)
        try:
            api_response = self.quota_api_instance.create_quota_quota(
                quota_quota=quota_params_obj, zone=zone)
            message = "Quota created, %s" % api_response
            LOG.info(message)
            return api_response
        except utils.ApiException as e:
            error_message = "Create quota for %s failed with %s" \
                            % (path, determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def update(self, quota_dict, quota_id, enforced, path):
        """
        Update the attributes for a Smart Quota.
        :param quota_dict: Threshold limits dictionary containing all limits.
        :param quota_id: Id of the quota.
        :param enforced: Boolean value whether to enforce limits or not.
        :param path: The path for which quota has to be updated.
        :return: True if the operation is successful.
        """
        threshold_obj = utils.isi_sdk.QuotaQuotaThresholds(
            advisory=quota_dict['advisory'], hard=quota_dict['hard'],
            soft=quota_dict['soft'], soft_grace=quota_dict['soft_grace'])
        quota_params_obj = utils.isi_sdk.QuotaQuota(
            enforced=enforced,
            thresholds_include_overhead=quota_dict['include_overheads'],
            thresholds=threshold_obj)
        try:
            self.quota_api_instance.update_quota_quota(
                quota_quota=quota_params_obj, quota_quota_id=quota_id)
            msg = "Quota Updated successfully for path %s" % path
            LOG.info(msg)
            return True
        except utils.ApiException as e:
            error_message = "Update quota for path %s failed with %s" \
                            % (path, determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_sid(self, name, type, provider, zone):
        """
        Get the User/Group Account's SID in Isilon.
        :param name: Name of the resource.
        :param type: Whether resource is of User or Group.
        :param provider: Authentication type for the resource.
        :param zone: Access Zone in which resource exists.
        :return: sid of the resource.
        """
        try:
            if type == 'user':
                api_response = self.auth_api_instance.get_auth_user(
                    auth_user_id='USER:' + name,
                    zone=zone, provider=provider)
                msg = "SID of the user: %s" % api_response.users[0].sid.id
                LOG.info(msg)
                return api_response.users[0].sid.id

            elif type == 'group':
                api_response = self.auth_api_instance.get_auth_group(
                    auth_group_id='GROUP:' + name, zone=zone,
                    provider=provider)
                msg = "SID of the group: %s" % api_response.groups[0].sid.id
                LOG.info(msg)
                return api_response.groups[0].sid.id

        except Exception as e:
            error_message = "Failed to get {0} details for " \
                            "AccessZone:{1} and Provider:{2} " \
                            "with error {3}" \
                .format(name, zone, provider, determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_quota_details(self, include_snapshots,
                          zone, type, path, persona=None):
        """
         Get the details of the Smart Quota.
        :param include_snapshots: Whether to include snapshots or not.
        :param zone: Access Zone in which User/Group/Quota exists.
        :param type: The type of the quota.
        :param path: The path for which quota exists.
        :param persona: User/Group object.
        :return: if exists returns details of the Quota and Quota's Id,
         else returns None.
        """
        try:
            if type == 'directory':
                api_response = self.quota_api_instance.list_quota_quotas(
                    include_snapshots=include_snapshots, zone=zone,
                    type=type, path=path)
            else:
                api_response = self.quota_api_instance.list_quota_quotas(
                    include_snapshots=include_snapshots, zone=zone,
                    persona=persona, type=type, path=path)
            if api_response.quotas:
                quota_id = api_response.quotas[0].id
                quota = api_response.quotas[0].to_dict()
                msg = "Get Quota Details Successful. Quota Details: %s"\
                      % quota
                LOG.info(msg)
                return quota, quota_id
            LOG.info("Get Quota Details Failed. Quota does not exist.")
            return None, None
        except Exception as e:
            error_message = "Get Quota Details for %s failed with %s" \
                            % (path, determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete(self, quota_id, path):
        """
        Delete the Smart Quota.
        :param quota_id: The Id of the Quota.
        :param path: The path for which quota exists.
        :return: True, if the delete operation is successful.
        """
        try:
            self.quota_api_instance.delete_quota_quota(quota_id)
            msg = "Quota Deleted Successfully for Path %s" % path
            LOG.info(msg)
            return True
        except Exception as e:
            error_message = "Delete quota for %s failed with %s" \
                            % (path, determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def convert_quota_thresholds(self, quota):
        """
        Convert the threshold limits to appropriate units.
        :param quota: Threshold limits dictionary containing all limits.
        :return: Converted Threshold limits dictionary.
        """
        limit_params = ['advisory_limit_size', 'soft_limit_size',
                        'hard_limit_size', 'soft_grace_period']
        for limit in quota.keys():
            if limit in limit_params:
                if quota[limit] is not None and quota[limit] <= 0:
                    self.module.fail_json(
                        msg="Invalid %s provided, must be greater than 0"
                            % limit)
                if limit == 'soft_grace_period':
                    if quota[limit] is not None and quota[limit] > 0:
                        quota[limit] = period_to_seconds(
                            quota[limit], quota['period_unit'])
                elif quota[limit] is not None and quota[limit] > 0:
                    quota[limit] = utils.get_size_bytes(
                        quota[limit], quota['cap_unit'])
        quota['advisory'] = quota.pop('advisory_limit_size')
        quota['soft'] = quota.pop('soft_limit_size')
        quota['hard'] = quota.pop('hard_limit_size')
        quota['soft_grace'] = quota.pop('soft_grace_period')
        return quota

    def perform_module_operation(self):
        """
        Perform different actions on Smart Quota module based on parameters
        chosen in playbook
        """
        quota_type = self.module.params['quota_type']
        user_name = self.module.params['user_name']
        group_name = self.module.params['group_name']

        access_zone = self.module.params['access_zone']
        if access_zone == "" or access_zone.isspace():
            self.module.fail_json(msg="Invalid Access_zone provided,"
                                      " Please a provide valid Access_zone")

        provider_type = self.module.params['provider_type']
        state = self.module.params['state']

        quota = self.module.params['quota']
        if quota:
            self.convert_quota_thresholds(quota)
            include_snapshots = quota.get('include_snapshots')
        else:
            include_snapshots = False
        message = "Quota Dictionary after conversion:  %s" % str(quota)
        LOG.debug(message)

        path = self.module.params['path']
        if path == "" or path.isspace():
            self.module.fail_json(msg="Invalid path provided,"
                                      " Please a provide valid path")
        # If Access_Zone is System then absolute path is required
        # else relative path is taken
        if access_zone.lower() == "system":
            complete_path = path
        else:
            complete_path = self.get_zone_base_path(access_zone) + path

        changed = False
        # Get the sid(security identifier) for User
        sid = None
        if quota_type == "user":
            sid = self.get_sid(user_name, quota_type,
                               provider_type, access_zone)
        # Get the sid(security identifier) for Group
        if quota_type == "group":
            sid = self.get_sid(group_name, quota_type,
                               provider_type, access_zone)

        # Throw error if quota_type is directory
        # and parameters for user and group are provided
        if quota_type == 'directory':
            provider_type = None
            if user_name or group_name or provider_type:
                self.module.fail_json(
                    msg="quota_type is directory given,"
                        " user_name/group_name/provider_type not required.")

        # Throw error if limits and cap_unit are not passed together
        if quota and (quota['advisory'] or quota['soft'] or quota['hard']) \
                and not quota['cap_unit']:
            self.module.fail_json(msg="advisory/soft/hard limit provided,"
                                      " cap_unit not provided")
        if quota and quota['cap_unit'] \
                and not(quota['advisory'] or quota['soft'] or quota['hard']):
            self.module.fail_json(
                msg="cap_unit provided,"
                    " advisory/soft/hard limit not provided")

        # Get the details of the Quota
        quota_details, quota_id = self.get_quota_details(
            include_snapshots, access_zone, quota_type, complete_path, sid)

        # Create a Quota
        if state == "present" and not quota_details:
            LOG.info("Create a Quota")
            persona_obj = None
            if quota_type != "directory":
                persona_obj = \
                    utils.isi_sdk.AuthAccessAccessItemFileGroup(id=sid)
            self.create(complete_path, quota_type, access_zone, quota,
                        persona_obj)
            changed = True

        # Update a Quota
        if state == "present" and quota_details and quota:
            modify_flag = False
            if quota:
                modify_flag = to_modify_quota(
                    quota, quota_details["thresholds"],
                    quota_details["thresholds_include_overhead"])
            enforce_limit = False
            if quota_details["enforced"] or quota['advisory'] or \
                    quota['hard'] or quota['soft']:
                enforce_limit = True
            if modify_flag:
                LOG.info("Updating the Quota")
                changed = self.update(quota, quota_id, enforce_limit, path)

        # Delete Quota
        if state == "absent" and quota_details:
            LOG.info("Delete Quota")
            changed = self.delete(quota_id, complete_path)

        quota_details, quota_id = self.get_quota_details(
            include_snapshots, access_zone, quota_type, complete_path, sid)
        if quota_type != "directory" and quota_details:
            quota_details['persona']['type'] = quota_type
            quota_details['persona']['name'] = \
                user_name if user_name else group_name
        quota_details = add_limits_with_unit(quota_details)
        self.result["changed"] = changed
        self.result["quota_details"] = quota_details
        self.module.exit_json(**self.result)


def add_limits_with_unit(quota_details):
    """
    Adds limits to the quota details with units.
    :param quota_details: details of the Quota
    :return: updated quota details if quota details exists else None
    """
    if quota_details is None:
        return None
    limit_list = ['hard', 'soft', 'advisory']
    for limit in limit_list:
        if quota_details['thresholds'][limit]:
            size_with_unit = utils.convert_size_with_unit(
                quota_details['thresholds'][limit]).split(" ")
            new_limit = limit + "("+size_with_unit[1]+")"
            quota_details['thresholds'][new_limit] = size_with_unit[0]
    return quota_details


def to_modify_quota(input_quota, array_quota, array_include_overhead):
    """

    :param input_quota: Threshold limits dictionary passed by the user.
    :param array_quota: Threshold limits dictionary got from the Isilon Array
    :param array_include_overhead: Whether Quota Include Overheads or not.
    :return: True if the quota is to be modified else returns False.
    """
    if input_quota['include_overheads'] is not None \
            and input_quota['include_overheads'] != array_include_overhead:
        return True
    for limit in input_quota:
        if limit in array_quota and input_quota[limit] is not None and\
                input_quota[limit] != array_quota[limit]:
            return True
    return False


def determine_error(error_obj):
    """Determine the error message to return"""
    if isinstance(error_obj, utils.ApiException):
        error = re.sub("[\n \"]+", ' ', str(error_obj.body))
    else:
        error = str(error_obj)
    return error


def period_to_seconds(period, period_unit):
    """ Convert the given period to seconds"""
    if period_unit == 'days':
        return period * 86400
    if period_unit == 'weeks':
        return period * 7 * 86400
    if period_unit == 'months':
        return period * 30 * 86400


def make_threshold_obj(advisory, soft, soft_grace, hard):
    """Make threshold object for quota"""
    thresholds = utils.isi_sdk.QuotaQuotaThresholds(
        advisory=advisory, hard=hard, soft=soft, soft_grace=soft_grace)
    return thresholds


def get_isilon_smartquota_parameters():
    """This method provides parameters required for the ansible Smart Quota
    module on Isilon"""
    return dict(
        path=dict(required=True, type='str'),
        user_name=dict(type='str'),
        group_name=dict(type='str'),
        access_zone=dict(type='str', default='system'),
        provider_type=dict(type='str', default='local',
                           choices=['local', 'file', 'ldap', 'ads']),
        quota_type=dict(required=True, type='str',
                        choices=['user', 'group', 'directory']),
        quota=dict(
            type='dict', options=dict(
                include_snapshots=dict(type='bool', default=False),
                include_overheads=dict(type='bool'),
                advisory_limit_size=dict(type='int'),
                soft_limit_size=dict(type='int'),
                hard_limit_size=dict(type='int'),
                soft_grace_period=dict(type='int'),
                period_unit=dict(type='str',
                                 choices=['days', 'weeks', 'months']),
                cap_unit=dict(type='str', choices=['GB', 'TB'])
            ),
            required_together=[
                ['soft_grace_period', 'period_unit'],
                ['soft_grace_period', 'soft_limit_size']
            ]
        ),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create Isilon Smart Quota object and perform actions on it
        based on user input from playbook"""
    obj = IsilonSmartQuota()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
