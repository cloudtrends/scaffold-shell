#!/bin/bash


M=1
while true
do
dd if=/dev/zero bs=500M | gzip | gzip -d | gzip | gzip -d | gzip | gzip -d > /dev/null &
sleep 1
let "M = $M + 1"
echo ${M}
if [ "${M}" -eq "3" ];then
    exit
fi
done
