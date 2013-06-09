#! /usr/bin/python
#coding: utf-8
#filename test_wrap_line_combine.py

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

reload(sys) 
sys.setdefaultencoding('utf8')

from cs_common_slicer_helper import *
from cs_exception_common_clz import *

if __name__ == "__main__":
	print "Begin test wrap combine helper ..."
	java_file_name = "./test/test_me.java"
	ojscm = OneJavaSourceCodeManager( java_file_name )
	ojscm.is_debug = True
	ojscm.parser()
	func_list = ojscm.get_all_func_obj_list()
	for obj in func_list :
		code_list = obj.ori_code_list
		#code_list = obj.format_code_list
		print "begin ..."
		print obj.ori_code
		#print obj.format_code
		print "end...	...	...			..."
		bwher=BlockWrapperHelper( code_list )
		bwher.combine_wrap_line()
		print "combined line -	-	-	-	-	-	-"
		for line in bwher.new_code_list:
			#print line
			pass
	