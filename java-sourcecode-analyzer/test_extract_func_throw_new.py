#! /usr/bin/python
#coding: utf-8
#filename test_extract_func_throw_new.py
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


LOG_FILENAME = '/home/es_catch_exceptions.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)


'''
D:\mydoc\SkyDrive\Document\python\cloudstack-exception>
python test_extract_func_throw_new.py -p  d:\java\CloudStack\server

'''
all_unique_throw_new_class_dict={}
def get_catch_exception( java_file_name):
	'''
	返回格式： file_name , func_name, catch_exception , throw new exception
	完整测试 catch block 代码。
	
	先把 java 代码分成 function list
	再从 function 中提取: try catch 块
	
	再从 try catch 块中提取 catch 块
	
	再分析 catch 块的属性。
	'''
	#java_file_name = './test_me.java'
	return_content = ''
	#print java_file_name
	ojscm = OneJavaSourceCodeManager( java_file_name , None )
	ojscm.is_debug = True
	ojscm.parser()
	func_list = ojscm.get_all_func_obj_list()
	#print " func list num :" , len( func_list )
	for obj in func_list:
		if '' == obj.func_name :
			continue
		for line in obj.ori_code_list:
			if isJavaThrowNewLine( line ):
				return_content += line
				tmp_throw_new_cls= getThrowNewExceptionClass( line )
				if all_unique_throw_new_class_dict.get( tmp_throw_new_cls ) is None:
					all_unique_throw_new_class_dict[tmp_throw_new_cls] = tmp_throw_new_cls
		'''
		
		
		
		
		
		
		
		
		
		
		only show one line throw new else continue
		'''
		continue
		split_by = ojscm.slicer.cr_lf
		func_try_blocks = SliceFuncToTryBlocks()
		try_catch_blocks = func_try_blocks.convert_to_try_blocks( obj , split_by )
		#print "try num :" , len( try_catch_blocks )
		for block in try_catch_blocks :
			if  'try_catch' == block.block_type :
				#如果是嵌套的trycatch则不处理
				#print " try func name :",obj.func_name
				if block.is_nested_try_catch:
					#print "Skip nested try catch "
					cs_global_variable.all_throw_nested_trycatch += 1
					continue
				else:
					cs_global_variable.all_throw_not_nested_trycatch += 1
					#continue
				catch_blocks_extractor = ExtractCatchBlocksFromTryCatchBlocks( block )
				'''
				extract 前需要判断：是否可以 extract 
			
				'''
				'''
				
						attr_analyzer = TryCatchAttrAnalyzer( block , split_by  )
				block_attr = attr_analyzer.analysis()
				block.block_attr = block_attr
				'''
				
				new_block = catch_blocks_extractor.extract()
				for catch_block_obj in new_block.catch_block_list:
					catch_attr_analyzer = CatchAttrAnalyzer( catch_block_obj , split_by )
					catch_attr = catch_attr_analyzer.analysis()
					'''
					all_catch_block_num 这个数字并不一定等于
					nested + not nested 因为。。 catch 块可能有多个。
					'''
					if catch_attr.catch_exception_class != '' :
						cs_global_variable.all_catch_block_num += 1
						#print " catch block num :" , cs_global_variable.all_catch_block_num
					if catch_attr.catch_exception_class != ''  and catch_attr.throw_exception_class == '' :
						#print catch_block_obj.ori_code
						cs_global_variable.all_catch_but_no_throw_num += 1
						#print " all_catch_but_no_throw_num " , cs_global_variable.all_catch_but_no_throw_num
					if True:
						if catch_attr.catch_exception_class != '' and catch_attr.throw_exception_class != '' :
							str_x = "1"
							if catch_attr.catch_exception_class == catch_attr.throw_exception_class:
								str_x = "0"
							line_num = str( catch_block_obj.ori_begin_line_num )
							str_p = ''
							if catch_attr.throw_init_parameters != '' :
								str_p = catch_attr.throw_init_parameters
							#return_content +=   java_file_name + '\t,\t' +obj.func_name + '\t,\t' + catch_attr.catch_exception_class + '\t,\t' + catch_attr.throw_exception_class + "\t,\t" + line_num + "\t,\t" + str_x + "\t,\t" + str_p  + '\n' 
							#cs_global_variable.all_throw_new_num += 1
							#return_content +=  str( cs_global_variable.all_throw_new_num ) + ",\t" +  str_p  + '\n' 
							if False:
								'''
								throw new 没有包含 catch exception 
								'''
								if   catch_attr.is_use_ori_excp_msg :
									cs_global_variable.all_throw_excp_no_use_ori_msg += 1
									tmp_i = cs_global_variable.all_throw_excp_no_use_ori_msg
									return_content += java_file_name + '\n' + str( tmp_i) + "\t" + catch_attr.throw_init_parameters + '\n'
							if False:
								para_str=''
								para_num_value = str( catch_attr.throw_init_para_num )
								if catch_attr.throw_init_para_num < 3 :
									for str_tmp in catch_attr.throw_init_para_list:
										str_tmp=str_tmp.strip()
										para_str += '\t<' + str_tmp  + '>'
								return_content +=  catch_attr.throw_init_paras_md5 + ","+  str( cs_global_variable.all_throw_new_num ) + ",\t" +  str_p  + "\t" + para_num_value + "==" + para_str +  '\n' 
							if False:
								para_str=''
								para_num_value = str( catch_attr.throw_init_para_num )
								if catch_attr.throw_init_para_num >= 3:
									cs_global_variable.all_throw_init_params_eq_gt_3 += 1
									for str_tmp in catch_attr.throw_init_para_list:
										str_tmp=str_tmp.strip()
										print str_tmp
										para_str += '\t<' + str_tmp  + '>'
									return_content +=  str( cs_global_variable.all_throw_new_num ) + ",\t" +  str_p  + "\t" + para_num_value + "==" + para_str +  '\n' 
							if True:
								'''
								打印 ori_throw_new_line 本身
								'''
								para_str=''
								para_num_value = str( catch_attr.throw_init_para_num )
								if catch_attr.throw_init_para_num >= 3:
									cs_global_variable.all_throw_init_params_eq_gt_3 += 1
								print catch_attr.ori_throw_new_line
					#print catch_block_obj.ori_code
	#print "job finished."
	return "\r\n"+return_content
		
		

if True:
	'''
	打印所有的 exception 和 throw new exception
	'''
	LOG_FILENAME = '/home/es_catch_exceptions.log'	
	logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)
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
					#
					#print "path" + file
				for filename in filenames:
					file = os.path.join(dirname, filename)
					# 只能是源文件，允许替换的文件，此处要验证
					if file.endswith( ".java" ) and file.find("AmazonEC2Stub.java") <= 0: 
						#total_class_num += 1
						#content = "src:" + file + "\r\n"
						content = get_catch_exception( file )
						#print "nest=",cs_global_variable.all_throw_nested_trycatch
						#print "not nest",cs_global_variable.all_throw_not_nested_trycatch
						
						if len( content ) > 10:
							logging.debug( content )
		else:
			print parser.usage
	num=0
	for class_str in all_unique_throw_new_class_dict:
		print num,class_str
		num += 1
	print " Throw new init para big than 3 num is : " , cs_global_variable.all_throw_init_params_eq_gt_3 
	sys.exit(0)

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
'''
						if catch_attr.is_wrapped:
							#print "-----wrapped------"
							#print catch_block_obj.ori_code
							#print "-----wrapped end ------"
							#continue
							pass
						if catch_attr.is_nest_catch_block:
							#print "----- nested ------"
							#print catch_block_obj.ori_code
							#print "----- nested end ------"
							#continue
							pass
						if catch_attr.is_complex_block:
							#print "----- complex -------"
							#print catch_block_obj.ori_code
							#print "----- complex end -------"
							#continue
							pass
						if catch_attr.is_have_throw_new:
							#print "----- throw_new -------"
							#print catch_block_obj.ori_code
							#print "----- throw_new end -------"
							pass
						if catch_attr.catch_exception_class != '':
							#print "----- exception begin -------"
							#print "catch exception class is :", catch_attr.catch_exception_class
							#print "----- end -------"
							pass
						if catch_attr.throw_exception_class != '':
							#print "----- throw new exception begin -------"
							#print "catch throw new exception class is :", catch_attr.catch_exception_class
							#print "----- end -------"
							pass
'''

