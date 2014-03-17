#!/bin/bash


yum install libvirt


FILENAME=$1

if [ -z  ${FILENAME} ];then
    echo "not assign filename. abort"
    exit 1
fi


sed 's/^[ ]*//g' -i ${FILENAME}


function check_value()
{
        
    return 0
}

function repl_value()
{
    _FILENAME=$1
    _FVAL=$3
    _FKEY=$2
    _FSTR=${_FKEY}
    _RSTR="${_FKEY} = ${_FVAL}"
    sed  -i "/${_FSTR}/a ${_RSTR}"   ${_FILENAME}
}


function check_item(){
    _FILENAME=$1
    _FKEY=$2
    _FVAL=$3
    _FSTR=${_FKEY}
    _RSTR="${_FKEY} = ${_FVAL}"
    if  grep -q "^${_FSTR}" "${_FILENAME}" ; then
        check_value ${_FILENAME} ${_FKEY} ${_FVAL}      
    else
        _FNSTR="#${_FSTR} = "
        if  grep -q "^${_FNSTR}" "${_FILENAME}"  ; then
            repl_value ${_FILENAME} ${_FKEY} ${_FVAL}
        else
            echo "not find: ${_FNSTR}, append to file"
        fi
    fi
}


FILENAME="/etc/libvirt/libvirtd.conf"

FKEY="listen_tls"
FVAL="0"
check_item  ${FILENAME}  ${FKEY} ${FVAL}

FKEY="auth_tcp"
FVAL="\"none\""
check_item ${FILENAME} ${FKEY} ${FVAL}

FKEY="listen_tcp"
FVAL="1"
check_item ${FILENAME} ${FKEY} ${FVAL}



FILENAME="/etc/libvirt/qemu.conf"

FKEY="security_driver"
FVAL="\"none\""
check_item ${FILENAME} ${FKEY} ${FVAL}

FKEY="user"
FVAL="\"root\""
check_item ${FILENAME} ${FKEY} ${FVAL}

FKEY="group"
FVALi="\"root\""
check_item ${FILENAME} ${FKEY} ${FVAL}


FILENAME="/etc/sysconfig/libvirtd"

FKEY="LIBVIRTD_ARGS"
FVAL="\"--listen\""
check_item ${FILENAME} ${FKEY} ${FVAL}


chkconfig iptables off
/etc/init.d/iptables stop
sed -i s/SELINUX=enforcing/SELINUX=permissive/g /etc/selinux/config
setenforce Permissive
/etc/init.d/libvirtd restart







 





