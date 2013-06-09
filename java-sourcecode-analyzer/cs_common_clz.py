#! /usr/bin/python
#coding: utf-8
#filename cs_common_clz.py

import os
import os
import os.path
import datetime
import sys
import string
import time
import re

reload(sys) 
sys.setdefaultencoding('utf8')



from cs_exception_common         import *

class ExceptionMapEntry:
	'''
	一个 map 条目
确保唯一性的判断：function 中的 function paras md5 和 throw new paras的 md5
替换源代码后要恢复，必须设定一个id ，可以返回来。
id md5化: package+src+com+...XXX.java+function name+funcparamd5+throw new para md5
结果格式：
UUID=id md5 ;
package\src\com\...\XXXX.java;function name ;function paras md5
FROM=throw new content;MD5 对 throw_new 内容的加密，这样防止翻译时修改错误
T  O=throw new content;	
	'''
	def __init__( self ):
		self.uuid = ''
		#file name 是以不包括 package 开头的路径和文件名 src\com ....java
		self.file_name = ''
		self.package = ''
		self.func_name = ''
		self.func_md5 = ''
		self.throw_new_content = ''
		self.throw_new_md5 = ''
		self.throw_new_class = ''
		self.new_throw_new_content = ''
	def init_from_config(self , item_list ):
		'''
		item_list 只能有4行，否则不合格
		'''
		pass
	pass
	
	
class ESFineInitParaWrapper:
    '''
    ElasterStack fine init para wrapper
    '''
    def __init__( self , line ):
        self.para_list = getThrowNewInitParaList( line )
        pass
    def get_refined_paras(self):
        new_para_all = ''
        for para in self.para_list:
            new_para = ''
            is_str_begin = False
            pre_c = ''
            for c in para:
                if '"' == c and '\\' != pre_c and not is_str_begin:
                    is_str_begin = True
                    new_para += c
                    new_para += '_B_'
                    pre_c = c
                    continue
                if '"' == c and '\\' != pre_c and is_str_begin:
                    is_str_begin = False
                    new_para += "_E_"
                    new_para += c
                    pre_c = c
                    continue
                new_para += c
                pre_c = c
            new_para_all += new_para + ","
        new_para_all = new_para_all[ : len( new_para_all )-1 ]
        return new_para_all
       

class OneJavaSourceCodePiece:
	'''
	 保存一个Slice的结果
	 多个slice可以合并成一个复原的文件，
	 line 尽可能保持和原来一样
	 但不要求
	'''
	def __init__(self  ):
		#self.file_name = file_name
		self.seq_no=-1 			#顺序号
		self.is_modified= False 	#默认不对其进行修改
		#以下提供了3中视图： 原始，格式化后，修改后
		self.new_code ='' 		#如果修改，保存修改后的代码
		self.ori_code = '' 		#原始的文档代码，包括回车等。。。
		self.format_code = ''   # 自动合并行后的code
		#
		self.new_code_list = []		# specialized for replace ONLY  DEST
		self.ori_code_list = []
		self.format_code_list = []   #  
		self.replace_code_list = [] # specialized for replace ONLY SRC
		#
		self.func_name=''
		self.func_paras_str=''  #方法括号内的参数字符串，去掉多余空格即可
		self.func_paras_num = 0 # 参数个数
		self.func_paras_list = []
		self.func_paras_md5 = '' # md5 把 func_paras_list 合并起来求md5
		self.piece_type='' 		# 类有：declare,package,libaries,begin_class,fields,function,nest_class等
		self.func_piece_list = [] #把一个function 分成多个piece
		self.ori_begin_line_num = -1
		self.ori_end_line_num = -1
	def add_line( self , line):
		self.format_code += line
		self.format_code_list.append( line )
		pass
	def add_line_ori( self, line ):
		self.ori_code+= line
		self.ori_code_list.append( line )

		
	


	


class OneJavaSourceCodePieceOriginal:
	def __init__(self  ):
		pass
		
		

class OneJavaFuncBlocks:
	'''
	代表一个 function slice 后的 一个 block。
	现在最关心这个 block 是否  try_catch 类型
	针对 function 的 blocks
	和 try catch 熟悉相关的操作，依赖于 block_type  是否try_atch
	'''
	def __init__( self , cr_lf ):
		self.cr_lf = cr_lf
		self.seq_no = -1
		self.block_type = '' #是否try_catch,
		self.is_nested_try_catch = False
		self.ori_code = ''
		self.ori_begin_line_num = -1
		self.ori_end_line_num = -1
		self.is_have_finally = False
		self.catch_num = 0
		self.catch_block_list = [] #专门存储 catch 块，可能有多个catch块
		pass
	def add_line( self , line ):
		self.ori_code += line
		
class CatchBlock:
	def __init__( self ):
		self.ori_code = ''
		self.catch_attr = None
		self.ori_begin_line_num = -1
		self.ori_end_line_num = -1		
		
	
class CatchBlockAttr:
	'''
	注意只是 catch block 的attr
	'''
	def __init__( self ):
		self.is_wrapped = False # is wrap line , not deal with warp line block
		self.is_have_finally = False 
		self.is_nest_catch_block = False
		self.is_complex_block = False
		self.is_have_throw_new = False
		self.ori_throw_new_line = ''
		self.catch_exception_class = ''
		self.catch_exception_instance = '' # 实例名 Exception e , e就是实例名
		self.throw_exception_class = ''
		self.catch_exception_paraname = '' # 这个值肯定有
		self.throw_init_parameters = '' # 比如：不包括括号 (" bla bla " + e.getMessage() + " bla bla " , e )
		self.throw_init_para_num = -1
		self.throw_init_para_list = []
		self.throw_init_paras_md5 = ''
		self.is_use_ori_excp_msg = False # 是否 catch exception 的消息 ，给 throw new 初始化了？
		#针对 "bla bla"+e.getMsg() 这种情况，怎么提取 error code
		self.throw_init_parameters_replace = ''
		#把"bla bla"+e.getMsg() 转换成：
		#"bla bla"+SChar+e.getMsg()+SChar
		#把"bla bla"+e.getMsg(),"bla bla",true 转换成：
		#"bla bla"+SChar+e.getMsg()+SChar,"bla bla",true
		#把"bla bla"+msg+"alb alb alb","bla bla",true 转换成：
		#"bla bla"+SChar+msg+SChar+"alb alb alb","bla bla",true
		pass
		
	
	
if __name__ == "__main__":
	str = "throw new CloudRuntimeException(msg);"
	init_paras = getThrowInitParameters( str )
	fine_init_paras = removeThrowNewInitParaSpace( init_paras )	
	epw = ESFineInitParaWrapper( fine_init_paras )
	wrap_fine_init_paras = epw.get_refined_paras(  )
	print wrap_fine_init_paras
	print "END"
	
	