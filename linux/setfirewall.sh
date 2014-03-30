#!/bin/bash

#!/bin/bash
#
# Flush all current rules from iptables
#
iptables -F
 
#
# Allow SSH connections on tcp port 22
# This is essential when working on remote servers via SSH to prevent locking yourself out of the system
#
# 28017 - MongoDB Web UI
 
#
# Do -NOT- remove the following line, 22 is to SSH in
#
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
 
#
# Configure the following
#
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
#iptables -A INPUT -p tcp --dport 28017 -j ACCEPT
 
# allow email
#iptables -A INPUT -p tcp --dport 25 -j ACCEPT
#iptables -A INPUT -p tcp --dport 110 -j ACCEPT
#iptables -A INPUT -p tcp --dport 143 -j ACCEPT
#iptables -A INPUT -p tcp --dport 993 -j ACCEPT
#iptables -A INPUT -p tcp --dport 995 -j ACCEPT
 
#
# Set default policies for INPUT, FORWARD and OUTPUT chains
#
 
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
 
#
# Set access for localhost
#
 
iptables -A INPUT -i lo -j ACCEPT
 
#
# Accept packets belonging to established and related connections
#
 
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
 
#
# Save settings
#
 
/sbin/service iptables save
 
#
# List rules
#
iptables -L -v


