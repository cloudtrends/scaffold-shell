#!/bin/bash



QEMU_NETWORK_AUTOSTART_XML="/etc/libvirt/qemu/networks/autostart/default.xml"
TMPDIR="/root/tmp_ovs"
mkdir -p  ${TMPDIR}

function help(){
    echo "after install open vswitch"
    echo "http://cloud.domolo.com/t/al2cyh1rfl6s.html"
}

function auto_config_ovs(){

    
  mv ${QEMU_NETWORK_AUTOSTART_XML}  ${TMPDIR}

  rm -rf ${QEMU_NETWORK_AUTOSTART_XML} 

  sed -i 's/#BRCOMPAT=yes/BRCOMPAT=yes/g' /etc/sysconfig/openvswitch

  

  ifconfig virbr0 down
  
  modprobe -r bridge
  modprobe brcompat
  modprobe openvswitch
  rmmod bridge
  
  echo 'blacklist bridge' >> /etc/modprobe.d/blacklist.conf


  /etc/init.d/openvswitch start


  ovs-vsctl -V

}


auto_config_ovs

ovs-vsctl add-br ovsbr












