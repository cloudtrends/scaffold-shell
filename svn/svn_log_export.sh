#!/bin/bash


#echo "Do you wish to install this program?"
#select yn in "Yes" "No"; do
#case $yn in
#    Yes ) make install; break;;
#No ) exit;;
#esac
#done

read -p "Input begin revision number:" BEGIN_R_NUM
read -p "Input begin revision number:" END_R_NUM
read -p "Input svn repo dir :" REPO_DIR
if [ -z ${REPO_DIR} ]; then 
    echo "repo dir is empty"
    exit 1
fi

echo "Begin and end revision number : ${BEGIN_R_NUM}-${END_R_NUM}"

CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FN=`date +%s`
SAVE_FILE="${CDIR}/${FN}-${BEGIN_R_NUM}-to-${END_R_NUM}.txt"
touch ${SAVE_FILE}
echo "go into repo dir ${REPO_DIR}"
if [ ! -d ${REPO_DIR} ]; then
    echo "repo dir not exist"
    exit 1
else
    echo "go into repo dir ${REPO_DIR}"
    cd ${REPO_DIR}
fi

for (( c=${BEGIN_R_NUM}; c<=${END_R_NUM}; c++ ))
do
     C=` svn log -r${c}  -v`
     echo "${C}" >> ${SAVE_FILE}
done



echo "return into dir:${CDIR}"


