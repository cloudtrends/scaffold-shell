#!/bin/bash

iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
iptables -t nat -A POSTROUTING -s 192.168.120.0/24 -o eth1 -j MASQUERADE
iptables -A FORWARD -i eth0 -j ACCEPT
iptables -A FORWARD -s 192.168.120.0/24 -m state --state ESTABLISHED,RELATED -j ACCEPT
service iptables save
echo 1 > /proc/sys/net/ipv4/ip_forward
service iptables restart

