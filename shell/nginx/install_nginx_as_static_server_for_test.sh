#!/bin/bash



yum install nginx -y 


mkdir -p /root/share
ln -s /mnt/share/ /usr/share/nginx/html/share


CF=/etc/nginx/conf.d/default.conf


LN=`awk '/index.htm;/{print NR - 1}' ${CF}`
sed -i "${LN}i\tautoindex on;" ${CF}

chkconfig nginx on
service nginx start


