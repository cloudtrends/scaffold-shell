#!/bin/bash

ETH=eth4
IP=$1

ifconfig $ETH down

ifconfig $ETH $IP netmask 255.255.255.0 up

route -n

route add default gw 10.1.1.1

mkdir -p /mnt/builds

mount 172.16.232.49:/volume1/builds /mnt/builds

