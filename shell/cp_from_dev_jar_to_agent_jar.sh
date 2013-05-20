#!/bin/bash

 
 
#local path
LP="/home/source/trunk/ElasterStack/client/target/cloud-client-ui-5.1/WEB-INF/lib"


find ${LP}   -name "cloud-*.jar"


#local version
LV="-5.1"

AGENT_HOST="10.1.1.29"

AGENT_HOST=$1

if [ -z ${AGENT_HOST} ];then
        echo "nohost"
        exit 1
fi



#agent host path
AHP="/usr/share/java"


echo "this script is used for debug agent "

echo "steps"

echo "1. running on debug mgmt server"

echo " compile first  "

echo "2. copy the jar to agent server "

TMP=""
jars="cloud-plugin-hypervisor-kvm cloud-agent cloud-utils cloud-api cloud-core"
for TMP in $jars
do
	scp ${LP}/${TMP}${LV}.jar  ${AGENT_HOST}:${AHP}/${TMP}.jar
done



echo "3. "


