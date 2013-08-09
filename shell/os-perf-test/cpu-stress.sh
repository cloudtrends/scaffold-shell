#!/bin/bash
let count=0
while :
do
#echo "countis :$count"
((count++))

if [ "$count" -eq "99999" ] ; then
    count=0
   sleep 2 
   echo "ok"
fi
done