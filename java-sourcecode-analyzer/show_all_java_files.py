#!/usr/bin/python
#coding: utf-8

import os
import os.path
import datetime
import sys
import string
import time
import re
import logging
import shutil
from optparse import OptionParser 


from cs_exception_common         import *



def show_java_files( start_dir  ):
    print "begin ..."

pack_class={}
def get_package_class_dict(full_path):
    parts = full_path.split( "/" )
    b_flag=False
    new_parts=[]
    for one in parts:
        if one == "src":
            b_flag = True
            continue
        if not b_flag:
            continue
        new_parts.append( one )
    len_parts=len( new_parts )
    tmp_i=0
    pack_str=""
    for one in new_parts:
        print one
        tmp_i = tmp_i + 1
        if tmp_i == (len_parts-1):
            break
        pack_str= pack_str + one + "."
    pack_str=[:-1]
    print pack_str


if "__main__" == __name__ :
    usage = "usage: %prog [options] package  "
    parser = OptionParser(usage=usage)
    parser.add_option("-P" , "--package",default="default" ,  dest="package" , type="string")
    parser.add_option("-D" , "--directory",default="default" ,  dest="f_directory" , type="string")
    (options, args) = parser.parse_args()
    if "default" == options.package or "default" == options.f_directory  :
        print parser.usage
        sys.exit( 0 )
        pass
    print "process package:",options.package
    start_path= options.f_directory +  "/" + options.package
    print "start path is :",start_path
    skip_file_list=[]
    skip_path_list=["test"]
    only_allow_file_list=None
    for file_name in getNextJavaSourceFile( start_path , skip_file_list , skip_path_list , only_allow_file_list  ):
        print file_name
        get_package_class_dict( file_name )





    print "End"









