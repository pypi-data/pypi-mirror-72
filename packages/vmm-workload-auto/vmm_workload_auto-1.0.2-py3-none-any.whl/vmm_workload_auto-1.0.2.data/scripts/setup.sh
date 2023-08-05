#!/bin/bash
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

fn() {
inp='M'
read -p "$1" inp
while [ "$inp" != 'Y' -a  "$inp" != 'N' ]
do
    echo "Please enter Y or N"
    read -p "$1" inp
done
if [ "$2" != "" -a "$inp" == 'N' ]
then
    echo "Please modify the" "$2" "file and run the setup again. For more help, please refer the README file"
exit
fi
export inp
}

setup_virt() {
    echo "setting up virtual env"
    pip3 install virtualenv
    virtualenv -p /usr/bin/python3 venv
    . ./venv/bin/activate
}

fn "Have you modified the config/conf.yml file as per your topology: Y/N " "conf.yml"
fn "Have you modified the csv file in config/ that was a part of the conf.yml: Y/N " ".csv"
read -p "Enter the http_proxy, e.g. http://proxy.esl.cisco.com:80 :" http_proxy
read -p "Enter the https_proxy, e.g. https://proxy.esl.cisco.com:80 :" https_proxy
read -p "Enter the comma separated no_proxy, e.g. 127.0.0.1,localhost,172.28.10.156 :" no_proxy
export http_proxy=$http_proxy
export https_proxy=$https_proxy
export no_proxy=$no_proxy
export PYTHONPATH=$PYTHONPATH:$PWD
echo $http_proxy
echo $https_proxy
echo $no_proxy
fn "Do you want to run in a virtual environment? Y/N "
echo $inp
WD=`pwd`
VENV=0
if [ $inp == "Y" ]
then
    VENV=1
    setup_virt
    #WD=`pwd`/../
    echo WD inside is $WD
    export VMM_TMP_VENV=1
fi
echo WD outside is $WD
ls $WD
python3 $WD/setup.py install
#pip3 install $WD/vmm_workload_auto-0.1.0.tar.gz
echo "VENV is " $VENV
sleep 3
if [ $VENV -eq 1 ]
then
    vmm_workload_auto --config=./config/conf.yml
    unset VMM_TMP_VENV
else
    export PATH=$PATH:/usr/local/bin
    vmm_workload_auto
fi
echo DONE
