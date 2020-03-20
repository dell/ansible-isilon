# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dell EMC.

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
options:
  - See respective platform section for more details
requirements:
  - See respective platform section for more details
notes:
  - Ansible modules are available for EMC PowerMax Storage Platform
'''

    # Documentation fragment for PowerMax (dellemc_powermax)
    DELLEMC_POWERMAX = r'''
options:
    serial_no:
        description:
            - the serial number of  PowerMax/VMAX array. It is a
              required parameter for all array specific operations
              except for getting list of arrays in the
              Gatherfacts module.
        type: str
        required: True
    unispherehost:
        description:
            - IP or FQDN of the Unisphere host
        type: str
        required: True
    universion:
        description:
            - Unisphere version
        type: int
        required: True
    verifycert:
        description:
            - boolean variable to specify whether to validate SSL
              certificate or not.
            - True - indicates that the SSL certificate should be
              verified.
            - False - indicates that the SSL certificate should not be
              verified.
        type: bool
        required: True
        choices: [True, False]
    user:
        description:
            - username of the Unisphere host.
        type: str
        required: True
    password:
        description:
            - the password of the Unisphere host.
        type: str
        required: True
requirements:
  - A DellEMC PowerMax Storage device.
  - Ansible 2.7.
notes:
  - The modules prefixed with dellemc_powermax are built to support the
    DellEMC PowerMax storage platform.
'''
    # Documentation fragment for Isilon (dellemc_isilon)
    DELLEMC_ISILON = r'''
    options:
        onefs_host:
            description:
            - IP address or FQDN of the Isilon cluster.
            type: str
            required: True
        port_no:
            description:
            - Port number of the Isilon cluster.It defaults to 8080 if
              not specified.
            type: str
            required: False
            default: '8080'
        verify_ssl:
            description:
            - boolean variable to specify whether to validate SSL
              certificate or not.
            - True - indicates that the SSL certificate should be
              verified.
            - False - indicates that the SSL certificate should not be
              verified.
            type: bool
            required: True
            choices: [True, False]
        api_user:
            type: str
            description:
            - username of the Isilon cluster.
            required: True
        api_password:
            type: str
            description:
            - the password of the Isilon cluster.
            required: True
    requirements:
      - A DellEMC Isilon Storage device.
      - Ansible 2.7 and above.
    notes:
      - The modules prefixed with dellemc_isilon are built to support the
        DellEMC Isilon storage platform.
    '''
