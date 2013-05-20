#!/bin/bash


setenforce 0

sed -i s/SELINUX=enforcing/SELINUX=permissive/g /etc/selinux/config

echo "cloud ALL =NOPASSWD : ALL"      >>  /etc/sudoers
echo "cloud   ALL=(ALL)       ALL"      >>  /etc/sudoers
echo "#Defaults    requiretty"      >>  /etc/sudoers

echo "cloud ALL =NOPASSWD : ALL"      >>  /etc/sudoers

echo 'Defaults:cloud !requiretty'     >>  /etc/sudoers


