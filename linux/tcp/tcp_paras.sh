#!/bin/bash

ktcpopt 

sed -i '/net.ipv4.tcp_syncookies\|net.ipv4.tcp_tw_reuse\|net.ipv4.tcp_tw_recycle\|net.ipv4.tcp_fin_timeout\|net.ipv4.tcp_max_syn_backlog\|net.ipv4.tcp_max_tw_buckets\|net.ipv4.ip_local_port_range/d' /etc/sysctl.conf

sed -i '$a\net.ipv4.tcp_syncookies=1\nnet.ipv4.tcp_tw_reuse=1\nnet.ipv4.tcp_tw_recycle=1\nnet.ipv4.tcp_fin_timeout=30\nnet.ipv4.tcp_max_syn_backlog=8192\nnet.ipv4.tcp_max_tw_buckets=5000\nnet.ipv4.ip_local_port_range=10000 65000' /etc/sysctl.conf
