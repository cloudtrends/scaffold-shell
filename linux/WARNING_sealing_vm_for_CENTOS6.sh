#!/bin/bash

#http://serverfault.com/questions/626889/what-is-the-recommended-method-to-prepare-red-hat-centos-7-templates

touch /.unconfigured
rm -f /etc/ssh/ssh_host_*
#rm -rf /etc/udev/rules.d/70-*
sed '/HOSTNAME=/d'  /etc/sysconfig/network
echo "HOSTNAME=localhost.localdomain" >> /etc/sysconfig/network

#sed '/HWADDR=/d'  /etc/sysconfig/network-scripts/ifcfg-eth0
#sed '/HWADDR=/d'  /etc/sysconfig/network-scripts/ifcfg-eth1
#sed '/HWADDR=/d'  /etc/sysconfig/network-scripts/ifcfg-eth2
#sed '/HWADDR=/d'  /etc/sysconfig/network-scripts/ifcfg-eth3



ifdown eth0
sed -i '/^HWADDR=.*$/d' /etc/sysconfig/network-scripts/ifcfg-eth0
sed -i '/^UUID=.*$/d' /etc/sysconfig/network-scripts/ifcfg-eth0
sed -i '/^BOOTPROTO=none$/d' /etc/sysconfig/network-scripts/ifcfg-eth0
# if return is 1 then add dhcp

sed -i '/^HWADDR=.*$/d' /etc/sysconfig/network-scripts/ifcfg-eth1
sed -i '/^HWADDR=.*$/d' /etc/sysconfig/network-scripts/ifcfg-eth2
sed -i '/^HWADDR=.*$/d' /etc/sysconfig/network-scripts/ifcfg-eth3
ifup eth0
rm -f /etc/udev/rules.d/70-persistent-net.rules


shutdown -h now



