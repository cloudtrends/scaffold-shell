#!/bin/bash
# $Id: installrtng.sh 11251 2010-07-23 23:40:44Z abhishek $ $HeadURL: svn://svn.lab.vmops.com/repos/vmdev/java/scripts/storage/secondary/installrtng.sh $
usage() {
  printf "Usage: %s: -m <secondary storage mount point> -f <system vm template file> [-h <hypervisor name: kvm|vmware|xenserver> ] [ -s <mgmt server secret key, if you specified any when running cloud-setup-database, default is password>][-u <Url to system vm template>] [-F <clean up system templates of specified hypervisor>] [-e <Template suffix, e.g vhd, ova, qcow2>]\n" $(basename $0) >&2
  printf "or\n" >&2
  printf "%s: -m <secondary storage mount point> -u <http url for system vm template> [-h <hypervisor name: kvm|vmware|xenserver> ] [ -s <mgmt server secret key>]\n" $(basename $0) >&2
}

failed() {
  echo "Installation failed"
  exit $1
}
#set -x
mflag=
fflag=
ext="qcow2"
templateId=3
hyper=
msKey=password
DISKSPACE=5120000  #free disk space required in kilobytes
while getopts 'm:h:f:u:Ft:e:s:' OPTION
do
  case $OPTION in
  m)	mflag=1
		mntpoint="$OPTARG"
		;;
  f)	fflag=1
		tmpltimg="$OPTARG"
		;;
  u)	uflag=1
		url="$OPTARG"
		;;
  F)	Fflag=1 ;;
  t)    templateId="$OPTARG"
  		;;
  e)    ext="$OPTARG"
  		;;
  h)    hyper="$OPTARG"
  		;;
  s)    sflag=1
		msKey="$OPTARG"
                ;;
  ?)	usage
		failed 2
		;;
  esac
done

if [[ "$mflag$fflag" != "11"  && "$mflag$uflag" != "11" ]]
then
  usage
  failed 2
fi

if [ -z "$hyper" ]
then
  usage
  failed 2
fi

if [ ! -d $mntpoint ] 
then
  echo "mount point $mntpoint doesn't exist\n"
  failed 4
fi

if [[ "$fflag" == "1" && ! -f $tmpltimg ]] 
then
  echo "template image file $tmpltimg doesn't exist"
  failed 3
fi


dbHost=
dbUser=
encType=

ext="qcow2"
templatedId=1

if [ ! $templateId ]
then
	echo "Unable to get template Id from database"
	failed 8
fi

localfile=$(uuidgen).$ext

mntpoint=`echo "$mntpoint" | sed 's|/*$||'`

destdir=$mntpoint/template/tmpl/1/$templateId/

mkdir -p $destdir
if [ $? -ne 0 ]
then
  printf "Failed to write to mount point $mntpoint -- is it mounted?\n"
  failed 3
fi

if [ "$Fflag" == "1" ]
then
  rm -rf $destdir/*
  if [ $? -ne 0 ]
  then
    echo "Failed to clean up template directory $destdir -- check permissions?"
    failed 2
  fi
fi

if [ -f $destdir/template.properties ]
then
  echo "Data already exists at destination $destdir -- use -F to force cleanup of old template"
  echo "IF YOU ARE ATTEMPTING AN UPGRADE, YOU MAY NEED TO SPECIFY A TEMPLATE ID USING THE -t FLAG"
  failed 4
fi

destvhdfiles=$(find $destdir -name \*.$ext)
if [ "$destvhdfiles" != "" ]
then
  echo "Data already exists at destination $destdir -- use -F to force cleanup of old template"
  failed 5
fi

tmpfile=$(dirname $0)/$localfile

touch $tmpfile
if [ $? -ne 0 ]
then
  printf "Failed to create temporary file in directory $(dirname $0) -- is it read-only or full?\n"
  failed 4
fi

destcap=$(df -P $destdir | awk '{print $4}' | tail -1 )
[ $destcap -lt $DISKSPACE ] && echo "Insufficient free disk space for target folder $destdir: avail=${destcap}k req=${DISKSPACE}k" && failed 4

localcap=$(df -P $(dirname $0) | awk '{print $4}' | tail -1 )
[ $localcap -lt $DISKSPACE ] && echo "Insufficient free disk space for local temporary folder $(dirname $0): avail=${localcap}k req=${DISKSPACE}k" && failed 4

if [ "$uflag" == "1" ]
then
  wget -O $tmpfile $url
  if [ $? -ne 0 ]
  then
    echo "Failed to fetch system vm template from $url"
    failed 5
  fi
fi


if [ "$fflag" == "1" ]
then
  cp $tmpltimg $tmpfile
  if [ $? -ne 0 ]
  then
    printf "Failed to create temporary file in directory $(dirname $0) -- is it read-only or full?\n"
    failed 6
  fi
fi


installrslt=$($(dirname $0)/createtmplt.sh -s 2 -d 'SystemVM Template' -n $localfile -t $destdir/ -f $tmpfile -u -v)

if [ $? -ne 0 ]
then
  echo "Failed to install system vm template $tmpltimg to $destdir: $installrslt"
  failed 7
fi

if [ "$ext" == "ova" ]
then
  tar xvf $destdir/$localfile -C $destdir &> /dev/null
fi

tmpltfile=$destdir/$localfile
tmpltsize=$(ls -l $tmpltfile| awk -F" " '{print $5}')

echo "$ext=true" >> $destdir/template.properties
echo "id=$templateId" >> $destdir/template.properties
echo "public=true" >> $destdir/template.properties
echo "$ext.filename=$localfile" >> $destdir/template.properties
echo "uniquename=routing-$templateId" >> $destdir/template.properties
echo "$ext.virtualsize=$tmpltsize" >> $destdir/template.properties
echo "virtualsize=$tmpltsize" >> $destdir/template.properties
echo "$ext.size=$tmpltsize" >> $destdir/template.properties

echo "Successfully installed system VM template $tmpltimg to $destdir"
