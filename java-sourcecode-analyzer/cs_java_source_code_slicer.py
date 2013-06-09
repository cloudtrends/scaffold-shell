#! /usr/bin/python
#coding: utf-8
#filename cs_java_source_code_slicer.py

import os
import os
import os.path
import datetime
import sys
import string
import time
import re
import md5



reload(sys) 
sys.setdefaultencoding('utf8')




from cs_exception_common import * 

from cs_common_clz import *

class SliceJavaSourceToPieceList:
	'''
	OneJavaSourceCodePiece
	把java源代码，原封不动的Slice成Piece，因为以后要合并。
	
	要想获取正确的Slice ，需要先把原来的代码理解后，按照正常的函数分开，并记录行号
	然后按照行号，来进行保存。
	最后就是一份 line number 列表，据此来进行 slice 
	
	'''
	def __init__(self , file_name , file_list_content ):	
		self.init_basic( file_name )
		if file_list_content is None:
			self.__init_by_filename( file_name , None )
		else:
			self.init_by_cache( file_list_content )
		pass
	def init_basic(self , file_name ):
		self.cr_lf = None
		self.is_debug = False
		self.is_func_begin = False # for add wrap function line support
		self.is_combine_line = False	### wrap 
		self.combine_line_tmp = ''   	### wrap
		self.combine_line_tmp_ori_list = []
		self.combine_line_tmp_modify_list = []
		self.func_num=0
		self.func_exception_num=0
		self.func_catch_num=0
		self.func_throw_num=0
		self.code_piece_list = []
		self.curr_code_piece = None
		self.curr_line_num = -1		
		self.file_name = file_name
		self.file_path = os.path.abspath( self.file_name )
		self.base_file_name = os.path.basename( self.file_name )		
	def init_by_cache( self , file_list_content ):
		if file_list_content is not None:
			self.content_list = file_list_content
	def __init_by_filename(self  , file_name , file_list_content):
		'''
		解决文件重复打开添加的
		'''
		if file_list_content is None:
			f = open( self.file_name ,"r")
			self.content_list = []
			for line in f.readlines():
				self.content_list.append( line )
				#print line
			f.close()		
	def add_combine_modify_line( self , line ):
		self.combine_line_tmp_modify_list.append( line )
	def add_combine_ori_line( self , line ):
		self.combine_line_tmp_ori_list.append( line )
	def add_modified_line( self ,line ):
		#
		#
		self.curr_code_piece.add_line(line)
	def add_ori_line( self ,line ):
		#
		#
		self.curr_code_piece.add_line_ori(line)
	
	def close_curr_piece( self   ):
		'''
		要为  curr_code_piece 提供 seq_no
		'''
		if self.curr_code_piece is not None:
			seq_no = len( self.code_piece_list )
			self.curr_code_piece.seq_no = seq_no
			self.code_piece_list.append( self.curr_code_piece )
		self.curr_code_piece = None
		self.curr_code_piece = OneJavaSourceCodePiece (  )
		self.curr_code_piece.ori_begin_line_num = self.curr_line_num
		pass		
	def report(self):
		report_str = "new class\r\n"
		report_str += "path:" + self.file_path + "\r\n"
		report_str += "name:" + self.base_file_name + "\r\n"
		report_str += "\t\t" + "function num:" + str(  self.func_num ) + "\r\n"
		report_str += "\t\t" + "exception function num:" + str(self.func_exception_num) + "\r\n"
		report_str += "\t\t" + "catch function num:" + str(self.func_catch_num) + "\r\n"
		report_str += "\t\t" + "throw new function num:" + str(self.func_throw_num) + "\r\n"
		report_str += "\t\t" + "" + "" + "\r\n"
		#print report_str
		logging.debug( report_str )
	def parser_to_pieces(self):
		'''
		暂时不考虑 function 嵌入class的情况
		只针对function这个级别进行处理！
		默认function有限定符:public,private,protected
		类有：package,libaries,begin_class,fields,function,nest_class等
			#说明：
			#如果是多行，且其中有一行是注释，目前不支持这种情况。
			#只支持，是多行，但是空行的情况		
		'''
		#if self.is_debug:
		#	print "Enter func parser_to_pieces"
		is_comments_begin=False
		is_clz_begin = False
		self.is_func_begin=False
		self.curr_code_piece = None
		num = 0
		sub_block_num = 0
		self.is_combine_line = False
		self.combine_line_tmp = ''
		self.curr_line_num=0
		#以下代码是首次初始化，因此不用 close curr piece 初始化
		self.curr_code_piece = OneJavaSourceCodePiece (  ) # 默认就开始了
		self.curr_code_piece.piece_type = 'declare' #默认是 declare  部分
		self.curr_code_piece.ori_begin_line_num = self.curr_line_num
		for ori_line in self.content_list :
			if not self.is_combine_line :
				self.combine_line_tmp = ''
				self.combine_line_tmp_ori_list = []
				self.combine_line_tmp_modify_list = []
			self.curr_line_num += 1  # slice by line number ，以1为第一行的行数
			if 1 == self.curr_line_num:
				visual_cr_lf=None
				if ori_line.endswith( "\r\n" ):
					self.cr_lf = "\r\n"
					visual_cr_lf = "\\r\\n"
				if ori_line.endswith( "\n" ):
					self.cr_lf = "\n"
					visual_cr_lf = "\\n"
				if ori_line.endswith( "\r" ):
					print " NOT POSSIBLE ENDSWITH \R "
					sys.exit( 0 )
				#print "Default CRLF is : ", visual_cr_lf
			'''
			怎么把分开的两行或者多行，合并成一行呢？
			主要针对函数声明
			'''
			#print "O:",ori_line
			num += 1
			line = ori_line
			if not self.is_combine_line and is_empty_line( line , self.cr_lf ): #有 空格tab的空行
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				continue
			#说明：
			#如果是多行，且其中有一行是注释，目前不支持这种情况。
			#只支持，是多行，但是空行的情况
			if SSW( line , "//"):
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				continue
			else:
				# remove all follow with //
				int_slash = line.find("//")
				if int_slash > 0:
					#下面2行，暂时不替换，不能破坏源代码
					line = line[:int_slash] #戒掉了回车
					line = repair_cr_lf( line , self.cr_lf )
					#print " MAY BE ERROR IN NEXT PROCESSING "
					pass
			'''
			case:
			private int _waitTime = 5; /*wait for 5 minutes*/
			'''
			if line.find( "/*" ) > 0 and line.find("*/") > 0 :
				line = line[ 0 : line.find("/*") ] + line[line.find("*/") + 2:]
				if self.is_debug:
					pass
					#print "remove /** */",line
			if SSW( line, "/*" ) and is_comments_begin == False:
				'''
				如果已经进入函数，那么就不应该 close curr
				'''
				is_comments_begin = True
				if not is_clz_begin and not self.is_func_begin:
					self.close_curr_piece()
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				continue
			if SEW( line , "*/" ) and is_comments_begin == True:
				is_comments_begin = False
				self.add_modified_line( line )
				self.add_ori_line( ori_line )
				if not is_clz_begin and not self.is_func_begin:
					self.close_curr_piece()
				continue
			if is_comments_begin :
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				continue
			if SSW( line ,"package" ) and SEW( line , ";"):
				self.close_curr_piece()
				self.curr_code_piece.ori_begin_line_num = self.curr_line_num 
				self.curr_code_piece.piece_type='package'
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				continue
			if SSW( line ,"import" ) and SEW( line , ";"):
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				continue
			# add 3 or more line support but not tested.
			# special case : public variables
			if SEW( line , ";" ) and ( SSW( line ,"public " ) \
							or SSW( line , "private ") \
							or SSW( line , "protected " ) \
						):
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				continue
			if SEW( line , ";" ) and not self.is_combine_line:
				'''
				以;结尾，并且不是 combine line 
				针对这种情况的处理：
				String abc=
					"  bla bla ";
				'''
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				continue		
			if not self.is_combine_line and not SEW( line , "{" ):
				#print "----------------------------\r\n"
				if  not SEW( line , ";" ) \
						and ( SSW( line ,"public " ) \
							or SSW( line , "private ") \
							or SSW( line , "protected " ) \
						 
						) \
						and not SEW( line , "}" ) :  
					#print "begin combine :",line
					line = line.replace("\r\n","")
					line = line.replace("\n","")
					self.is_combine_line = True
					self.combine_line_tmp = line
					## for line num equal against to ori
					#DON'T DELETE
					#self.add_ori_line( ori_line )			#DON'T DELETE
					#self.add_modified_line( self.cr_lf )	#DON'T DELETE
					##DON'T DELETE
					self.add_combine_ori_line( ori_line )
					self.add_combine_modify_line( self.cr_lf )
					continue
			if self.is_combine_line and SEW( line , ";" ):
				'''
				2012-06-04 add for class level muliti line 
				public String abc=
					"  bla bla ";
				
				'''
				line = line.replace("\r\n","")
				line = line.replace("\n","")
				self.combine_line_tmp += line #+ "\r\n"
				self.is_combine_line = False
				self.combine_line_tmp = repair_cr_lf( self.combine_line_tmp  , self.cr_lf )
				#DON'T DELETE
				#self.add_ori_line( ori_line )
				#self.add_modified_line( self.combine_line_tmp )
				#
				self.add_combine_ori_line( ori_line )
				self.add_combine_modify_line( self.combine_line_tmp )
				for ori_combine_tmp_line in self.combine_line_tmp_ori_list :
					self.add_ori_line( ori_combine_tmp_line )
				for modify_combine_tmp_line in self.combine_line_tmp_modify_list:
					self.add_modified_line( modify_combine_tmp_line )
				continue
			# 考虑3行的情况
			if self.is_combine_line and not SEW(  line , "{" ):
				#DON'T DELETE
				#self.add_ori_line( ori_line )
				#self.add_modified_line( self.cr_lf )
				#
				self.add_combine_ori_line( ori_line )
				self.add_combine_modify_line( self.cr_lf )
				# and empty for line number equal
				line = line.replace("\r\n","")
				line = line.replace("\n","")
				self.combine_line_tmp += line
				continue
			if self.is_combine_line and SEW( line , "{" ):	
				line = line.replace("\r\n","")
				line = line.replace("\n","")
				self.combine_line_tmp += line #+ "\r\n"
				self.is_combine_line = False
				line = self.combine_line_tmp
				line = repair_cr_lf( line  , self.cr_lf )
				#self.add_ori_line( ori_line )
				#self.add_modified_line( line )
				
				#if self.is_debug:
				#	print "self.combine_line_tmp:" , line
				#	pass
				# continue process ...
				'''
				is a function or not ?
				tmp combine line block choice ?
				'''
				if SEW( line , "{" ) and \
						( SSW( line,"public " ) \
							or SSW( line,"private " ) \
							or SSW( line,"protected " ) ):
					int_l = line.find( "(" )
					int_r = line.find( ")" ) 
					if int_l >0 and int_r > int_l :
						# for support wrap func begin line
						# if new func find , add combine tmp lines to current piece
						self.close_curr_piece(   )
						self.add_combine_ori_line( ori_line )
						self.add_combine_modify_line( line )						
						for ori_combine_tmp_line in self.combine_line_tmp_ori_list :
							self.add_ori_line( ori_combine_tmp_line )
						for modify_combine_tmp_line in self.combine_line_tmp_modify_list:
							self.add_modified_line( modify_combine_tmp_line )
						is_close_curr_piece = False
						self.anslysis_func_begin_line( line ,ori_line , is_close_curr_piece )
						continue
					else:					
						for ori_combine_tmp_line in self.combine_line_tmp_ori_list :
							self.add_ori_line( ori_combine_tmp_line )
						for modify_combine_tmp_line in self.combine_line_tmp_modify_list:
							self.add_modified_line( modify_combine_tmp_line )						
			if SSW( line, "}" ) and SEW( line, "{" ):
				'''
				} else { 特殊处理
				'''
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				continue
			if SEW( line , "{" ):
				#print "line endswith {" , line
				if line.find( "class" ) >= 0 \
					and line.find( "(" )< 0 \
					and line.find( ")" )< 0 \
					and is_clz_begin == False:  # 第二次发现的类不管？
					is_clz_begin = True
					self.close_curr_piece(   ) #旧的模块结束了
					self.add_ori_line( ori_line )
					self.add_modified_line( line )
					self.curr_code_piece.ori_begin_line_num = self.curr_line_num 
					self.curr_code_piece.piece_type='class'
					continue
				#else:
				#	'''
				#	class abc
				#	'''
				#	print "impossible!"
				#	print line
				#	sys.exit(0)
				#	pass
			if SEW( line , "{" ):
				if self.is_func_begin :
					sub_block_num += 1
					self.add_ori_line( ori_line )
					self.add_modified_line( line )
					continue
			if SEW( line , "{" ) and \
					( SSW( line,"public " ) \
						or SSW( line,"private " ) \
						or SSW( line,"protected " ) ):
				int_l = line.find( "(" )
				int_r = line.find( ")" ) 
				if int_l >0 and int_r > int_l :
					# for support wrap func begin line
					is_close_curr_piece = True
					self.anslysis_func_begin_line( line ,ori_line , is_close_curr_piece)
					continue
				else:
					'''
					function a
					{
					}
					function a()
						throws exception {
					这样的写法
					可以先不处理，但要做一个特殊的计数。
					防止这种情况的发生 。
					
					如果要处理，需要回溯到以前的行，找到function声明的行
					
					'''
					#print " ERROR : occur the multi-line function declare ." 
					#sys.exit(0)
					self.add_ori_line( ori_line )
					self.add_modified_line( line )
					continue
					pass
			if sub_block_num > 0:
				pass
			if SCOMPARE( line , "}" ) and self.is_func_begin == False and sub_block_num == 0 :
				is_clz_begin= False
				
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				self.close_curr_piece(   ) #旧的模块结束了
				continue
			#做的更严格一点
			if SCOMPARE( line, "}" ) and self.is_func_begin == True:
			#if SSW( line, "}" ) and self.is_func_begin == True:
				if sub_block_num > 0:
					sub_block_num -= 1
					self.add_ori_line( ori_line )
					self.add_modified_line( line )
					continue
				else:
					self.is_func_begin = False
					self.curr_code_piece.ori_end_line_num = self.curr_line_num 
					self.add_ori_line( ori_line )
					self.add_modified_line( line )
					self.close_curr_piece(  ) #旧的模块结束了
					continue
			#deal with }		
			if is_clz_begin and self.is_func_begin and self.curr_code_piece is not None :
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				continue
			if is_clz_begin :
				'''
				处理 annotation 这类在 函数前，类后的数据
				'''
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				continue				
			if not is_clz_begin : 
				#类结束了，后面的空行。。等
				self.add_ori_line( ori_line )
				self.add_modified_line( line )
				continue
				#print line
		#print "end"		
		#print " code pieces num :" , len( self.code_piece_list )
		self.close_curr_piece(  )  
		self.curr_code_piece = None
		for cp in self.code_piece_list:
			pass
			#print "###   ###   ###   ###   "
			#print cp.ori_code
		pass
	def analysis_wrap_line( self , line , ori_line ):
		pass
	def anslysis_func_begin_line( self , line , ori_line , is_close_curr_piece ):
		if is_close_curr_piece:
			self.close_curr_piece(   ) #旧的模块结束了
			self.add_ori_line( ori_line )
			self.add_modified_line( line )			
		else:
			pass
		#if self.is_debug:
		#	print "find new func ... "
		self.is_func_begin = True
		self.curr_code_piece.ori_begin_line_num = self.curr_line_num 
		self.curr_code_piece.piece_type='function'
		self.curr_code_piece.func_name = self.parser_func_name( line )
		self.curr_code_piece.func_paras_str = self.parser_func_paras_str( line )
		self.curr_code_piece.func_paras_num = self.parser_func_paras_num( self.curr_code_piece.func_paras_str )
		self.curr_code_piece.func_paras_list = self.parser_func_paras_list( self.curr_code_piece.func_paras_str )
		self.curr_code_piece.func_paras_str= ''
		for one_item in self.curr_code_piece.func_paras_list:
			self.curr_code_piece.func_paras_str += one_item + ","
		len_str_tmp = len( self.curr_code_piece.func_paras_str )
		len_str_tmp -= 1
		self.curr_code_piece.func_paras_str = self.curr_code_piece.func_paras_str[ : len_str_tmp ]
		'''
		通过 2 个md5来确定一个替换对象，另一个是 throw new 的 init para md5
		用这2个 md5 生成最终的 md5 即 uuid
		
		func 的md5 = md5( funcname + init para str )
		'''
		md5_src_str = self.curr_code_piece.func_name + self.curr_code_piece.func_paras_str
		self.curr_code_piece.func_paras_md5 = self.get_func_paras_md5( md5_src_str )
		if self.is_debug:
			pass
			#print "occur new func name:" , self.curr_code_piece.func_name	
		pass
	def parser_to_function_list( self , file_name):
		pass
	def get_func_paras_md5( self , line ) :
		m = md5.new()
		m.update( line )
		return m.hexdigest()
	def parser_func_paras_list( self , line ):
		list_para = []
		one_string = ''
		lt_find = False
		gt_find = False
		for c in line:
			if "," == c and not lt_find and not gt_find :
				ont_string = MSTOO( one_string )
				list_para.append( one_string )
				one_string=''
				continue
			if '<'  == c:
				lt_find = True
			if '>' == c:
				gt_find = True
			if lt_find and gt_find:
				lt_find = False
				gt_find = False
			one_string += c
		one_string = MSTOO( one_string )
		list_para.append( one_string )
		return list_para
	def parser_func_paras_num( self , line ):
		para_num = 0
		line = line.strip()
		in_loop = False
		lt_find = False
		gt_find = False
		minus_num = 0
		for c in line:
			if '<'  == c:
				lt_find = True
			if '>' == c:
				gt_find = True
			if lt_find and gt_find:
				minus_num += 1
				gt_find = False
				lt_find = False
			if not in_loop:
				in_loop = True
			if ',' == c:
				para_num += 1
		if not in_loop :
			para_num = 0
		if in_loop:
			para_num += 1
		para_num -= minus_num
		return para_num
		pass
	def parser_func_paras_str( self , line ):
		'''
		func_paras_str
		参数可能为空
		'''
		new_line = line
		#return new_line
		
		func_paras_str = ''
		int_s = new_line.find( "/*" )
		int_e = new_line.find( "*/" )
		if int_s >= 0 and int_e > int_s :
			new_line = new_line[ :int_s ] + new_line[ int_e + 2 : ]
		int_b = new_line.find( "//" )
		if int_b > 0:
			new_line = new_line[:int_b]
		int_l = new_line.find( "(" )
		int_r = new_line.find( ")" )
		if int_l > 0 and int_r > int_l:
			new_line = new_line[int_l + 1 : int_r ]
		func_paras_str = new_line
		if func_paras_str.find( "\"" ) >= 0:
			print " func paras content quota"
			sys.exit( 1 )
		return func_paras_str 
		pass
	def parser_func_name( self , line ):
		'''
		 提取方法名称
		 传入的参数行，如果是折行的，要经过合并行
		'''
		#print "Enter func parser func name "
		#if self.is_debug:
		#	print "Enter func parser_func_name: " , line
		int_a = line.find( "(" );
		if int_a > 0:
			line = line[ : int_a ]
		line = MSTOO( line )
		lines = line.split(' ')
		func_name = lines[ len(lines) - 1 ]
		#if self.is_debug :
		#	print "\t\t",func_name
		return func_name.strip()
	pass

	
	
	
	