#! /usr/bin/python
#coding: utf-8
#filename cs_code_exception_extractor.py 

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

'''
throw new 可鞥的类型
31,	ServerError.InternalError, e.getMessage() != null ? e.getMessage() : "An unexpected error occurred."


312,	BaseCmd.INTERNAL_ERROR, cre.getMessage()

394,	"DB Exception on: " + sql, e

464,	"Failed to disassociate lun", uhe

484,	"Unable to resolve state '" + state + "' to a supported value {Enabled or Disabled}"


大于 3 的参数，手动修改
0,	true, "Failed to authenticate/authorize", e	3==	<true>	< "Failed to authenticate/authorize">	< e>
0,	BaseCmd.PARAM_ERROR, "Unable to execute API command " + cmd.getCommandName().substring(0, cmd.getCommandName().length() - 8) + " due to invalid value. " + invEx.getMessage()	3==	<BaseCmd.PARAM_ERROR>	< "Unable to execute API command " + cmd.getCommandName().substring(0>	< cmd.getCommandName().length() - 8) + " due to invalid value. " + invEx.getMessage()>
0,	BaseCmd.INTERNAL_ERROR, "Internal error executing API command " + cmd.getCommandName().substring(0, cmd.getCommandName().length() - 8)	3==	<BaseCmd.INTERNAL_ERROR>	< "Internal error executing API command " + cmd.getCommandName().substring(0>	< cmd.getCommandName().length() - 8)>
0,	errMsg + e.getMessage(), DataCenter.class, zoneId	3==	<errMsg + e.getMessage()>	< DataCenter.class>	< zoneId>
0,	"There are no F5 load balancer devices with the free capacity for implementing this network", DataCenter.class, guestConfig.getDataCenterId()	3==	<"There are no F5 load balancer devices with the free capacity for implementing this network">	< DataCenter.class>	< guestConfig.getDataCenterId()>
0,	"There are no NetScaler load balancer devices with the free capacity for implementing this network", DataCenter.class, guestConfig.getDataCenterId()	3==	<"There are no NetScaler load balancer devices with the free capacity for implementing this network">	< DataCenter.class>	< guestConfig.getDataCenterId()>
0,	errMsg, this.getClass(), 0	3==	<errMsg>	< this.getClass()>	< 0>
0,	"Unable to send commands to virtual router ", router.getHostId(), e	3==	<"Unable to send commands to virtual router ">	< router.getHostId()>	< e>
0,	"Unable to send commands to virtual router ", router.getHostId(), e	3==	<"Unable to send commands to virtual router ">	< router.getHostId()>	< e>
0,	true, "Unable to setup the local storage pool for " + host, e	3==	<true>	< "Unable to setup the local storage pool for " + host>	< e>
0,	true, "Unable to connect to pool " + pool, e	3==	<true>	< "Unable to connect to pool " + pool>	< e>
0,	"Unable to stop vm because the operation to stop timed out", vm.getHostId(), e	3==	<"Unable to stop vm because the operation to stop timed out">	< vm.getHostId()>	< e>
0,	true, "Unable to sync", e	3==	<true>	< "Unable to sync">	< e>
0,	true, "Unable to sync", e	3==	<true>	< "Unable to sync">	< e>




'''

'''
以后的代码总体上会分为两个部分替换：
1、为国际化目的的替换：throw new ，国际化成中文
2、为获得详细错误信息:try catch 重新整理Exception逻辑


所有，有换行的代码，暂时不替换。
（需要做一个功能：合并换行的功能！）




func 中的  ori_begin_line_num 和 end line_num 是做参考用的。
每个与代码有关类都有三个样子：
1、真是的代码
2、语法格式化后的代码，或者去掉comment后的代码
3、修改后的代码


'''


LOG_FILENAME = '/home/es_catch_exceptions.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)



if False:
	'''
	替换掉代码中的 comments 测试
	'''
	file_ori = ReadFileToString ( './test_me.java' )
	result_str = RemoveBlockComments( file_ori , '\n' )
	print result_str
	sys.exit(0)

def get_all_try_catch_blocks( java_file_name ):
	ojscm = OneJavaSourceCodeManager( java_file_name )
	ojscm.is_debug = True
	ojscm.parser()
	func_list = ojscm.get_all_func_obj_list()
	content_try_catchs = ''
	for obj in func_list:
		if '' == obj.func_name :
			continue
		tmp_content_try_catchs = ''
		tmp_content_try_catchs += "\r\nfunc_name:" + obj.func_name + "\tBEGIN\r\n"
		func_try_blocks = SliceFuncToTryBlocks()
		split_by = ojscm.slicer.cr_lf
		func_try_blocks.convert_to_try_blocks( obj , split_by )
		is_have_try_catch = False
		for block in func_try_blocks.func_try_blocks_list:
			if  'try_catch' == block.block_type :
				tmp_content_try_catchs += block.ori_code
				is_have_try_catch = True
		tmp_content_try_catchs += "\r\nfunc END\r\n"
		if is_have_try_catch :
			content_try_catchs += tmp_content_try_catchs
	return content_try_catchs
	
	

if False:
	'''
	打印所有带　try catch 的代码
	'''
	if "__main__" == __name__ :
		usage = "usage: %prog [options] arg1 arg2 such as python cs_code_exception_extractor.py  -p /home/source/trunk/ "
		parser = OptionParser(usage=usage)	
		parser.add_option("-p" , "--path",default="default" ,  dest="java_path" , type="string")
		(options, args) = parser.parse_args()
		if "default" != options.java_path and len(options.java_path ) > 1 :
			#start_path = "/home/source/trunk"
			start_path = options.java_path
			for dirname, dirnames, filenames in os.walk( start_path ):
				for subdirname in dirnames:
					file = os.path.join(dirname, subdirname)
					#
					#print "path" + file
				for filename in filenames:
					file = os.path.join(dirname, filename)
					# 只能是源文件，允许替换的文件，此处要验证
					if file.endswith( ".java" ): 
						#total_class_num += 1
						content = "src:" + file + "\r\n"
						content += get_all_try_catch_blocks( file )
						logging.debug( content )
	sys.exit(0)

	
'''
	f = open( file_name + ".try_catch.java" , "w" )
	f.write( content_try_catchs )
	f.close()
	sys.exit( 0 )
'''


if False:
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
	
	