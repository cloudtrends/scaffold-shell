#!/bin/bash


yum install wget -y
yum install python-devel -y



wget  --no-check-certificate  http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c7.tar.gz
tar zxvf setuptools-0.6c7.tar.gz
cd setuptools-0.6c7
python ./setup.py install 






wget http://downloads.sourceforge.net/zenoss/Zenoss-Plugins-2.0.4.tar.gz
tar zxvf Zenoss-Plugins-2.0.4.tar.gz
cd Zenoss-Plugins-2.0.4
python ./setup.py build
python ./setup.py install


zenplugin.py --list-plugins

