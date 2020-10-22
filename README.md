# Ansible Modules for Dell EMC Isilon
The Ansible Modules for Dell EMC Isilon allow Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuartion and management of Dell EMC Isilon arrays.

The capabilities of the Ansible modules are managing users, groups, access zones, file system, nfs exports, smb shares, snapshots, snapshot schedules and smart quotas; and to gather facts from the array. The tasks can be executed by running simple playbooks written in yaml syntax.

## Supported Platforms
  * Dell EMC Isilon Arrays version 8.0 and above.

## Prerequisites
  * Ansible 2.7 or higher
  * Python >= 2.7.12
  * Red Hat Enterprise Linux 7.6
  * Python SDK for Isilon ( version 8.1.1 )

## Idempotency
The modules are written in such a way that all requests are idempotent and hence fault-tolerant. It essentially means that the result of a successfully performed request is independent of the number of times it is executed.

## List of Ansible Modules for Dell EMC Isilon
  * File System Module
  * Access Zone Module
  * Users Module
  * Groups Module
  * Snapshot Module
  * Snapshot Schedule Module
  * NFS Module
  * SMB Module
  * Smart Quota Module
  * Gather Facts Module

## Installation of SDK
Install python sdk named 'isi-sdk-8-1-1'. It can be installed using pip, based on appropriate python version.

## Documentation
Check documentation from each module's file in /library/

## Examples
Check examples from each module's file in /library/

## Results
Each module returns the updated state and details of the entity. 
For example, if you are using the group module, all calls will return the updated details of the group.
Sample result is shown in each module's documentation.

## Support
  * Ansible modules for Isilon are supported by Dell EMC and are provided under the terms of the license attached to the source code.
  * For any setup, configuration issues, questions or feedback, join the [Dell EMC Automation community](https://www.dell.com/community/Automation/bd-p/Automation).
  * For any Dell EMC storage issues, please contact Dell support at: https://www.dell.com/support.
  * Dell EMC does not provide support for any source code modifications.
