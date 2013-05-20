#!/bin/bash

IMAGE=centos-zenoss-collector
VNCDISPLAY=:3



sudo /usr/libexec/qemu-kvm -enable-kvm  \
-smp 2,sockets=1,cores=1,threads=1 \
-drive file="${IMAGE}".qcow2,if=virtio,index=0 -boot c  \
-m 3120 \
-net nic \
-net tap,ifname=tap0 \
-nographic -vnc "${VNCDISPLAY}"

