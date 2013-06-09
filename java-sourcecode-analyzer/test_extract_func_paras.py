#! /usr/bin/python
#coding: utf-8
#filename test_extract_func_paras.py

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

from file_comp_lbl import *

import cs_global_variable 

from cs_exception_common_clz import *

from cs_try_catch_analyzer import *


LOG_FILENAME = '/home/text_extract_func_paras.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)


'''
D:\mydoc\SkyDrive\Document\python\cloudstack-exception>
python test_extract_func_paras.py -p d:\java\CloudStack\server
'''

def extract_func_paras( java_file_name):
	'''
	'''
	#java_file_name = './test_me.java'
	return_content = ''
	print java_file_name
	ojscm = OneJavaSourceCodeManager( java_file_name )
	ojscm.is_debug = True
	ojscm.parser()
	func_list = ojscm.get_all_func_obj_list()
	content = '\n' + java_file_name + '\n'
	for obj in func_list:
		if '' == obj.func_name :
			continue
		content += obj.func_name + "\t" + ";"+  obj.func_paras_md5  +","+ str( obj.func_paras_num ) +", \n ==" + obj.func_paras_str + "==\n"
		content += "\n"
		for tmp_obj in obj.func_paras_list:
			content += tmp_obj + " || "
		content += "\n"
	return "\n"+content + "\n"
if True:
	if "__main__" == __name__ :  
		usage = "usage: %prog [options] arg1 arg2 such as python cs_code_exception_extractor.py  -p /home/source/trunk/ "
		parser = OptionParser(usage=usage)	
		parser.add_option("-p" , "--path",default="default" ,  dest="java_path" , type="string")
		(options, args) = parser.parse_args()
		if "default" != options.java_path and len(options.java_path ) > 1 :
			start_path = options.java_path
			for dirname, dirnames, filenames in os.walk( start_path ):
				for subdirname in dirnames:
					file = os.path.join(dirname, subdirname)
				for filename in filenames:
					file = os.path.join(dirname, filename)
					# 只能是源文件，允许替换的文件，此处要验证
					if file.endswith( ".java" ): 
						#total_class_num += 1
						#content = "src:" + file + "\r\n"
						content = extract_func_paras( file )
						logging.debug( content )
	sys.exit(0)




