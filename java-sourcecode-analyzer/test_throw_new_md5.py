#! /usr/bin/python
#coding: utf-8
#filename test_throw_new_md5.py

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



'''
用来验证 throw new 的 md5 是否计算正确。

验证方法：
1、 从java代码中提取throw new md5
	java 中只有一个 catch throw new  为测试
	文件名：test_md5_class.java
2、从 一行代码中提取 md5 
3、比较2次 md5 结果

python test_throw_new_md5.py -f d:\mydoc\SkyDrive\Document\python
\cloudstack-exception\test_md5_class.java -l "throw new Exception( "abc", "def" ,   , "efg" );


'''


from cs_exception_common_clz import *

from cs_try_catch_analyzer import *

if "__main__" == __name__ :
	usage = "usage: %prog [options] arg1 arg2 such as python cs_code_exception_extractor.py  -p /home/source/trunk/ "
	parser = OptionParser(usage=usage)	
	parser.add_option("-f" , "--java_file",default="default" ,  dest="java_source_file" , type="string")
	parser.add_option("-l" , "--line",default="default" ,  dest="throw_new_line" , type="string")
	(options, args) = parser.parse_args()
	if "default" == options.throw_new_line  or "default" == options.java_source_file:
		print usage
		sys.exit( 0 )
		pass
	file_name = options.java_source_file
	throw_line = options.throw_new_line
	print file_name
	md5_class = ''
	md5_one_line = ''
	ojscm = OneJavaSourceCodeManager( file_name )
	ojscm.is_debug = True
	ojscm.parser()
	func_list = ojscm.get_all_func_obj_list()
	#print " func list num: ", len(func_list)
	for obj in func_list:
		#print obj.ori_code
		#print "-	-	-	-	-	-"
		if '' == obj.func_name :
			continue
		#print obj.func_name
		func_try_blocks = SliceFuncToTryBlocks()
		split_by = ojscm.slicer.cr_lf
		func_try_blocks.convert_to_try_blocks( obj , split_by )
		for block in func_try_blocks.func_try_blocks_list:
			if  'try_catch' != block.block_type :
				continue
			catch_blocks_extractor = ExtractCatchBlocksFromTryCatchBlocks( block )
			new_block = catch_blocks_extractor.extract()
			for catch_block_obj in new_block.catch_block_list:
				catch_attr_analyzer = CatchAttrAnalyzer( catch_block_obj , split_by )
				catch_attr = catch_attr_analyzer.analysis()
				md5_class = catch_attr.throw_init_paras_md5
				break
	print "class md5 ",md5_class
	print "throw_line:",throw_line
	throw_line_para = getThrowInitParameters( throw_line )
	#print "throw_line_para:",throw_line_para
	para_list = getThrowNewInitParaList( throw_line_para )
	#重新格式化，去掉参数中多余的空格，计算md5
	throw_line_para = refineThrowNewInitParameters( throw_line_para, para_list )
	print "fefind para str:",throw_line_para
	#self.block_attr.throw_init_parameters = ''
	md5_one_line = get_md5( throw_line_para )
	print "md5_one_line",md5_one_line
	
				
		