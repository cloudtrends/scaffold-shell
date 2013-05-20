#!/bin/bash

P=/root/svn_log_revision
mkdir -p ${P}

T=${P}/log_content.txt

touch ${T}

for i in {1..1857}
do

    svn log -r r$i >> ${T}
    echo $i
done


