#!/bin/bash

VNETNAME=$1
VNET=${VNETNAME}; for vm in $(virsh list | grep running | awk '{print $2}'); do virsh dumpxml $vm|grep -q "$VNET" && echo $vm; done


for vm in $(virsh list | grep running | awk '{print $2}'); do echo -n "$vm:"; virsh dumpxml $vm| grep -oP "vnet\d+" ; done 



