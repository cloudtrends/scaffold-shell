#!/bin/bash









mkdir /mnt/hotfix
showmount -e 10.6.1.2
mount 10.6.1.2:/home/xenserver62 /mnt/hotfix/
cd /mnt/hotfix/hotfix/






# XS62ESP1002  XS62ESP1003  XS62ESP1005  XS62ESP1008  XS62ESP1009  XS62ESP1011  XS62ESP1013  XS62ESP1014  XS62ESP1015

#HOSTUUID=545cdf83-947c-4d9e-aaf9-12bf0d1dec86
#PNAME=XS62ESP1002 
UUUID=` cd ${PNAME};xe patch-upload file-name=${PNAME}.xsupdate ; cd ..` ; xe patch-apply uuid=${UUUID} host-uuid=${HOSTUUID};
 

