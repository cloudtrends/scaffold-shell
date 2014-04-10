#! /bin/bash
# coredump
#http://www.cppblog.com/qinqing1984/archive/2014/03/24/206316.html
sed -i '/ulimit -c unlimited\|export core_path=\/tmp\/corefiles\|mkdir -p $core_path\|echo "0" > \/proc\/sys\/kernel\/core_uses_pid\|echo "$core_path\/%e" > \/proc\/sys\/kernel\/core_pattern/d' ~/.bashrc

sed -i '$a\ulimit -c unlimited\nexport core_path=/tmp/corefiles\nmkdir -p $core_path\necho "0" > /proc/sys/kernel/core_uses_pid\necho "$core_path/%e" > /proc/sys/kernel/core_pattern' ~/.bashrc

