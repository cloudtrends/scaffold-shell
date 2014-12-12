#!/bin/bash



yum install nginx -y 


mkdir -p /root/share
ln -s /mnt/share/ /usr/share/nginx/html/share


#/etc/nginx/conf.d/default.conf


LN=`awk '/index.htm;/{print NR - 1}' ./default.conf`
sed -i "${LN}i\tautoindex on;" ./default.conf

chkconfig nginx on
service nginx start


