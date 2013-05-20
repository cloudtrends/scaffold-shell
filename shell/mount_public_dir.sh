#!/bin/bash


yum install nfs-utils -y


service rpcbind restart

service nfs restart

HOST=172.16.206.48

showmount -e ${HOST}


mkdir -p /mnt/systemvm

mount ${HOST}:/volume1/public /mnt/systemvm


