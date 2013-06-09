#! /usr/bin/python
#coding: utf-8
#filename cs_try_catch_analyzer.py 

import os
import os.path
import datetime
import sys
import string
import time
import re
import calendar
import shutil
import md5

from optparse import OptionParser 

from cs_exception_common import * 

from cs_common_clz  import CatchBlockAttr
from inspect import currentframe, getframeinfo

reload(sys) 
sys.setdefaultencoding('utf8')


class CatchAttrAnalyzer:
	'''
	  # catch 属性分析器 ，只分析 catch 块，不分析 try 块
	
	
	分析 不带嵌套的 try catch block  代码段
	1、不嵌套 try catch				暂不处理
	2、try catch 中不包含复杂逻辑：while,  for ,if 等 代码少于10 行
									暂不处理
	3、取得 catch 的 exception 类型
	3.1 、取得 catch 的 exception 类型 的变量名称
	4、取得 catch 中是否  throw
	5、取得 catch 中是否  logger
	6、取得 catch 中 throw new 的 exception 类型
	7、取得 catch 中 throw new 中的 msg 是否包含 catch 的exception 。
	8、有finally的,					暂时处理
	9、如果try catch 中有折行的，	暂不处理
	10、 要移除 block 中的所有 comments 
	
	11、 exception 的消息是否在 throw  中用到了？
		is_use_ori_excp_msg
		
	'''
	def __init__( self , catch_block , split_by ) :
		self.split_by = split_by
		self.ori_block = RemoveBlockComments( catch_block.ori_code , split_by )
		self.block_attr = CatchBlockAttr()
		pass
	def analysis( self ) :
		self.block_attr.is_wrapped = self.check_is_wrapped()
		self.block_attr.is_have_finally = self.check_is_have_finally()
		self.block_attr.is_nest_try_block = self.check_is_nest_catch_block()
		self.block_attr.is_complex_block = self.check_is_complex_block()
		self.block_attr.is_have_throw_new = self.check_is_have_throw_new()
		self.block_attr.catch_exception_class = self.get_catch_exception_class()
		'''
		catch_exception_instance 在 get_catch_exception_class 中初始化
		'''
		#self.block_attr.catch_exception_instance = self.get_catch_exception_instance();
		if not self.block_attr.is_have_throw_new:
			pass
		else:
			self.block_attr.throw_exception_class = self.get_throw_exception_class()
			self.block_attr.catch_exception_paraname = self.get_catch_exception_paraname()
			self.block_attr.throw_init_parameters = self.get_throw_init_parameters()
			if self.block_attr.throw_init_parameters is None :
				'''
				做什么呢？
				有些 catch 中，就是没有 throw new 啊！
				'''
				print "Catch Block have no throw new , status : is_have_throw_new = ", self.block_attr.is_have_throw_new
				pass
			#以下是计算md5代码的测试
			para_list = getThrowNewInitParaList( self.block_attr.throw_init_parameters )
			if para_list is None :
				para_list = []
			self.block_attr.throw_init_para_list = para_list
			self.block_attr.throw_init_para_num = len( para_list )
			#重新格式化，去掉参数中多余的空格，计算md5
			self.block_attr.throw_init_parameters = refineThrowNewInitParameters( self.block_attr.throw_init_parameters, para_list )
			#self.block_attr.throw_init_parameters = ''
			self.block_attr.throw_init_paras_md5 = self.get_md5( self.block_attr.throw_init_parameters )
			#计算md5结束
			# 以下代码取消，暂时保留
			# 重新获得 num 两次应该一样，同时，初始化  list 中的空格
			#para_num_pre = self.block_attr.throw_init_para_num
			# 
			#self.block_attr.throw_init_para_num = self.get_throw_init_para_num()
			#if self.block_attr.throw_init_para_num != para_num_pre:
			#	print " Must Wrong cause: format space in catch analyzer . "
			#	sys.exit( 0 )
			# 也被初始化了  self.block_attr.throw_init_para_list
			self.block_attr.is_use_ori_excp_msg = self.get_is_use_ori_excp_msg()
		return self.block_attr
	def get_is_use_ori_excp_msg( self ):
		'''
		catch 的变量已经取得
		self.block_attr.catch_exception_instance 
		
		关键问题，怎么取得 throw new 的变量。
		'''
		is_use_me = False
		for one_item in self.block_attr.throw_init_para_list :
			one_items = one_item.split( "+" )
			for one_tmp in one_items:
				one_tmp = one_tmp.strip()
				if one_tmp.find( self.block_attr.catch_exception_instance + ".getMessage" ) >= 0 :
					is_use_me = True
					break
				if one_tmp.find( self.block_attr.catch_exception_instance + ".toString" ) >= 0 :
					is_use_me = True
					break
				if one_tmp == self.block_attr.catch_exception_instance:
					is_use_me = True
					break
		return is_use_me
	def get_md5( self, line ):
		m = md5.new()
		m.update( line )
		return m.hexdigest()		
	def remove_space( self , line ):
		return removeThrowNewInitParaSpace( line )
		
	def check_is_wrapped( self ):
		'''
		结尾的2中情况: { , ; 
		'''
		is_wrapped = False
		lines = self.ori_block.split( self.split_by )
		for line in lines:
			if SEW( line , "}" ):
				continue
			if is_empty_line( line , self.split_by ):
				continue
			if SEW( line , "{" ) or SEW( line , ";" ):
				continue
			else:
				is_wrapped = True
				break
		return is_wrapped
	def check_is_have_finally( self ):
		lines = self.ori_block.split( self.split_by )
		is_have_finally = False
		for line in lines:
			if line.find( "finally" ) >=0 :
				is_have_finally = True
				break
		return is_have_finally
	def check_is_nest_catch_block( self ):
		is_nest_try_block = False
		lines = self.ori_block.split( self.split_by )
		try_num = 0 
		for line in lines:
			if line.find( "try" ) > 0 :
				try_num += 1
		if try_num != 1:
			is_nest_try_block = True
		return is_nest_try_block
	def check_is_complex_block( self ):
		'''
		cache的代码少于10 行,且不能有：
		while,  for ,if 等 
		'''
		is_complex_block = False
		lines = self.ori_block.split( self.split_by )
		is_allow_check = False
		for line in lines:
			if   SEW( line , "{" ) and line.find( "catch" ) > 0  :
				is_allow_check = True
			if SSW( line , "}" ) and is_allow_check and not SEW( line , "{" ):
				is_allow_check = False
			if is_allow_check and SSW( line , "while" ) and SEW( line , "{" ):
				is_complex_block = True
				break
			if is_allow_check and SSW( line , "if" ) and SEW( line , "{" ):
				is_complex_block = True
				break
			if is_allow_check and SSW( line , "for" ) and SEW( line , "{" ):
				is_complex_block = True
				break
			pass
		return is_complex_block
	def check_is_have_throw_new( self ):
		is_have_throw_new = False
		lines = self.ori_block.split( self.split_by )
		for line in lines:
			if SSW( line , "throw" ) and SEW( line , ";" ) :
				int_a = line.find("throw")
				int_b = line.find(" new")
				if int_a >=0 and int_b >0 and int_b > int_a:
					is_have_throw_new = True
					break
		return is_have_throw_new
	def get_catch_exception_class( self ):
		class_name = ''
		lines = self.ori_block.split( self.split_by )
		for line in lines:
			if SSW( line , "}" ) and SEW( line , "{" ):
				int_l = line.find( "(" )
				int_r = line.find( ")" )
				int_e = line.find( "catch" )
				int_f = line.find("finally")
				if int_f < 0 and int_e > 0 and int_l > int_e and int_r > int_l :
					str_tmp = line[ int_l + 1 : int_r ]
					str_tmps = str_tmp.strip().split( ' ' )
					if len( str_tmps ) < 2:
						print "NOT EXIST CATCH exception class"
						frameinfo = getframeinfo(currentframe())
						print frameinfo.filename, frameinfo.lineno
						sys.exit(0)
					if len( str_tmps ) > 3:
						print "NOT EXIST CATCH exception class More Than 3. "
						frameinfo = getframeinfo(currentframe())
						print frameinfo.filename, frameinfo.lineno
						sys.exit(0)					
					class_name = str_tmps[0]
					self.block_attr.catch_exception_instance = str_tmps[1]
					if class_name == "final":
						class_name = str_tmps[1]
						self.block_attr.catch_exception_instance = str_tmps[2]
					self.block_attr.catch_exception_instance = self.block_attr.catch_exception_instance.strip()
					break
		if len( class_name ) > 0  and class_name.find( 'Exception' ) < 0 and class_name.find( "Throwable" ) < 0 \
			and class_name.find("OutOfMemoryError") < 0 \
			and class_name.find("RuntimeFault") < 0 \
			and class_name.find("BadServerResponse") < 0 \
			and class_name.find("exception") < 0 \
			and class_name.find("Invalid") < 0 \
			and class_name.find("apache") < 0 \
			and class_name.find("Fault") < 0 \
			and class_name.find("Failed") < 0 \
			and class_name.find("Types") < 0:
			print "CATCH exception class name is WRONG! :" , class_name
			print self.ori_block
			frameinfo = getframeinfo(currentframe())
			print frameinfo.filename, frameinfo.lineno
			sys.exit(0)			
		return class_name
	def get_throw_init_parameters( self ):
		'''
		一个catch block中最多只有一个throw new
		tcf 这个应该检查一下
		返回值可能为空
		'''
		init_parameters = ''
		lines = self.ori_block.split( self.split_by )
		str_a=None
		find_line = ''
		for line in lines:
			if SSW( line , "throw" ) \
					and SEW( line , ";" )\
					and line.find(" new ") > 0:
				self.block_attr.ori_throw_new_line = line
				#print "throw new line :",line
				str_a = getThrowInitParameters( line )
				#print "find result:",str_a
				break
		if None == str_a :
			print "Error : catch analyzer no init parameter. ",self.block_attr.ori_throw_new_line 
		init_parameters = str_a
		return init_parameters
	def get_catch_exception_paraname( self ):
		paraname = ''
		lines = self.ori_block.split( self.split_by )
		for line in lines:
			if SSW( line , "}" ) and SEW( line , "{" ) \
				and line.find( "catch" ) > 0 :
				int_l =  line.find( "(" )
				int_r = line.find( ")" )
				if int_l > 0 and int_r > int_l :
					str_a = line[ int_l + 1 : int_r ]
					str_a=str_a.replace( "final" , "" )
					str_a = RemoveJavaCommentsInLine( str_a )
					str_a = str_a.strip()
					str_a = MSTOO( str_a )
					strs = str_a.split( ' ' )
					if 2 != len( strs ):
						print " Catch parameters variable is not right "
						print self.ori_block
						print line
						frameinfo = getframeinfo(currentframe())
						print frameinfo.filename, frameinfo.lineno						
						sys.exit( 0 )
					paraname = strs[ 1 ]
		if '' == paraname:
			print " Catch parameters variable is not right "
			print self.ori_block
			frameinfo = getframeinfo(currentframe())
			print frameinfo.filename, frameinfo.lineno						
			sys.exit( 0 )			
		return paraname
				
	def get_throw_exception_class(self):
		class_name = ''
		lines = self.ori_block.split( self.split_by )
		if self.block_attr.is_wrapped:
			print "CATCH block is Wrapped Line . can not get throw exception class :" , class_name
			print self.ori_block
			frameinfo = getframeinfo(currentframe())
			print frameinfo.filename, frameinfo.lineno
			#sys.exit(0)
			return class_name
		for line in lines:
			if SSW( line , "throw" ) and SEW( line , ";" ):
				int_t = line.find( "throw" )
				int_n = line.find( "new" )
				int_l = line.find( "(" )
				int_r = line.find( ")" )
				if int_t >=0 and int_n > int_t and int_l > int_n and int_r > int_l :
					str_tmp = line[ int_n + 3 : int_l ]
					str_tmp = str_tmp.strip()
					class_name = str_tmp
					break
		if len( class_name ) > 0 and class_name.find( 'Exception' ) < 0 and class_name.find( "Throwable" ) < 0 \
				 and class_name.find("OutOfMemoryError") < 0  \
				 and class_name.find("RuntimeFault") < 0 \
				 and class_name.find("BadServerResponse") < 0 \
				 and class_name.find("exception") < 0 \
				 and class_name.find("Invalid") < 0 \
				 and class_name.find("apache") < 0 \
				 and class_name.find("Fault") < 0 \
				 and class_name.find("Failed") < 0 \
				 and class_name.find("Types") < 0:
			print "CATCH throw new exception class name is WRONG! :" , class_name
			frameinfo = getframeinfo(currentframe())
			print frameinfo.filename, frameinfo.lineno
			sys.exit(0)		
		return class_name
	def get_throw_init_para_num( self ):
		'''
		分析逗号个数
		歇菜了
		0,	
		BaseCmd.PARAM_ERROR,
		"Unable to execute API command "+cmd.getCommandName().substring(0,cmd.getCommandName().length()-8)+" due to invalid value. "+invEx.getMessage()	3==

		
		'''
		para_list = getThrowNewInitParaList( self.block_attr.throw_init_parameters )
		self.block_attr.throw_init_para_list = para_list
		return len( para_list )

	
	
	

