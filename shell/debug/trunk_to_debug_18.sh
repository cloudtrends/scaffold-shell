

#scp -rp /Users/chunfeng/workspace42_maintrunk/server/  root@192.168.120.18:/root/tmp/abc


#mkdir /c

umount /c

mount c: /c

#scp -rp *.java /c/Users/chunfeng/workspace42_maintrunk/server/  root@192.168.120.18:/root/tmp/abc

#scp -rp  /c/Users/chunfeng/workspace42_maintrunk/server/*/*/*.java  root@192.168.120.18:/root/tmp/abc

# must use auto login
# http://www.cyberciti.biz/faq/ssh-password-less-login-with-dsa-publickey-authentication/

#find /c/Users/chunfeng/workspace42_maintrunk/server/ -name "*.java" -exec scp '{}' root@192.168.120.18:/root/tmp/abc \;

#
#for f in `ssh user@host "find /some/dir/ -name "*.pdf"`; do
#    scp user@host:$f /some/local/dir
#done
#

#cd /c/Users/chunfeng/workspace42_maintrunk/server/src
#rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.18:/home/source/trunk/server/src

#cd /c/Users/chunfeng/workspace42_maintrunk/api/src
#rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.18:/home/source/trunk/api/src

#CF_DIR=/c/Users/chunfeng/workspace_cf_brunch

#REMOTE_DIR=/home/source/elasterstack5_cf

echo "error "
exit 1

echo "cp agent"
target=agent
cd ${CF_DIR}/${target}/src
rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.18:${REMOTE_CF_DIR}/${target}/src

echo "cp utils"
target=utils
cd ${CF_DIR}/${target}/src
rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.18:${REMOTE_CF_DIR}/${target}/src

echo "cp server"
target=server
cd ${CF_DIR}/${target}/src
rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.18:${REMOTE_CF_DIR}/${target}/src
rsync --recursive --relative  --include="*.xml.in"  ./ root@192.168.120.18:${REMOTE_CF_DIR}/${target}/src

echo "cp api with properties"
target=api
cd ${CF_DIR}/${target}/src
rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.18:${REMOTE_CF_DIR}/${target}/src
rsync --recursive --relative  --include="*.properties"  ./ root@192.168.120.18:${REMOTE_CF_DIR}/${target}/src

echo "cp core"
target=core
cd ${CF_DIR}/${target}/src
rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.18:${REMOTE_CF_DIR}/${target}/src

#echo "cp ui"
#cd /c/Users/chunfeng/workspace42_maintrunk/ui/scripts
#rsync --recursive --relative  --include="*.js"  ./ root@192.168.120.18:/home/source/trunk/ui/scripts



#echo "cp agent"
#cd /c/Users/chunfeng/workspace42_maintrunk/agent/src
#rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.18:/home/source/trunk/agent/src







#cd /c/Users/chunfeng/workspace42_maintrunk/server/src
#rsync /c/tmp  ./ root@192.168.120.18:/root/tmp



