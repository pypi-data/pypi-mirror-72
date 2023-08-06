# Copyright 2020 Cisco Systems, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

Introduction:
--------------

VMM Workload Automation is about the automation of network configuration
in Cisco's Nexus switches for workloads spawned in a VMWare environment.

Automatic Installation of Dependancies:
----------------------------------------

During installation, the following dependent python packages are installed.

a) pyvim

b) pyvmomi

c) PyYAML

d) Flask

If the above packages has dependancies on different packages, they also get installed.

Functionality:
--------------
When workloads are spawned in vCenter, they require provisioning in the network/fabric.
The workloads spawned in the vCenter are either associated with a DPG or a PG. Those DPG 
or PG in the VMWare needs to be mapped to a corresponding DCNM network. For the network 
provisioning to happen, each network object in a vCenter (a DPG or a PG) needs to be 
mapped to a network object in DCNM. A network object in DCNM has the following 
characteristics.

a) VRF Name

b) IPV4/IPV6 subnet and gateway information

c) Secondary IPV4/V6 and gateway information

d) VLAN ID

e) BGP-EVPN configuration

A static mapping needs to be defined in a config file that maps the network object in a 
vCenter to a network object in DCNM. Please refer the configuration section for more 
information.Once the config file is populated, the workload automation module (will be just referred to as module) can be started. Once started, it scans all the vCenters specified in the config file (conf.yml) and collects the following information for each vCenter:

Once the config file is populated, the workload automation module can be started. Once 
started, it scans all the vCenters specified in the config file (conf.yml) and collects 
the following information for each vCenter:

a) List of DVS and the DV-PG configured in all DC's.

b) List of PG's configured in every host in all DC's.

c) For every DPG or PG specified in the conf file, it finds the configured VLAN’s and the directly connected neighbor switches along with its interface information.

d) For every <DVS, DPG> or <Host, PG> pair specified in the config file, it gets the associated network mapping in DCNM.

Then, it merges all the information and calls the DCNM API’s to provision/amend 
the networks in all the switches that are discovered as neighbors in one of the 
steps above. Provisioning of the network/fabric uses DCNM’s top-down 
provisioning. Provisioning/Amending a network consists of the following steps:

1.	Attaching the network configuration to the relevant interfaces of one or more switches, that are discovered as neighbors. This is done by the workload automation module.

2.	Once the configuration is attached, the user has the option to review the exact CLI’s that will get pushed to the switches. 

3.	Once reviewed, the user can deploy the configuration to the switches. This can either be done by the module based on the configuration file setting (default is False) or the user can do it through DCNM. Only after this step the configuration appears in the switch(es).

Configuration Files:
--------------------

There are two configuration files.

1. Global YML File (Conf.yml): This file has some global configuration and access/credential information of the DCNM’s and the vCenters. The location of the CSV file for each DCNM is also specified here. Subsequent sections will have more information about the fields in the file.

2. CSV file (Sample.csv): This file has the mapping of <DVS, DVS-PG> or <Host, PG> pair in vCenter to Network name in DCNM. There’s a separate CSV file for each DCNM. Subsequent sections will have more information about the fields in the file.

conf.yml:
-----------

This file specifies the IP address, username and password of DCNM. And, for each DCNM, the list of vCenter’s information like the IP address, username, and password of the vCenters are also specified. Multiple DCNM’s can be specified in this conf.yml. For every DCNM instance, there’s an associated csv file. The multi-DCNM case is only applicable when the module is not run in a DCNM, but run in a server that has connectivity to all the DCNM’s and vCenters specified in the config file.

For better understanding, the hierarchy in this .yml file is given below:

- Global config parameters

- DCNM1

  - DCNM1 config parameters including location of the CSV file
  - vCenter1

    - vCenter1 config parameters
  - vCenter2

    - vCenter2 config parameters

The location of this file is dependant on the installation method. Please refer the
installation section. This file comes up with some example entries. Modify
this file to suit your environment. This file has the following entries.

LogFile: This specifies the name of the logfile including the absolute path that will be used by the workload automation module for logging the errors and debug information.
Make sure the directory has write permission for creating the log file.
e.g. /tmp/workloadauto.log

ListenPort: This specifies the port that the workload automation module will use to listen
for the REST API's. e.g. 9590. Make sure that this port is not used by any other
application. One way to find this information is by issuing 
"sudo netstat -tulpn".

AutoDeploy: This value indicates whether the module should automatically
deploy the configuration in the switches after doing the attachment. By
default, it's set to False so that the user can review the config and deploy
it himself in the DCNM.

NwkMgr: This is the top level section under that indicates the Network Manager 
section a.k.a DCNM. For multiple-DCNM's, the information underneath this will
repeat with the appropriate values. Look at the file conf_multiple_dcnm.yml
for a sample yml file that handles multiple DCNM's.

Ip: This specifies the Management IP address of the DCNM. e.g. 172.28.10.156. In case of a HA
setup, the management IP address of the Active DCNM node needs to be specified.

User: This specifies the username used to login to DCNM. e.g. admin

Password: This specifies the password of DCNM.

CsvFile: This specifies the absolute path of the location of the CSV file
for this DCNM. e.g. /etc/vmm_workload_auto/sample.csv.

ServerCntrlr: This section has information for the server controller,
a.k.a vCenter/vSphere. For multiple vCenters that fall under this DCNM, this
section will repeat. Please refer the file conf_multiple_vcenter.yml for a
sample file for multiple vCenters under a DCNM.

Ip: This specifies the IP address of the vCenter.

Type: This is the type of the server controller. Leave the default as
vCenter.

User: This refers to the username used to login to the vCenter.
e.g. administrator@vsphere.local

Password: This refers to the password for the vCenter.

CSV File:
----------

This file holds the mapping of the network object in vCenter to the network
created in DCNM. This file has the entries in CSV format,
i.e.. comma separated entries.
The main reason for having a CSV file is to specify the mapping between a vSphere’s PG (or DPG) to the DCNM’s Network name. It’s just a 1-1 mapping. But, since a PG or a DPG cannot stand on its own (not unique), we need an additional DVS name or Hostname to qualify it. 
This file has the following fields.

vCenter - This refers to the IP address of vCenter

Dvs - This refers to the name of the DVS.

Dvs_pg - This refers to the DVS PG in the DVS

Host - This refers to the ESXi Host/Server (IP address)

Host_pg - This refers to the port-group belonging to a VS in the host.

Fabric - This refers to the fabric in DCNM.

Network - This refers to the name of the network already created in DCNM.

Consider the table below:

vCenter Params	DCNM_Params vCenter	DVS	DVPortGroup/ Network	ESXi Host	Port Group/ Network	Fabric Name	Network Name

172.28.12.123	DVS1	DPG1			        Fab1	Network 10

172.28.12.123	DVS1	DPG1			        Fab2	Network 30

172.28.12.123			172.28.12.11	PG10	Fab1	Network 20

172.28.12.123			172.28.12.12	PG20	Fab1	Network 20


This table has the mapping for vCenter 172.28.12.123. This has four entries.

1. The first entry specifies  that for DPG1 in DVS1, the network in DCNM is ‘Network10’ in fabric ‘Fab1’. There can be cases where in the hosts of the DVS can connect to switches in multiple fabrics. The network name in each fabric can be different, which is why the fabric name is also needed. The example in the table shows one such case in the second entry.

2. The second entry specifies the same <DVS1, DPG1> pair being mapped to Network 30 in fabric ‘Fab2’.

3. The third entry specifies that for PG10 in host 172.28.12.11, the network in DCNM is ‘Network20’ in fabric ‘Fab1’

4. The forth entry specifies that for PG20 in host 172.28.12.11, the network in DCNM is ‘Network20’ in fabric ‘Fab1’
As can be seen in the above table, the network object is identified by a unique pair of either <DVS, DVS_PG> or <Host, Host PG>. If there’s a value specified for DVS, DVS_PG, then the values for <Host, Host_PG> will be blank. In other words, <DVS, DVS_PG> and <Host, Host_PG) are mutually exclusive.
When the above table is specified in a CSV format, it will appear as below in the CSV file:

172.28.12.123,DVS1,DPG1,,,Fab1,Network10
172.28.12.123,DVS1,DPG1,,,Fab2,Network30
172.28.12.123,,,172.28.12.11,PG10,Fab1,Network20
172.28.12.123,,,172.28.12.12,PG20,Fab1,Network20

Let’s consider more examples:

1)
172.28.10.184,DSwitchPad,DSPad-PG2,,,DEF,MyNetwork_30000

The above line in the CSV file specifies the IP address of vCenter as 172.28.10.184 and the <DVS, DVS PG> values are DSwitchPad, DSPad-PG2 respectively. Since the values for DVS, DVS-PG is specified, the values for Host, Host-PG will be blank as seen in the above example. The Fabric name is DEF and the network in DCNM is MyNetwork_30000.

2)
172.28.10.184,,,172.28.11.33,Pad_Workload_Auto_Nwk,DEF,MyNetwork_60000

In this example, the values for <DVS, DVS-PG> is left blank and the values for <Host, Host_PG> is specified as 172.28.11.33 and Pad_Workload_Auto_Nwk respectively. The fabric in DCNM is DEF and the network name in DCNM is MyNetwork_60000.
An example CSV file is given below:

vCenter,Dvs,Dvs_pg,Host,Host_pg,Fabric,Network

172.28.10.184,DSwitchNew,DPGNew,,,DEF,MyNetwork_30000

172.28.10.184,DSwitchNew,DPGNew,,,ABC,MyNetwork_30000

172.28.10.184,,,172.28.11.33,Pad_Workload_Auto_Nwk,DEF,MyNetwork_60000


Installation and starting the module:
--------------------------------------

There are couple of ways to install and use this module.

Using pip install Option 1:
----------------------------
This is for users who are familiar with doing pip install and know how to
setup the proxy or handle cases when there's a conflict in the python packages.

Step 1: Decide whether you want to run it run this in a virtual env or just
normally. If you decide to run this normally, ensure that the user has write permission for doing pip install.

Step 2: Setup the http_proxy, https_proxy and no_proxy appropriately.

For e.g: export http_proxy=http://proxy.esl.cisco.com:80

export https_proxy=https://proxy.esl.cisco.com:80

export no_proxy=127.0.0.1,172.28.10.0/24

In the above example, 172.28.10.0 specified in the no_proxy is the DCNM's management subnet.

Step 3:Download and install it from https://pypi.org/.

pip3 install vmm-workload-auto

Step 4:
By default, the installation will happen in the following directories unless
the user overrides by giving options in pip command.

The package will be installed under /usr/local/lib/python3.7/site-packages/vmm_workload_auto-0.1.1.dist-info

The config files will be installed under /usr/local/lib/python3.7/site-packages/etc/vmm_workload_auto

The source code will be placed under /usr/local/lib/python3.7/site-packages/workload_auto

Step 5:
Edit the config files in 
/usr/local/lib/python3.7/site-packages/etc/vmm_workload_auto as explained
under the Configuration Section.

Make sure that the path of the CSV file specified in the conf.yml file is correct.

Step 6 (Running the module):
The entry point for the python module will be /usr/local/bin/vmm_workload_auto.
Either run it as /usr/local/bin/vmm_workload_auto or just vmm_workload_auto,
if '/usr/local/bin/ is already in $PATH. Provide the config file as a command 
line option.

e.g
"/usr/local/bin/vmm_workload_auto --config=/usr/local/lib/python3.7/site-packages/etc/vmm_workload_auto/conf.yml"

[Please note the above config is preceded by two dashes.]

Step 7:
Finally, to uninstall the module, do "pip3 uninstall vmm-workload-auto"



Using the install script (Option 2):
------------------------------------

This is an alternate method for users who does not want to use pip install. The install script will do the installation and starting of the python module.

Step 1:
Goto https://pypi.org/project/vmm-workload-auto/ and 
download the latest .tar.gz file

Step 2:
Untar it. e.g.

tar -xvf vmm_workload_auto-0.1.0.tar.gz.

Step 3:
Modify the config/conf.yml and config/sample.csv according to your environment.

Step 4:
Run the setup script as "source setup.sh"

Step 5:
This script will initially prompt the user to edit the conf.yaml and .csv file.
Once that is done, the script will prompt the user for proxy and other details.
Once all that is done, the script will install the python packages and start
the module automatically.

REST API:
----------

This module also provides REST API’s for the operations described below:

1) Refresh:
When the CSV file is changed, a refresh operation needs to be performed. This operation will re-read the file and apply any new configuration if needed. The API is:

curl -XPOST http://127.0.0.1:{port}/workload_auto/refresh

2) Resync:
When there is any change in the DVS-PG, PG, Vlan or neighbour switches, then a re-sync operation is needed. If there are any changes found, the configuration is re-applied accordingly. The API is:

curl -XPOST http://127.0.0.1:{port}/workload_auto/resync

3) Clean 
In order to clean up the network provisioning done, a clean up operation is needed. The API is:

curl -XPOST http://127.0.0.1:{port}/workload_auto/clean


Post Install:
-------------

After running the module, go to the DCNM Network page and look for the Network
attachments done by the script. Review the configs and deploy it, if auto_deploy
is set to false.

Events in vCenter:
-------------------

Real time event processing is not done as of this release. The various relevant events and its significance to this module are given in this section. It is grouped by the operation that needs to be performed:

Refresh:
---------

For the following events, a refresh operation needs to be performed by running the REST API given above for refresh. The API will make the module to read the CSV file again and apply the network configuration to the relevant switch(es).

a) PG Add: Create an entry in the CSV file that specifies the associated network in DCNM for this PG. After the entry is added, call the refresh REST API.
b) DPG Add: Create an entry in the CSV file that specifies the associated network in DCNM for this DPG. After the entry is added, call the refresh REST API.

Resync:
--------

For the following events, a resync operation needs to be performed by running the REST API given above for resync. The API will make the script to discover the network objects and its associated properties again. The result of this operation is applying the network configuration to the new/changed switches/interfaces.

a) Host add to a DVS 
b) Modify VLAN in a DPG or PG
c) Change in topology: When any of the following information is changed, issue the Resync REST API to rediscover the topology and applying the REST API.
   1) Neighbour switch change. This can happen if the attached leaf switch is replaced with a new switch or rewired to a different switch.
   2) Interface change: This can happen due to re-wiring to a different interface in the switch.
   3) Host pNIC Change.
   4) Add an extra connection: This can happen when:

      i) A regular interface in the host is made a port-channel by connecting an extra interface from the host to the switch.
      ii) An extra interface in the host connecting to a different switch forming a vPC pair.

No-op
------
For the following events, no operation needs to be performed and is just given here for completeness.

a) Host Add: When a stand-alone host is added, no action is required either from the module or from the user perspective.

b) VSwitch Add: No action is required either from the module or from the user perspective.

c) DVS Delete: No action is required, since every individual DPG delete is already handled as given in the other sections.

Mapping Change
----------------

The different cases for mapping change in a CSV file and operation is given below:

a) If a new mapping is added, just issue the Refresh API after adding the mapping in the CSV file.

b) If the mapping between the vCenter network to the DCNM network need to change, then issue the clean REST API, modify the mapping the CSV file and then issue the refresh REST API. 

c) If the existing mapping needs to be deleted, then issue the clean REST API, delete the mapping in the CSV file and then issue the refresh API.

Other Events:
--------------
Following are other events or operations that does not fall directly into the above category. The events and the operation that needs to be performed is given below.

a) Host removed from the DVS: When a host is removed from the DVS, the network configuration in the associated leaf switch and connected interface needs to be removed. This needs to be done for all the DPG’s of this DVS. Please go to the DCNM and un-attach the appropriate network(s).

b) DPG or PG Delete: For all the network mappings specified in the spec file, that are associated with this DPG or PG, the network configuration in the relevant switches (and interfaces) needs to be removed. Please go to the DCNM and un-attach the appropriate network(s).

c) Port Down or Switch Down: If the port or switch is permanently going to be offline, the configuration needs to be removed out of band. If the switch is not reachable from the host, but if still managed by DCNM, one can still go to the DCNM and un-attach the appropriate network(s).

