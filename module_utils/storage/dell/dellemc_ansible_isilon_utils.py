""" import isilon sdk"""
try:
    import isi_sdk_8_1_1 as isi_sdk
    from isi_sdk_8_1_1.rest import ApiException

    HAS_ISILON_SDK = True

except ImportError:
    HAS_ISILON_SDK = False


'''import pkg_resources'''
try:
    from pkg_resources import parse_version
    import pkg_resources
    PKG_RSRC_IMPORTED = True
except ImportError:
    PKG_RSRC_IMPORTED = False


import logging
import math
import urllib3
urllib3.disable_warnings()
from decimal import Decimal


''' Check and Get required libraries '''


def has_isilon_sdk():
    return HAS_ISILON_SDK


def get_isilon_sdk():
    return isi_sdk


'''
Check if required Isilon SDK version is installed
'''


def isilon_sdk_version_check():
    try:
        supported_version = False
        if not PKG_RSRC_IMPORTED:
            unsupported_version_message = "Unable to import " \
                                          "'pkg_resources', please install" \
                                          " the required package"
        else:
            min_ver = '0.2.7'
            curr_version = pkg_resources.require("isi-sdk-8-1-1")[0].version
            unsupported_version_message =\
                "isilon sdk {0} is not supported by this module. Minimum " \
                "supported version is : {1} ".format(curr_version, min_ver)
            supported_version = parse_version(curr_version) >= parse_version(
                min_ver)

        isi_sdk_version = dict(
            supported_version=supported_version,
            unsupported_version_message=unsupported_version_message)

        return isi_sdk_version

    except Exception as e:
        unsupported_version_message = \
            "Unable to get the isilon sdk version," \
            " failed with Error {0} ".format(str(e))
        isi_sdk_version = dict(
            supported_version=False,
            unsupported_version_message=unsupported_version_message)
        return isi_sdk_version


'''
This method provides common access parameters required for the Ansible Modules on Isilon
options:
  onefshost:
    description:
    - IP of the Isilon OneFS host
    required: true
  port_no:
    decription:
    - The port number through which all the requests will be addressed by the OneFS host.
  verifyssl:
    description:
    - Boolean value to inform system whether to verify ssl certificate or not.
  api_user:
    description:
    - User name to access OneFS
  api_password:
    description:
    - password to access OneFS
'''


def get_isilon_management_host_parameters():
    return dict(
        onefs_host=dict(type='str', required=True),
        verify_ssl=dict(type='bool', required=True),
        port_no=dict(type='str'),
        api_user=dict(type='str', required=True),
        api_password=dict(type='str', required=True, no_log=True)
    )


'''
This method is to establish connection to Isilon
using its SDK.
parameters:
  module_params - Ansible module parameters which contain below OneFS details
                 to establish connection on to OneFS
     - onefshost: IP of OneFS host.
     - verifyssl: Boolean value to inform system whether to verify ssl certificate or not.
     - port_no: The port no of the OneFS host.
     - username:  Username to access OneFS
     - password: Password to access OneFS
returns configuration object 
'''


def get_isilon_connection(module_params):
    if HAS_ISILON_SDK:
        conn = isi_sdk.Configuration()
        if module_params['port_no'] is not None:
            conn.host = module_params['onefs_host'] + ":" + module_params[
                'port_no']
        else:
            conn.host = module_params['onefs_host']
        conn.verify_ssl = module_params['verify_ssl']
        conn.username = module_params['api_user']
        conn.password = module_params['api_password']
        api_client = isi_sdk.ApiClient(conn)
        return api_client


'''
This method is to initialize logger and return the logger object 
parameters:
     - module_name: Name of module to be part of log message.
     - log_file_name: name of the file in which the log meessages get appended.
     - log_devel: log level.
returns logger object 
'''


def get_logger(module_name, log_file_name='dellemc_ansible_provisioning.log',
               log_devel=logging.INFO):
    FORMAT = '%(asctime)-15s %(filename)s %(levelname)s : %(message)s'
    logging.basicConfig(filename=log_file_name, format=FORMAT)
    LOG = logging.getLogger(module_name)
    LOG.setLevel(log_devel)
    return LOG


'''
Convert the given size to bytes
'''
KB_IN_BYTES = 1024
MB_IN_BYTES = 1024 * 1024
GB_IN_BYTES = 1024 * 1024 * 1024
TB_IN_BYTES = 1024 * 1024 * 1024 * 1024


def get_size_bytes(size, cap_units):
    if size is not None and size > 0:
        if cap_units in ('kb', 'KB'):
            return size * KB_IN_BYTES
        elif cap_units in ('mb', 'MB'):
            return size * MB_IN_BYTES
        elif cap_units in ('gb', 'GB'):
            return size * GB_IN_BYTES
        elif cap_units in ('tb', 'TB'):
            return size * TB_IN_BYTES
        else:
            return size
    else:
        return 0


'''
Convert size in byte with actual unit like KB,MB,GB,TB,PB etc.
'''


def convert_size_with_unit(size_bytes):
    if not isinstance(size_bytes, int):
        raise ValueError('This method takes Integer type argument only')
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


'''
Convert the given size to size in GB, size is restricted to 2 decimal places
'''


def get_size_in_gb(size, cap_units):
    size_in_bytes = get_size_bytes(size, cap_units)
    size = Decimal(size_in_bytes / GB_IN_BYTES)
    size_in_gb = round(size, 2)
    return size_in_gb

