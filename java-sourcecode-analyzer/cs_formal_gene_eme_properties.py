#! /usr/bin/python
#coding: utf-8
#filename cs_formal_gene_eme_properties.py

'''
这个文件的作用是，按照 eme ，把翻页人员的eme，生成一份java properties配置文件
让翻页人员帮助翻译，
翻译后的文件会生成 eme 的对象列表



step
1. check eme file format
2. generate properties file


'''

import os
import os
import os.path
import datetime
import sys
import string
import time
import re
import logging
from collections import Counter
from optparse import OptionParser 
reload(sys) 
sys.setdefaultencoding('utf8')

from cs_exception_common import *
from cs_exception_common_clz     import *
from cs_try_catch_analyzer         import *
from cs_formal_config             import *
from cs_formal_config_helper     import *

#DO NOT CHANGE
SPLITER_PARA = "_#_"
SPLITER_INNER = "_@_"

cher = ConfigHelper()






def gene_properties( version , package):
    '''
    get ori para md5
    gene translated value
    '''
    eme_dict = cher.load_eme_dict(version,package)
    new_file_name = cher.get_eme_generate_dir( version )
    new_file_name += os.sep +package+"_" +config_eme_properties_file_name 
    print "eme properties file:",new_file_name
    f = open( new_file_name , "w" )
    for file in eme_dict:
        eme_list = eme_dict.get( file )
        for eme in eme_list:
            init_paras = getThrowInitParameters( eme.throw_new_content )
            fine_init_paras = removeThrowNewInitParaSpace( init_paras )
            str_md5 = get_msg_properties_md5( fine_init_paras )
            #print all_str
            #把 new_throw_new_content 转化为 _B__E_的格式
            str_new = get_local_throw_new( eme.new_throw_new_content )
            #debug
            #f.write( "-    -    -    "+"\n" )
            #f.write( eme.throw_new_content + "\n" )
            #f.write( all_str + "\n" )
            #debug end
            f.write( str_md5 + "=" + str_new  + "\n" )
            #把md5作为key,写入properties文件
            #难点是要拼出 string , java 中比较方便，因为就是  string类型的参数
            '''
                            这里的string 是 变量赋值前的，而java中是赋值后的.
                                把所有在 "" 内的字符串连接起来即可。
            java中，因为变量已经替换，所以需要做_B__E_的标识符号
            '''
    f.close()
    pass
def get_local_throw_new( line ):
    init_paras = getThrowInitParameters( line )
    fine_init_paras = removeThrowNewInitParaSpace( init_paras )
    epw = ESFineInitParaWrapper( fine_init_paras )
    wrap_fine_init_paras = epw.get_refined_paras(  )
    wrap_fine_init_paras=wrap_fine_init_paras.strip()
    return wrap_fine_init_paras


def get_double_quota_num( str ):
    num =0
    pre_c = ''
    for c in str:
        if c == '"' and pre_c != "\\":
            num += 1
            pass
        pre_c = c
    return num 
def check_eme( version , package):
    '''
    check from and to format
    FROM=throw new PermissionDeniedException(caller + " is disabled.");__##__e68b74628399bb3f215f097e35f7fbe1__##__PermissionDeniedException
    T  O=throw new PermissionDeniedException(caller + " is disabled.");
    '''
    eme_dict = cher.load_eme_dict(version,package)
    for file in eme_dict:
        #print file
        eme_list = eme_dict.get( file )
        if eme_list is None:
            print "File eme not found:",file
            sys.exit(1)
        for eme in eme_list:
            #print eme.throw_new_content
            #print eme.new_throw_new_content
            if not isJavaThrowNewLine( eme.throw_new_content ) \
                    or not isJavaThrowNewLine( eme.new_throw_new_content ):
                print "check eme error not throw new line:", eme.uuid
                print eme.throw_new_content
                sys.exit(1)
            ori_para = getThrowInitParameters( eme.throw_new_content )
            new_para = getThrowInitParameters( eme.new_throw_new_content )
            
            #if ori_para == new_para:
            #    print ori_para
            #else:
            #    print "check eme error"
            #    print eme.new_throw_new_content
            #    print eme.throw_new_content
            #    sys.exit(1)
            ori_para_list = getThrowNewInitParaList( ori_para )
            new_para_list = getThrowNewInitParaList( new_para )
            
            if len( ori_para_list ) != len(new_para_list ):
                print "check eme error , para list number not equal .", eme.uuid
                print eme.throw_new_content
                sys.exit(1)
            p_len = len( ori_para_list )
            #print p_len
            for i in range( 0 , p_len ):
                ori_str = ori_para_list[i].strip()
                new_str = new_para_list[i].strip()
                o_n = get_double_quota_num( ori_str )
                n_n = get_double_quota_num( new_str )
                if o_n != n_n:
                    print "check eme error quota not equal ,",eme.uuid
                    print eme.new_throw_new_content
                    print eme.throw_new_content
                    sys.exit(1)
                #if ori_str != new_str:
                #    print "check eme error,",eme.uuid
                #    print ori_str
                #    print new_str
                #    sys.exit(1)
                oc= ori_str[0:1]
                nc = new_str[0:1]
                #print oc,"=",nc
                #if oc == "B":
                #    print eme.new_throw_new_content
                if oc != nc:
                    print "check eme error, para not equal .",eme.uuid
                    print eme.throw_new_content
                    print eme.new_throw_new_content
                    sys.exit(1)
                pass
    pass


'''
功能：根据 eme config file 生成 properties file
'''
if __name__ == "__main__":
    usage = "usage: %prog [options] arg1 arg2  "
    parser = OptionParser(usage=usage)    
    parser.add_option("-P" , "--package",default="default" ,  dest="package" , type="string")
    parser.add_option("-V" , "--version",default="default" ,  dest="version" , type="string")
    (options, args) = parser.parse_args()
    if "default" == options.package  or "default" == options.version :
        print parser.usage
        sys.exit( 0 )
        pass
    if options.package not in config_allow_package:
        print "package not int allow process list :" , options.package
        print parser.usage
        sys.exit( 0 )
        pass
    print "check eme"
    check_eme( options.version , options.package )
    print "gene eme"
    gene_properties( options.version , options.package )
    
