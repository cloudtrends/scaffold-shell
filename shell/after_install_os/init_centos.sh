#!/bin/bash



yum install git -y;
yum install wget -y;
yum install openssh -y ; yum install openssh-clients -y

yum install vim -y;

service iptables stop; chkconfig iptables off;
sed -i s/SELINUX=enforcing/SELINUX=permissive/g /etc/selinux/config
rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
#rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm

yum update -y

yum install acpid -y ; service acpid restart ; chkconfig acipd on ;
yum install vixie-cron crontabs -y;chkconfig crond on
yum install yum-priorities -y 
yum install acpid -y;chkconfig acpid on;service acpid start
yum install ntp -y;chkconfig ntpd on;



ntpdate cn.pool.ntp.org ; ntpdate 1.cn.pool.ntp.org;ntpdate  -d cn.pool.ntp.org

ntpdate  -d cn.pool.ntp.org

git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle

 service iptables stop;

  chkconfig iptables off;

  yum install nfs-utils -y;yum install rpcbind -y

   mkdir -p /export/primary ;mkdir -p /export/secondary;mkdir -p /export/normal;mkdir -p /export/vms;


   service rpcbind start;service nfs start
   service rpcbind restart;service nfs restart
   chkconfig rpcbind on;chkconfig nfs on
    yum -y install openssh-server openssh-clients

    echo '/export/primary *(rw,async,no_root_squash,no_subtree_check,insecure)'


    yum install xorg-x11-xauth -y
    yum install  xorg-x11-fonts-*  -y
    yum install xorg-x11-utils  -y
    yum install xhost -y
    yum install x11-xserver-utils -y;

    chkconfig --level 345 vncserver on



    yum install -y  tigervnc-server tigervnc-server-module
    yum install -y  tigervnc-server tigervnc-server-module libXfont pixman xterm xorg-x11-twm
    yum -y install tigervnc-server pixman pixman-devel libXfont

yum install gcc -y
yum install sqlite-devel -y


echo "cat /proc/sys/net/ipv4/ip_forward"

cat /proc/sys/net/ipv4/ip_forward

