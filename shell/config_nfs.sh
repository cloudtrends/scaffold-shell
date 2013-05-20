#!/bin/bash

setenforce 0

sed -i s/SELINUX=enforcing/SELINUX=permissive/g /etc/selinux/config



rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm


rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6

	  

yum install nfs-utils -y

yum install rpcbind -y






chkconfig nfs on

chkconfig rpcbind on

mkdir -p /export/secondary
mkdir -p /export/primary

echo "/export/secondary *(rw,async,no_root_squash)" >> /etc/exports
echo "/export/primary *(rw,async,no_root_squash)" >> /etc/exports



exportfs
service rpcbind restart

service nfs restart
	  
	  
	  
	  
	  
# vi /etc/sysconfig/nfs

echo "LOCKD_TCPPORT=32803" >>  /etc/sysconfig/nfs
echo "LOCKD_UDPPORT=32769" >>  /etc/sysconfig/nfs
echo "MOUNTD_PORT=892" >>  /etc/sysconfig/nfs
echo "RQUOTAD_PORT=875" >>  /etc/sysconfig/nfs
echo "STATD_PORT=662" >>  /etc/sysconfig/nfs
echo "STATD_OUTGOING_PORT=2020" >>  /etc/sysconfig/nfs
echo 'RPCNFSDARGS="-N 4"' >>  /etc/sysconfig/nfs
		
		

	  
	  