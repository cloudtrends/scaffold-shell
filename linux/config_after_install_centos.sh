#!/bin/bash

#http://www.ruanyifeng.com/blog/2014/03/server_setup.html

echo "change root password"

passwd


read -p "Input new group:" NEW_GP

addgroup ${NEW_GP}

read -p "Input new username:" NEW_UN

useradd -d /home/${NEW_UN} -s /bin/bash  -m ${NEW_UN}

passwd ${NEW_UN}

usermod -a -G ${NEW_GP} ${NEW_UN}

# bill    ALL=(ALL) NOPASSWD: ALL  , this should .... need some calc




