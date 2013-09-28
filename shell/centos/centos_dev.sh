#!/bin/bash


yum install xz -y
yum -y install ncurses-devel  -y
yum install gcc make kernel-devel -y
yum groupinstall "Development Tools" -y
yum groupinstall "Development Libraries" "Development Tools" -y


