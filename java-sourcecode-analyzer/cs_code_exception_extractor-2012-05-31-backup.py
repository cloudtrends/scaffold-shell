#! /usr/bin/python
#coding: utf-8
#filename cs_code_exception_extractor.py 

import os
import os
import os.path
import datetime
import sys
import string
import time
import re
import calendar
import urllib
import shutil
import socket
from optparse import OptionParser 



reload(sys) 
sys.setdefaultencoding('utf8')



from file_comp_lbl import *
from cs_exception_common_clz import *


if True:
	file_ori = './test_me.java'
	#file_comp = './test_me.java.ori.java'
	file_comp = './test_me.java.format.java'
	strict = 0
	fc = file_compare_linebyline( file_ori , file_comp , strict )
	fc_obj = fc.compare_file()
	print fc_obj.desc
	sys.exit(0)











#logging.debug('This message should go to the log file')


#python cs_code_exception_extractor.py  -f /home/source/trunk/server/src/com/cloud/server/ManagementServerImpl.java 


total_class_num=0	
total_func_num=0
total_func_exception_num=0
total_func_catch_num=0
total_func_throw_num=0	
	
#python cs_code_exception_extractor.py  -p /home/source/trunk/	
if "__main__" == __name__ :
	usage = "usage: %prog [options] arg1 arg2 such as python cs_code_exception_extractor.py  -p /home/source/trunk/ "
	parser = OptionParser(usage=usage)	
	parser.add_option("-f" , "--java_file",default="default" ,  dest="java_source_file" , type="string")
	parser.add_option("-p" , "--path",default="default" ,  dest="java_path" , type="string")
	(options, args) = parser.parse_args()
	if "default" == options.java_path  and "default" == options.java_source_file:
		print usage
		sys.exit( 0 )
		pass	
	if "default" != options.java_source_file and len(options.java_source_file) > 1 :
		if  ( not options.java_source_file.endswith( ".java" ) ) :
			print "end not with java" , usage
			pass
		else:
			file_name = options.java_source_file
			if not os.path.exists( file_name ):
				print " file not exist : " , file_name , usage
				sys.exit(0)		
			else:
				ojscm = OneJavaSourceCodeManager( file_name )
				ojscm.is_debug = True
				ojscm.parser()
				ojscm.save_ori_file()
				ojscm.save_changed_file()
				ojscm.save_format_file()
				ojscm.print_exception_funcs()
				
		#print usage
		#sys.exit( 0 )
		pass
	if "default" != options.java_path and len(options.java_path ) > 1 :
		start_path = "/home/source/trunk"
		start_path = options.java_path
		for dirname, dirnames, filenames in os.walk( start_path ):
			for subdirname in dirnames:
				file = os.path.join(dirname, subdirname)
				#
				#print "path" + file
			for filename in filenames:
				file = os.path.join(dirname, filename)
				if file.endswith( "java" ):
					total_class_num += 1
					#print os.path.join(dirname, filename)
					ojscm = OneJavaSourceCodeManager( file )
					ojscm.parser()										
					total_func_num += ojscm.slicer.func_num
					total_func_exception_num += ojscm.slicer.func_exception_num
					total_func_catch_num += ojscm.slicer.func_catch_num 
					total_func_throw_num += ojscm.slicer.func_throw_num 
					#print " out total number :" + str( ojscm.slicer.func_num )
		print "total_class_num" , total_class_num
		print "total_func_num",total_func_num
		print "total_func_exception_num",total_func_exception_num
		print "total_func_catch_num",total_func_catch_num
		print "total_func_throw_num",total_func_throw_num
		pass
	#jca = JavaClassAnalyzer ( file_name )
	#jca.get_all_functions_with_exception() # get all exception's function
	pass		
	
	