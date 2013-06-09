




DEBUG_SERVER=s12

mkdir -p /d

umount /d

mount d: /d

LOCAL_PATH=/d/workspace-for-maven-new/ElasterView
LOCAL_VIEW_PATH=${LOCAL_PATH}/elasterview-plugin

REMOTE_VIEW_PATH=/home/source/trunk/ElasterView/elasterview-plugin








FILE_PROPERTIES=elaster-view_commands.properties
LOCAL_VIEW_CMD_PROPERTIES_FILE=${LOCAL_VIEW_PATH}/${FILE_PROPERTIES}
REMOTE_VIEW_CMD_PROPERTIES_FILE=${REMOTE_VIEW_PATH}/${FILE_PROPERTIES}
rm -f s12:${REMOTE_VIEW_CMD_PROPERTIES_FILE}
scp ${LOCAL_VIEW_CMD_PROPERTIES_FILE}  s12:${REMOTE_VIEW_CMD_PROPERTIES_FILE}
echo "--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- "

REFERSH_ADD_DEVICE_FILE=src/com/tcloud/elaster/api/commands/device/RefershAddDeviceCmd.java
LOCAL_ADD_DEVICE_FILE=${LOCAL_VIEW_PATH}/${REFERSH_ADD_DEVICE_FILE}
REMOTE_ADD_DEVICE_FILE=${REMOTE_VIEW_PATH}/${REFERSH_ADD_DEVICE_FILE}
rm -f s12:${REMOTE_ADD_DEVICE_FILE}
scp ${LOCAL_ADD_DEVICE_FILE} s12:${REMOTE_ADD_DEVICE_FILE}

echo "--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- "


REFERSH_MODEL_DEVICE_FILE=src/com/tcloud/elaster/api/commands/device/RefershModelDeviceCmd.java
LOCAL_MODEL_DEVICE_FILE=${LOCAL_VIEW_PATH}/${REFERSH_MODEL_DEVICE_FILE}
REMOTE_MODEL_DEVICE_FILE=${REMOTE_VIEW_PATH}/${REFERSH_MODEL_DEVICE_FILE}
rm -f s12:${REMOTE_MODEL_DEVICE_FILE}
scp ${LOCAL_MODEL_DEVICE_FILE} s12:${REMOTE_MODEL_DEVICE_FILE}


echo "--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- "

ssh s12 "chown root ${REMOTE_VIEW_PATH}/src/com/tcloud/elaster/api/commands/device/*.java"
ssh s12 "chmod 666 ${REMOTE_VIEW_PATH}/src/com/tcloud/elaster/api/commands/device/*.java"

ssh s12 "ls -lh ${REMOTE_VIEW_PATH}/src/com/tcloud/elaster/api/commands/device/"




















exit 1

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



