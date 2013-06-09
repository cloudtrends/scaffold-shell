#! /usr/bin/python
#coding: utf-8
#filename test_print_java_file_num.py
import os
import os.path
import datetime
import sys
import string
import time
import re
import calendar
import shutil
from optparse import OptionParser 

from cs_exception_common import *
from cs_exception_common_clz     import *
from cs_try_catch_analyzer         import *
from cs_formal_config             import *
from cs_formal_config_helper     import *



if "__main__" == __name__ :
    usage = "usage: %prog [options] arg1 arg2  "
    parser = OptionParser(usage=usage)    
    parser.add_option("-P" , "--package",default="default" ,  dest="package" , type="string")
    parser.add_option("-V" , "--version",default="default" ,  dest="version" , type="string")
    (options, args) = parser.parse_args()
    if "default" == options.package  or "default" == options.version :
        print parser.usage
        sys.exit( 0 )
        pass
    if options.package not in config_allow_package:
        print "package not int allow process list :" , options.package
        print parser.usage
        sys.exit( 0 )
        pass
    dir = config_cs_dir + os.sep + options.package
    java_file = 0
    print "dir:",dir
    for file in getNextFile( dir ):
        if file.endswith("java"):
            java_file += 1
    print "java file num:",java_file