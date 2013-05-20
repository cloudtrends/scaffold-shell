#!/bin/bash



ES_HOME="/home/source/trunk/ElasterStack"
KVM_AGENT_HOST="root@$1"
ES_VERSION="-5.1"



if [ -z ${KVM_AGENT_HOST} ]; then
	echo "which kvm agent host I should copy to ?"
	exit 1
fi


if [ -n ${KVM_AGENT_HOST} ]; then
	echo " I will copy cloud-*.jar to ${KVM_AGENT_HOST} ... "
fi


echo "current ElasterStack Version is :${ES_VERSION}"

scp  ${ES_HOME}/api/target/cloud-api${ES_VERSION}.jar    ${KVM_AGENT_HOST}:/usr/share/java/cloud-api.jar
scp  ${ES_HOME}/core/target/cloud-core${ES_VERSION}.jar       ${KVM_AGENT_HOST}:/usr/share/java/cloud-core.jar
scp  ${ES_HOME}/server/target/cloud-server${ES_VERSION}.jar        ${KVM_AGENT_HOST}:/usr/share/java/cloud-server.jar
scp  ${ES_HOME}/utils/target/cloud-utils${ES_VERSION}.jar        ${KVM_AGENT_HOST}:/usr/share/java/cloud-utils.jar
scp  ${ES_HOME}/agent/target/cloud-agent${ES_VERSION}.jar        ${KVM_AGENT_HOST}:/usr/share/java/cloud-agent.jar
scp  ${ES_HOME}/plugins/hypervisors/kvm/target/cloud-plugin-hypervisor-kvm${ES_VERSION}.jar        ${KVM_AGENT_HOST}:/usr/share/java/cloud-plugin-hypervisor-kvm.jar
scp  ${ES_HOME}/console-proxy/target/cloud-console-proxy${ES_VERSION}.jar        ${KVM_AGENT_HOST}:/usr/share/java/cloud-console-proxy.jar





