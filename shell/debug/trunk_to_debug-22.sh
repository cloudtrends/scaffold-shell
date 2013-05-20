

#scp -rp /Users/chunfeng/workspace42_maintrunk/server/  root@192.168.120.22:/root/tmp/abc


#mkdir /c

umount /c

mount c: /c

#scp -rp *.java /c/Users/chunfeng/workspace42_maintrunk/server/  root@192.168.120.22:/root/tmp/abc

#scp -rp  /c/Users/chunfeng/workspace42_maintrunk/server/*/*/*.java  root@192.168.120.22:/root/tmp/abc

# must use auto login
# http://www.cyberciti.biz/faq/ssh-password-less-login-with-dsa-publickey-authentication/

#find /c/Users/chunfeng/workspace42_maintrunk/server/ -name "*.java" -exec scp '{}' root@192.168.120.22:/root/tmp/abc \;

#
#for f in `ssh user@host "find /some/dir/ -name "*.pdf"`; do
#    scp user@host:$f /some/local/dir
#done
#

#cd /c/Users/chunfeng/workspace42_maintrunk/server/src
#rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.22:/home/source/trunk/server/src

#cd /c/Users/chunfeng/workspace42_maintrunk/api/src
#rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.22:/home/source/trunk/api/src


echo "cp agent"
cd /c/Users/chunfeng/workspace42_maintrunk/agent/src
rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.22:/home/source/trunk/agent/src




echo "cp utils"
cd /c/Users/chunfeng/workspace42_maintrunk/utils/src
rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.22:/home/source/trunk/utils/src

echo "cp server"
cd /c/Users/chunfeng/workspace42_maintrunk/server/src
rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.22:/home/source/trunk/server/src
rsync --recursive --relative  --include="*.xml.in"  ./ root@192.168.120.22:/home/source/trunk/server/src





echo "cp api with properties"
cd /c/Users/chunfeng/workspace42_maintrunk/api/src
rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.22:/home/source/trunk/api/src
rsync --recursive --relative  --include="*.properties"  ./ root@192.168.120.22:/home/source/trunk/api/src


echo "cp core"
cd /c/Users/chunfeng/workspace42_maintrunk/core/src
rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.22:/home/source/trunk/core/src

echo "cp ui"
cd /c/Users/chunfeng/workspace42_maintrunk/ui/scripts
rsync --recursive --relative  --include="*.js"  ./ root@192.168.120.22:/home/source/trunk/ui/scripts



#echo "cp agent"
#cd /c/Users/chunfeng/workspace42_maintrunk/agent/src
#rsync --recursive --relative  --include="*.java"  ./ root@192.168.120.22:/home/source/trunk/agent/src







#cd /c/Users/chunfeng/workspace42_maintrunk/server/src
#rsync /c/tmp  ./ root@192.168.120.22:/root/tmp



