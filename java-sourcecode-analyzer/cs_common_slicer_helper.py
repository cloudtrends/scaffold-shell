#! /usr/bin/python
#coding: utf-8
#filename cs_common_slicer_helper.py

import os
import os
import os.path
import datetime
import sys
import string
import time
import re
from inspect import currentframe, getframeinfo


reload(sys) 
sys.setdefaultencoding('utf8')

from cs_exception_common import * 
from cs_common_clz import *


class OneFineInitPart:
    def __init__(self):
        self.ori_part = ''
        self.new_part = ''
        self.is_plus_part = ''









class JavaFunctionThrowNewFormatter:
    '''
    把一个 func obj 中的 throw new 代码折行变成一行
    在代码替换 和 生成eme 配置文件的时候使用
    '''
    def __init__( self , func_obj ):
        self.func_obj = func_obj
        self.format_code_list = []
        self.cr_lf = "\n"
    def format( self ):
        #print "begin format throw new line"
        self.format_code_list = []
        is_throw_combine_begin = False
        tmp_combine_line = ''
        prefix = ''
        for line in self.func_obj.ori_code_list:
            if SSW( line , "throw " ) \
                    and not SEW( line , ";" ) \
                    and line.find( " new " )> 0 \
                    and not is_throw_combine_begin:
                is_throw_combine_begin = True
                prefix = get_throw_new_line_prefix_str( line )
                line = line.strip()
                self.format_code_list.append( prefix + self.cr_lf );
                tmp_combine_line = prefix + line 
                continue
            if SEW( line , ";" ) and is_throw_combine_begin:
                is_throw_combine_begin = False
                line = line.strip()
                tmp_combine_line += line + self.cr_lf
                
                self.format_code_list.append( tmp_combine_line )
                #print "throw new line:",tmp_combine_line
                tmp_combine_line    = ''
                continue
            if is_throw_combine_begin:
                line = line.strip()
                tmp_combine_line += line 
                self.format_code_list.append( prefix + self.cr_lf );
                continue
            self.format_code_list.append( line )
        return self.format_code_list
            
            

class BlockWrapperHelper:
    '''
    有注释的多行合并不支持
    只支持常用的语法
    '''
    def __init__( self , code_list ):
        self.ori_code_list = code_list
        self.new_code_list = []
        self.cr_lf = "\n"
        pass
    def add_new_line( self , line ):
        self.new_code_list.append( line )
    def combine_wrap_line( self ):
        is_wrap_line = False
        is_comments_begin = False
        curr_wrap_line = ''
        for line in self.ori_code_list:
            if SSW( line , "//"):
                self.add_new_line( line )
                continue
            int_l = line.find( "/*" )
            int_r = line.find( "*/" )
            if int_l >= 0 and int_r > int_l :
                remain_line = line[ :int_l ] + line[ int_r + 2 : ]
                remain_line = remain_line.strip()
                if 0 == len( remain_line ):
                    self.add_new_line( line )
                    continue
                else:
                    line = remain_line
                    # continue process ... 
            int_s = line.find( "//" )
            if int_s > 0:
                left_line = line[ : int_s ].strip()
                if 0 == len( left_line ):
                    self.add_new_line( line )
                    continue
                else:
                    line = left_line
                    # continue process ...
            if SSW( line , "/*" ) and not is_comments_begin:
                is_comments_begin = True
                self.add_new_line( line )
                continue
            if is_comments_begin and not SEW( line , "*/" ):
                self.add_new_line( line )
                continue
            if is_comments_begin and SEW( line , "*/" ):
                is_comments_begin = False
                self.add_new_line( line )
                continue
            if not is_wrap_line and SEW( line , ";" ):
                self.add_new_line( line )
                continue
            if not is_wrap_line and not SEW( line , ";" ) \
                    and not SEW( line , "{" ):
                is_wrap_line = True
                line = line.strip()
                curr_wrap_line = ''
                curr_wrap_line += line
                self.add_new_line( self.cr_lf )
                continue
            if is_wrap_line and ( SEW( line , ";" ) or SEW( line , "{") ):
                line = line.strip()
                curr_wrap_line += line + self.cr_lf
                self.add_new_line( curr_wrap_line )
                curr_wrap_line= ''
                is_wrap_line = False
                continue
            if is_wrap_line :
                line = line.strip()
                curr_wrap_line += line
                continue
            self.add_new_line( line )
        pass
        
        
        
        
        

class OneLineThrowNewSignCompare:
    '''
    比较源代码中，和 对应关系表中的 throw 签名是否一致
    
    参数个数，exception 类名称，参数值（只比较引号内的），加号分割后的，或者 e.getmessage 等
    
    如果相等，那么就替换。
    
    对比内容：
    1、去掉 comments
    2、throw new 的 exception 类
    3、throw new exception 类的 参数数量
    4、参数严格对比， string , ex.getMessage 等。
    '''
    pass
    
class ExtractThrowNewLineToList:
    '''
    get throw new line , if word wrap line  combine it first.
    
    ignore throw new line when after no braces if,else statement 
    '''
    def __init__( self , func_obj ):
        self.throw_new_list = []
        self.func_obj = func_obj
        self.throw_formatter    = JavaFunctionThrowNewFormatter( func_obj )
        pass
    def extract( self ):
        format_code_list = self.throw_formatter.format()
        pre_line = ''
        for line in self.func_obj.ori_code_list:
            #要严格匹配，忽略 comments
            #ignore new obj in throw new line
            #line = removeJavaCommentsInLine( line )
            if isJavaThrowNewLine( line ):
                if  isNewObjInThrowNewLine( line ):
                    pre_line = line
                    continue
                if SCOMPARE( pre_line , "else" ) :
                    pre_line = line
                    continue
                if SSW( pre_line, "if" ) and SEW( pre_line,")" ):
                    pre_line = line
                    continue
                if SSW( pre_line , "}" ) and SEW( pre_line, "else" ):
                    pre_line = line
                    continue
                if SEW( pre_line , ")" ) and ( not SSW( pre_line , "if" )  ) :
                    pre_line = line
                    continue
                self.throw_new_list.append( line )
            pre_line = line
        return self.throw_new_list
    

class ExtractCatchBlocksFromTryCatchBlocks:
    '''
    从trycatch 中抽取catch块。
    为分析 catch 的 exception , exception instance name ,
            throw new Exception 类型等。
            
    不处理嵌套的try catch代码
    '''
    def __init__( self , func_blocks_obj ):
        '''
        OneJavaFuncBlocks 代表一个 function slice 后的 一个 block。 
        '''
        self.block_obj = func_blocks_obj
        self.cr_lf = func_blocks_obj.cr_lf
        self.curr_line_num = 0
        '''
        if self.block_obj.block_attr is None:
            print "extract block HAS NOT INITIALIZE ATTRIBUTE!"
            frameinfo = getframeinfo(currentframe())
            print frameinfo.filename, frameinfo.lineno
            sys.exit( 0 )
        '''
    def extract( self ):
        '''
        以 }catch(){ 开始
        以} 或者 }catch(){结束
        '''
        if not self.block_obj.block_type == "try_catch" :
            print "function block is not try catch block"
            frameinfo = getframeinfo(currentframe())
            print frameinfo.filename, frameinfo.lineno
            sys.exit( 0 )
        '''
        if self.block_obj.block_attr.is_nest_try_block :
            print "function block is NESTED try catch block"
            frameinfo = getframeinfo(currentframe())
            print frameinfo.filename, frameinfo.lineno
            sys.exit( 0 )
        if self.block_obj.block_attr.is_wrapped :
            print "function block is WRAPPED try catch block"
            frameinfo = getframeinfo(currentframe())
            print frameinfo.filename, frameinfo.lineno
            sys.exit( 0 )            
        if self.block_obj.block_attr.is_complex_block :
            print "function block is COMPLEXED try catch block"
            frameinfo = getframeinfo(currentframe())
            print frameinfo.filename, frameinfo.lineno
            sys.exit( 0 )
        '''
        #开始提取 catch 块。
        lines = self.block_obj.ori_code.split( self.block_obj.cr_lf )
        is_catch_begin = False
        #one_catch_block_content = ''
        one_catch_block = CatchBlock()
        brace_num = 0
        self.curr_line_num = self.block_obj.ori_begin_line_num
        for line in lines:
            if not is_catch_begin and SSW( line , "}" ) \
                    and SEW( line , "{" ) \
                    and line.find( "catch" ) > 0 :
                is_catch_begin = True
                #one_catch_block_content += line + self.cr_lf
                one_catch_block.ori_code += line + self.cr_lf
                one_catch_block.ori_begin_line_num = self.curr_line_num
                continue
            if is_catch_begin and SSW( line , "}" ) \
                    and SEW( line , "{" ) and line.find("catch") > 0 :
                is_catch_begin = True
                #self.block_obj.catch_block_list.append( one_catch_block_content )
                one_catch_block.ori_end_line_num = self.curr_line_num
                self.block_obj.catch_block_list.append( one_catch_block )
                #one_catch_block_content = ''
                one_catch_block = CatchBlock()
                #one_catch_block_content += line + self.cr_lf
                one_catch_block.ori_code += line + self.cr_lf
                one_catch_block.ori_begin_line_num = self.curr_line_num
                continue
            if is_catch_begin and SSW( line , "}" ) \
                    and SEW( line , "{" ) and line.find("finally") > 0 :
                is_catch_begin = False
                one_catch_block.ori_end_line_num = self.curr_line_num
                self.block_obj.catch_block_list.append( one_catch_block )
                one_catch_block = CatchBlock()
                one_catch_block.ori_code += line + self.cr_lf
                one_catch_block.ori_begin_line_num = self.curr_line_num
                continue
            if is_catch_begin and SSW( line , "}" ) and SEW( line , "{" ) and line.find("else") > 0 :
                one_catch_block.ori_code += line + self.cr_lf
                continue
            if is_catch_begin and SEW( line , "{" ) and line.find("=") < 0 :
                '''
                String [] = {
                };  how to do deal with this?
                '''
                brace_num += 1
                #one_catch_block_content += line + self.cr_lf
                one_catch_block.ori_code += line + self.cr_lf
                continue
            if is_catch_begin and SEW(  line, "}" ) :
                if brace_num > 0 :
                    brace_num -= 1
                    #one_catch_block_content += line + self.cr_lf
                    one_catch_block.ori_code += line + self.cr_lf
                    continue
                else:
                    is_catch_begin = False
                    #one_catch_block_content += line + self.cr_lf
                    one_catch_block.ori_code += line + self.cr_lf
                    #self.block_obj.catch_block_list.append( one_catch_block_content )
                    one_catch_block.ori_end_line_num = self.curr_line_num
                    self.block_obj.catch_block_list.append( one_catch_block )
                    #one_catch_block_content = ''
                    one_catch_block = CatchBlock()
                    continue
            if is_catch_begin:
                #其他代码都加上！ 
                one_catch_block.ori_code += line + self.cr_lf
        if is_catch_begin:
            '''
            catch { 和 } 不匹配，出现严重错误
            '''
            print "extract catch block error ! NOT MATCH BRACE }"
            print self.block_obj.ori_code
            frameinfo = getframeinfo(currentframe())
            print frameinfo.filename, frameinfo.lineno
            sys.exit( 0 )
        return self.block_obj
        pass
        pass
    

class SliceFuncToTryBlocks:
    '''
    把function 格式化成 try catch 。
    '''
    def __init__( self   ):
        self.cr_lf = None # 在 convert_to_try_blocks 中初始化
        self.is_debug = False
        self.func_try_blocks_list = None
        self.func_try_blocks_list = []
        self.curr_line_num = -1
        self.curr_func_block = None
        pass
    def close_curr_block( self ):
        if self.curr_func_block is not None:
            seq_no = len( self.func_try_blocks_list )
            self.curr_func_block.seq_no = seq_no
            self.func_try_blocks_list.append( self.curr_func_block )
        self.curr_func_block = None
        self.curr_func_block = OneJavaFuncBlocks( self.cr_lf )
        # old 行号，不准确，暂不添加
        #self.curr_func_block.ori_begin_line_num = ??
        pass
    def add_ori_line( self , line):
        self.curr_func_block.add_line( line )
    def get_all_try_catch_blocks(self):
        return_list = []
        for block in self.func_try_blocks_list:
            if  'try_catch' != block.block_type :
                continue
            return_list.append( block )
        return return_list
    def convert_to_try_blocks( self , obj , split_by  ) :
        self.cr_lf = split_by
        #print "mmmmmmmmmmmmmmmmmmmmmm"
        #print obj.ori_code
        #print "uuuuuuuuuuuuuuuuuuuuuu"
        lines = obj.ori_code.split( self.cr_lf )
        self.curr_line_num = 0
        self.curr_func_block = OneJavaFuncBlocks( self.cr_lf  )
        self.curr_line_num = obj.ori_begin_line_num
        self.block_type = ''
        #if obj.func_name == 'initialize':
        #    print obj.ori_code
        #print obj.func_name
        is_try_block = False
        try_block_num = -1 # {} 配对计数器
        is_comments_start = False
        for ori_line in lines :
            #print "ori code \t" ,ori_line
            self.curr_line_num += 1
            #这里 curr_line_num 已经不是1了
            if False and 1 == self.curr_line_num :
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
                if visual_cr_lf is None:
                    #print ">",ori_line,"<"
                    pass
                #print "Block Default CRLF is : ", visual_cr_lf
                #print ori_line
            ori_line += self.cr_lf
            line = ori_line
            
            if SSW( line , "//" ):
                continue
            int_l = line.find( "/*" )
            int_r = line.find( "*/" )
            if int_l >= 0 and int_r > int_l:
                line = line[:int_l] + line[int_r + 2 :]
            if SSW( line , "/*") and not is_comments_start :
                is_comments_start=True
                continue
            if SEW( line , "*/") and is_comments_start:
                is_comments_start=False
                continue
            if is_comments_start :
                continue
            int_s = line.find("//")
            if int_s > 0:
                #print "--<<<",line
                line = line[:int_s] + self.cr_lf
                #tcf
                #try catch 这一层的源代码可以随意修改注释
                ori_line = line
                #print "-->//>",line
            if is_try_block :
                '''
                难点在于如何判断  try 结束 计算 {} 配对
                有两种情况结束： 多个catch 后结束，或者finally后结束
                } 开头 { 结尾， 中间为 cache
                } 开头 ｛ 结尾 中间为  finally
                
                如果 碰到 finaly 后只有一行就歇菜
                '''
                if SEW( line , "{" ) and not SSW( line , "}" ):
                    try_block_num += 1
                    self.add_ori_line( ori_line )
                    continue
                if SEW( line , "{" ) and  SSW( line , "}" ) :
                    if line.find( "catch" ) > 0 :
                        self.curr_func_block.catch_num += 1
                    if line.find( "finally" ) > 0:
                        self.curr_func_block.is_have_finally = True
                    self.add_ori_line( ori_line )                
                    continue
                if SSW( line , "}" )  :
                    if  SEW( line , "{" ) : 
                        if line.find( "catch" ) > 0 :
                            self.curr_func_block.catch_num += 1
                        if line.find( "finally" ) > 0:
                            self.curr_func_block.is_have_finally = True
                        self.add_ori_line( ori_line )
                    else:
                        try_block_num -= 1
                        if 0 == try_block_num :
                            self.add_ori_line( ori_line )
                            self.curr_func_block.ori_end_line_num = self.curr_line_num
                            self.close_curr_block()
                            is_try_block = False
                            continue
                        self.add_ori_line( ori_line )
                else:
                    self.add_ori_line( ori_line )
            else:
                if SSW( line , "try" ) and SEW( line , "{"  ) \
                        and not is_try_block:
                    self.close_curr_block()
                    self.curr_func_block.ori_begin_line_num  = self.curr_line_num
                    self.curr_func_block.block_type = "try_catch"
                    #print "find new try block:",ori_line
                    self.add_ori_line( ori_line )
                    is_try_block = True
                    try_block_num = 1
                else:
                    self.add_ori_line( ori_line )
                    pass
            
            pass
        self.close_curr_block()
        self.curr_func_block = None
        # 判断是否 nested try_catch_block
        list_return_new = []
        for obj in self.func_try_blocks_list:
            if obj.block_type == 'try_catch':
                if self.check_is_nested_try_catch( obj ):
                    obj.is_nested_try_catch = True
                #print "----------------------------"
                #print obj.ori_code
            list_return_new.append( obj )
        self.func_try_blocks_list = None
        self.func_try_blocks_list = list_return_new
        
        #print "eeeeeeeeeeeeee------------eeeeeee"
        return self.func_try_blocks_list
        pass
    def check_is_nested_try_catch( self , func_block ):
        if self.cr_lf is None:
            print "cr_lf is NONE"
            sys.exit(0)
        lines = func_block.ori_code.split( self.cr_lf )
        try_num = 0
        is_nestes_try_catch = False
        #print "b   b    b     b"
        for line in lines:
            if SSW( line , "try" ) and SEW( line , "{" ):
                try_num += 1
                #print line
        #print "e   e    e    e    e"
        if try_num > 1:
            is_nestes_try_catch = True
        return is_nestes_try_catch


