#! /usr/bin/python
#coding: utf-8
#filename cs_exception_common_clz.py 


import os
import os.path
import datetime
import sys
import string
import time
import re
from itertools import ifilter
import logging

reload(sys) 
sys.setdefaultencoding('utf8')


from cs_java_source_code_slicer import *
from cs_common_slicer_helper  import *

class OneJavaSourceCodeManager:
	def __init__( self , file_name , file_content_list ):
		self.is_debug = False
		self.file_name = file_name
		self.slicer = SliceJavaSourceToPieceList( file_name , file_content_list )
		self.func_to_try_blocks_slicer = SliceFuncToTryBlocks()
		pass
	def parser(self):
		self.slicer.is_debug = self.is_debug
		self.slicer.parser_to_pieces()
		#self.print_exception_funcs()
		#self.slicer.report()
		#print " total number :" + str( self.slicer.func_num )
	def get_obj_by_funcname_and_md5( self, func_name , md5_str ):
		func_list = self.get_all_obj_by_func_name( func_name )
		for one_obj in func_list:
			if one_obj.func_name == func_name:
				if one_obj.func_paras_md5 == md5_str:
					return one_obj
		return None
	def get_all_obj_by_func_name( self , func_name ):
		'''
		为了防止函数有重载的情况，因此用这个来做
		'''
		obj_list = []
		for obj in self.slicer.code_piece_list :
			if obj.piece_type == "function":
				if obj.func_name == func_name :
					obj_list.append( obj )
		return obj_list
	def get_package_func_obj( self ):
		#for obj in self.slicer.code_piece_list :
		#	if obj.piece_type == "package":
		for obj in ifilter(lambda obj: obj.piece_type == "package" , self.slicer.code_piece_list):
			return obj
	def get_one_piece_obj_by_func_name( self , func_name ):
		'''
		根据方法名，返回方法 obj 
		重名的方法怎么办？
		根据参数？ 太复杂了吧？ 
		根据参数个数？ 目前这块还没解析！
		强制要求方法名以 public ,private , protected 的才算
		'''
		for obj in self.slicer.code_piece_list :
			if obj.piece_type == "function":
				if obj.func_name == func_name :
					return obj
		return None
	def update_one_piece_obj_by_seq_no( self , obj ):
		del self.slicer.code_piece_list[ obj.seq_no ]
		self.slicer.code_piece_list.insert( obj.seq_no , obj )
		pass
	def get_all_ori_code( self ):
		pass
	def get_all_new_code( self ):
		pass
	def get_all_func_name_list( self ):
		'''
		验证 Slicer解析的是否正确。
		最好能结合 ast 一起做，这样更严格。
		
		'''
		obj_list = []
		for obj in self.slicer.code_piece_list :
			if obj.piece_type == "function":
				obj_list.append( obj )
		return obj_list
	def get_all_func_try_pieces( self ):
		'''
		获得类中所有function中带有 try 的 block 。
		'''
		funcs_list = self.get_all_func_obj_list()
		for obj in func_list:
			'''
			把ori_code转成 try blocks
			'''
			if '' == obj.ori_code :
				print "ERROR not initialized before call "
				sys.exit(0)
			blocks_list = self.func_to_try_blocks_slicer.convert_to_try_blocks( obj )
			for block in blocks_list:
				if block.block_type == 'try_catch':
					print block.ori_code
			pass
		pass
	def get_all_func_obj_list( self ):
		return self.slicer.code_piece_list
	def get_all_funcname_obj_list( self ):
		'''
		 获取所有有方法名的 obj list
		'''
		return_list = []
		for obj in self.slicer.code_piece_list:
			if '' == obj.func_name :
				continue
			return_list.append( obj )
		return return_list
	def get_all_exception_func_obj_list( self ):
		return_list = []
		for obj in self.slicer.code_piece_list :
			if obj.piece_type == "function":
				if obj.ori_code.find( "exception" ) > 0 :
					return_list.append( obj )
				pass
		return return_list
		
	def save_ori_file(self , dest_dir ):
		'''
		
		
		f = open( self.file_name+".ori.java" , "w" )
		for obj in self.slicer.code_piece_list:
			lines = obj.ori_code.split(  "\r\n" )
			for line in lines:
				f.write( line )
		f.close()
		'''
		#ori_code_list
		pass
	def save_format_file(self):
		f = open( self.file_name+".format.java" , "w" )
		for obj in self.slicer.code_piece_list:
			lines = obj.format_code.split(  "\r\n" )
			for line in lines:
				f.write( line )
		f.close()	
	def save_changed_file( self  , file_full_name ):
		f = open( file_full_name , "w" )
		for obj in self.slicer.code_piece_list:
			if obj.is_modified:
				lines = obj.new_code_list
			else:
				lines = obj.ori_code_list
			for line in lines:
				f.write( line )
		f.close()		
	pass
	def print_exception_funcs( self ):
		'''
		output format: exception , func name , file
		'''
		for obj in self.slicer.code_piece_list:
			if obj.piece_type == "function":
				#print obj.func_name
				self.slicer.func_num += 1
				code_lines = obj.ori_code.split("\r\n")
				for line in code_lines:
					if line.find("Exception")>0:
						#print "#   #   #   #   #   #   #   #   #   #   #   #   "
						#print obj.func_name
						if line.find( obj.func_name ) >0 :
							pass
							pass
						else:
							self.slicer.func_exception_num += 1
							if line.startswith("throw new"):
								self.func_throw_num += 1
								print line
								pass
							elif line.find("catch") >0 :
								self.slicer.func_catch_num += 1
								#print line
								pass
							elif line.find("logger") >0 :
								pass
							else:
								pass
								#print line
		pass
		
		
		
		

	


class JavaClassAnalyzer:
	def __init__( self , file_name ):
		self.file_name = file_name
		pass
	def get_all_functions(self    ):
		jstfl = JavaSourceToFunctionList()
		func_list = fstfl.parser_to_function_list( source_file_name )
		pass
	def get_all_functions_with_exception():
		'''
		获得所有包含Exception的方法
		'''
		list_funcs = self.get_all_functions()
		for one_func in list_funcs:
			# judge if exception include
			pass
	pass
	
	
	
if __name__ == "__main__":
	file_name = "D:\java\workspaces\core\src\com\cloud\agent\resource\virtualnetwork\VirtualRoutingResource.java"
	file_name = './test/VirtualRoutingResource.java'
	ojscm = OneJavaSourceCodeManager( file_name , None )
	ojscm.parser()
	obj = ojscm.get_package_func_obj()
	print obj.ori_code