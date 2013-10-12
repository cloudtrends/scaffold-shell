#!/bin/bash


echo "http://wiki.centos.org/HowTos/KVM"


yum install kvm kmod-kvm -y

yum install qemu -y

yum install -y qemu-kvm.x86_64 qemu-kvm-tools.x86_64 \
    kvm libvirt bridge-utils tunctl python-virtinst.noarch avahi -y

yum groupinstall virtualization -y

modprobe kvm-intel

echo "usermod -G kvm -a USERNAME"

