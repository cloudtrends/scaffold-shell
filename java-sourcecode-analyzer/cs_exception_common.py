#! /usr/bin/python
#coding: utf-8
#filename cs_exception_common.py 


import os
import os.path
import datetime
import sys
import string
import time
import re
import md5
from random import randint

#from cs_formal_config             import *


reload(sys) 
sys.setdefaultencoding('utf8')


#DO NOT CHANGE reference generate eme properties python file.
SPLITER_PARA = "_#_"
SPLITER_INNER = "_@_"


def getRand( max ):
    return randint(1, max) 

def isVersionNumValid( ver_num ):
    return True

def get_md5(   line ):
    m = md5.new()
    m.update( line )
    return m.hexdigest()

    

def isJavaFileAllowed( file_name):
    pass

def isNewObjInThrowNewLine( line ):
    init_paras = getThrowInitParameters( line )
    tmp_para_list=getThrowNewInitParaList( init_paras )
    find_new_in_throw=False
    for one_para in tmp_para_list:
        if SSW( one_para , "new " ):
            find_new_in_throw=True
            break
    return find_new_in_throw
    
def getNextJavaSourceFile( start_path , skip_file_list , skip_path_list , only_allow_file_list = None ):
    for file in getNextFile( start_path ):
        if file.endswith( ".java" ):
            find_path = False
            for tmp_line in skip_path_list:
                '''
                这里是简化处理，对比 文件名中是否包含 
                '''
                if file.find( os.sep+tmp_line+os.sep ) >0 :
                    find_path = True
                    break
            if find_path:
                continue
            if only_allow_file_list is not None:
                is_allow=False
                for allow_line in only_allow_file_list:
                    if allow_line in file :
                        is_allow= True
                        break
                if not is_allow:
                    continue
            for skip_file in skip_file_list:
                if skip_file in file:
                    continue
            yield file
            '''
            allow_file = False
            if only_allow_file_list is not None and not allow_file:
                for allow_line in only_allow_file_list:
                    if file.find( allow_line ) >= 0:
                        allow_file = True
                        break
            else:
                find_skip_file = False
                for skip_file in skip_file_list:
                    if file.find( skip_file ):
                        find_skip_file = True
                        break
                if find_skip_file:
                    continue
                else:
                    allow_file = True
            if allow_file:
                yield file
            '''
            '''
            if only_allow_file_list is None:
                for line in skip_file_list:
                    if not file.find( line ) >=0 :
                        yield file
            else:
                for allow_line in only_allow_file_list:
                    #print "allow_line:",allow_line
                    if file.find( "Virtual" ) >=0 :
                        print file
                    if file.find( allow_line ) >= 0:
                        print "Debug Mode for few files."
                        yield file
            '''
            
def getNextJavaFile( start_path ):
    for file in getNextFile( start_path ):
        if SEW( file, ".java" ):
            yield file
def getNextFile( start_path  ):
    for dirname, dirnames, filenames in os.walk( start_path ):
        for subdirname in dirnames:
            pass
            #file = os.path.join(dirname, subdirname)
            #
            #print "path" + file
        for filename in filenames:
            file = os.path.join(dirname, filename)
            yield file
    
def MSTOO( line ):
    '''
    merge space to one
    '''
    line = line.strip()
    max_num = 10
    allow_repeat = True
    for i in range( max_num )  :
        if   allow_repeat:
            line = line.replace( "  " , " " )
            line = line.replace( "\t" , " " )
            if i == 9 and line.find( ' ' ) > 0:
                allow_repeat = True
            else:
                allow_repeat = False
    return line

def ReadFileToString( file_name ):
    '''
    '''
    contents =''
    f_list = ReadFileToList( file_name )
    for line in f_list:
        contents += line
    return contents
def ReadFileToList( file_name  ):
    f = open( file_name ,"r")
    ori_list = []
    for line in f.readlines():
        ori_list.append( line )
    f.close()
    return ori_list
def appendOneLine( file , line ):
    f = open( file , "a" )
    f.write( line )
    f.close
def RemoveBlockComments( block_code , split_by ):
    lines = block_code.split( split_by )
    return_content = ''
    is_commons_begin = False
    for line in lines:
        if SSW( line , "//" ):
            continue
        int_slash = line.find( "//" )
        if int_slash > 0:
            line = line[:int_slash]
        if SSW( line , "/*" ) and SEW( line , "*/" ) :
            continue
        int_a = line.find( "/*" ) 
        int_b = line.find( "*/" )
        if int_a > 0 and int_b > 0 and int_b > int_a :
            line = line[:int_a] + line[int_b + 2 :]
        if SSW( line , "/*" ) and not is_commons_begin :
            is_commons_begin = True
            continue
        int_e = line.find( "/*" ) # 不在开头
        if int_e > 0 and not is_commons_begin:
            line = line[:int_e]
            is_commons_begin = True
            #continue
        if SEW( line , "*/" ) and is_commons_begin :
            is_commons_begin = False
            continue
        int_d = line.find( "*/" )
        if is_commons_begin and int_d >= 0 :
            line = line[ int_d + 2: ]
            is_commons_begin = False
        if is_commons_begin:
            continue
        return_content += line + split_by
    return return_content
            

def SCOMPARE( line , com_str ):
    n = line.strip()
    if n == com_str:
        return True
    else:
        return False
        
def SSW( line , startswith_str ):
    '''
    strip startswith ssw
    '''
    line = line.strip()
    if line.startswith( startswith_str ):
        return True
    else:
        return False
def SEW( line , endswith_str ):
    '''
    '''
    line = line.strip()
    if line.endswith( endswith_str ):
        return True
    else:
        return False

def repair_cr_lf( line , cr_lf ):
    '''
    if cr_lf is \n
    and lind end with : \r\n ? how to ....?
    '''
    if not line.endswith( cr_lf ):
        line = line + cr_lf
    return line

def is_empty_line( line , cr_lf ):
    line = line.strip()
    for c in line:
        if not c == ' ' and not c == '\t' and not c == cr_lf :
            return False
    return True

    
def get_grammer_line( line ):
    '''
    获取符合语法的line ，去掉行内的注释、最后的注释 等
    '''
    pass

def is_comments_in_line( line ):
    '''
    判断 line 里有 // 或者 /**  */
    '''
    if SSW( line , "//" ):
        print "is_comments_in_line ERROR " , line 
        sys.exit(0)
    if SSW( line , "/**" ):
        print "is_comments_in_line ERROR " , line 
        sys.exit(0)
    if line.find("//") > 0 :
        return True
    int_a = line.find( "/*" )
    int_b = lind.find( " */" )
    if int_a > 0 and int_b > 0 and int_b > int_a :
        return True
    return False
    

def removeJavaCommentsInLine( line ):
    line = line.strip()
    if SSW( line , "//" ):
        line = ''
    int_l = line.find( "/*" )
    int_r = line.find( "*/" )
    if int_l >= 0 and int_r > int_l:
        line = line[:int_l] + line[int_r + 2:]
    int_l = -1
    int_l = line.find( "//" )
    if int_l > 0:
        line = line[: int_l]
    return line
    

def getThrowNewExceptionClass( line ):
    int_t = line.find( "throw" )
    int_r = line.find( " new " )
    int_b = line.find( "(" )
    return_str = ''
    if int_t >=0 and int_r > int_t and int_b > int_r:
        return_str = line[int_r+5 : int_b]
    return return_str.strip()
    
def retriveThrowInitParameters( line ):
    '''
    this function is a reverse way find ,used for find md5 , in replaced exception msg
    such as:
    ConfigurationException _ex_=(ConfigurationException) ESECreater.create("ConfigurationException","_B_Unable to find the ipassoc.sh_E_");throw _ex_;
    '''
    if not line.endswith( ";throw _ex_;" ):
        print "the input line not valid, not endswith ;throw _ex_; "
        sys.exit(1)
    find_str1="ESECreater.create("
    find_str2="ESEBCreater.create("
    find_str3=");throw _ex_;"
    
    if find_str1 not in line and find_str2 not in line :
        print "the input line not valid , cause : ",find_str1  ," or ",find_str2," not find ."
        sys.exit(1)
    offset = len( find_str1 )
    find_pos=line.find( find_str1 )
    if find_pos < 0 :
        offset = len( find_str2 )
        find_pos = line.find( find_str2 )
    new_line = line[ find_pos + offset : line.find( find_str3 ) ]
    new_line = new_line[ new_line.find( "\"," ) + 2 : ]
    new_line = new_line.replace( "_B_","" )
    new_line = new_line.replace("_E_","" )
    print new_line
    return new_line
    
    pass    
def getThrowInitParameters( line ):
    '''
    the input line is starts with throw new and ends with ;
    '''
    if not SSW( line , "throw " ) or line.find(" new ") < 0  or not SEW( line , ";" ):
        print "comm func get throw init para : throw para is not valid ."
        sys.exit(1)
        return None
    int_t = line.find( "throw" )
    int_n = line.find( "new" )
    int_l = line.find( "(" )
    line_reverse = line[::-1]
    int_r = line_reverse.find( ")" )
    #误区：int_r = len( line ) - int_r  翻转后，从0开始
    int_r = len( line ) - int_r - 1
    str_a = None
    if int_t >= 0 and int_n > int_t and int_l > int_n and int_r > int_l:
        str_a = line[ int_l + 1 : int_r ]
    #if str_a is not None:
    #    str_a = removeThrowNewInitParaSpace( str_a )
    #    para_list = getThrowNewInitParaList( str_a )
    #    str_a = refineThrowNewInitParameters( str_a , para_list  )
    return str_a
    

    
def removeThrowNewInitParaSpace( line ):
    '''
    去掉 throw new exception 中 init  参数的空格
    
    如果里面有 new 的话？
    tcf
    '''
    line=line.strip()
    new_line = ''
    pre_char = ''
    is_brace_begin = False
    for c in line:
        if "\"" == c and pre_char == "\\":
            new_line += c
            pre_char = c
            continue
        if "\"" == c  and not is_brace_begin:
            is_brace_begin = True
            new_line += c
            pre_char = c
            continue
        if "\"" == c and is_brace_begin:
            is_brace_begin = False
            new_line += c
            pre_char = c
            continue
        if " " == c and not is_brace_begin:
            pre_char = c
            continue
        new_line += c
        pre_char = c
    return new_line    
    
def refineThrowNewInitParameters( ori_parameters , para_list ):
    if None == ori_parameters:
        print "comm func :  ori_parameters is none"
        return None
    new_line = ''
    for one_item in para_list :
        one_item = removeThrowNewInitParaSpace( one_item )
        new_line += one_item + ","
    len_tmp = len( ori_parameters )
    new_line = new_line[ : len_tmp - 1 ]
    return new_line
    
def generateDynamicThrowNewParas( line ):
    pass
    #for para in para_list:
    pass    
    pass

    
def getThrowNewInitParaList( line ):
    '''
    把throw new 初始化参数格式化成列表，便于以后计算md5
    '''
    if None == line:
        print "comm func input line is None "
        return None
    line = line.strip()
    para_list = []
    if 0 == len( line ) :
        return para_list
    is_quota_begin = False
    pre_char = ""
    one_para_str = ""
    is_valid_bracket_begin = False
    for c in line:
        if "("  ==  c and pre_char != "\\" and not is_quota_begin:
            is_valid_bracket_begin = True
            one_para_str += c
            pre_char = c
            continue
        if ")"  ==  c and pre_char != "\\" and not is_quota_begin:
            is_valid_bracket_begin = False
            one_para_str += c
            pre_char = c
            continue            
        if "\"" == c and pre_char != "\\" and not is_quota_begin:
            is_quota_begin=True
            one_para_str += c
            pre_char = c
            continue
        if "\"" == c and pre_char != "\\" and  is_quota_begin:
            is_quota_begin = False
            one_para_str += c
            pre_char = c
            continue
        if "," == c :
            if  is_valid_bracket_begin:
                one_para_str += c
                pre_char = c
                continue
            if not  is_quota_begin :
                para_list.append( one_para_str )
                one_para_str = ''
                # add to list and strip
                pre_char = c
                continue
            else:
                one_para_str += c
                pre_char = c
            continue                    
        else:
            one_para_str += c
            pre_char = c
            continue
    para_list.append( one_para_str )
    return para_list
   
def getJavaThrowNewLineMd5( line ):     
    init_paras = getThrowInitParameters( line )
    #print init_paras
    fine_init_paras = removeThrowNewInitParaSpace( init_paras )
    #print fine_init_paras
    fip_md5 = get_md5( fine_init_paras )
    return fip_md5

        
def isJavaThrowNewLine( line ):
    if  SSW(line,"throw") and SEW( line , ";" ):
        int_t = line.find( "throw" )
        int_n = line.find( " new " )
        int_l = line.find("(")
        int_r = line.find( ")" )    
        if int_t >= 0 and int_n > int_t and int_l > int_n and int_r>int_l:
            return True
    return False

    
def get_throw_new_line_prefix_str( throw_new_line ):
    '''
    '''
    max_num = 1000
    curr_num = 0
    return_line = ''
    for c in throw_new_line:
        if c == 't' and curr_num < max_num :
            break
        curr_num += 1
        return_line += c
    if curr_num > 500 :
        print "Fatal Error for get prefix str of throw new line"
        sys.exit(1)
    return return_line







def get_msg_properties_md5( fine_init_paras ):
    '''
    used when generate( update) eme message properties file.
    '''
    #check number of fine init paras should!
    para_list = getThrowNewInitParaList( fine_init_paras )
    new_para_list = []
    for one_para in para_list:
        pre_c = ''
        one_str = ''
        brace_begin=False
        for c in one_para:
            if c == '"' and pre_c != "\\" and brace_begin == False:
                if len( one_str ) > 0:
                    one_str += SPLITER_INNER
                brace_begin = True
                pre_c = c
                continue
            if c == '"' and pre_c != "\\" and brace_begin :
                brace_begin = False
                pre_c = c
                continue
            if brace_begin:
                one_str += c
                pre_c = c
                continue
            pre_c = c
        if len ( one_str ) > 0:
            new_para_list.append( one_str )
    all_str = ''
    all_str = SPLITER_PARA.join( new_para_list )
    str_md5 = get_md5( all_str )
    return str_md5


if __name__ == "__main__":
    str = "throw new CloudRuntimeException(msg);"
    md = getJavaThrowNewLineMd5( str )
    print md

'''
备份代码
        para_num = 0
        self.block_attr.throw_init_parameters=self.block_attr.throw_init_parameters.strip()
        if 0 == len( self.block_attr.throw_init_parameters ) :
            return para_num
        is_quota_begin = False
        pre_char = ""
        one_para_str = ""
        is_valid_bracket_begin = False
        for c in self.block_attr.throw_init_parameters:
            if "("  ==  c and pre_char != "\\" and not is_quota_begin:
                is_valid_bracket_begin = True
                one_para_str += c
                pre_char = c
                continue
            if ")"  ==  c and pre_char != "\\" and not is_quota_begin:
                is_valid_bracket_begin = False
                one_para_str += c
                pre_char = c
                continue            
            if "\"" == c and pre_char != "\\" and not is_quota_begin:
                is_quota_begin=True
                one_para_str += c
                pre_char = c
                continue
            if "\"" == c and pre_char != "\\" and  is_quota_begin:
                is_quota_begin = False
                one_para_str += c
                pre_char = c
                continue
            if "," == c :
                if  is_valid_bracket_begin:
                    one_para_str += c
                    pre_char = c
                    continue
                if not  is_quota_begin :
                    self.block_attr.throw_init_para_list.append( one_para_str )
                    one_para_str = ''
                    # add to list and strip
                    para_num += 1
                    pre_char = c
                    continue
                else:
                    one_para_str += c
                    pre_char = c
                continue                    
            else:
                one_para_str += c
                pre_char = c
                continue
        self.block_attr.throw_init_para_list.append( one_para_str )        
        para_num += 1
        return para_num
        pass
'''
