#!/bin/bash
service iptables stop
chkconfig iptables off

yum install net-snmp net-snmp-utils net-snmp-devel -y
service snmpd start ; chkconfig snmpd on; netstat -apn | grep snmpd
mv /etc/snmp/snmpd.conf  /etc/snmp/snmpd.conf.bak.ori
touch /etc/snmp/snmpd.conf
echo 'rocommunity  public' > /etc/snmp/snmpd.conf
service snmpd restart
snmpwalk -v 1 -c public -O e 127.0.0.1