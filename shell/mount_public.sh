#!/bin/bash


yum install nfs-utils -y


service rpcbind restart

service nfs restart

HOST=172.16.232.48

showmount -e ${HOST}


mkdir -p /mnt/builds

mount ${HOST}:/volume1/builds /mnt/builds

