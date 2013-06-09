#! /usr/bin/python
#coding: utf-8
#filename cs_formal_eme_trans_checker.py

'''
这个文件的作用是：
按照project，生成一份配置文件
让翻页人员帮助翻译，
翻译后的文件会生成 eme 的对象列表


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

LOG_FILENAME = '/home/es_formal_eme_trans_checker.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)


def  get_double_quote_num(line):
    num = 0
    pre_c = ''
    for c in line:
        if '"' == c and pre_c != '\\':
            num += 1
        pre_c = c  
    return num

if "__main__" == __name__ :
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
    if not isVersionNumValid( options.version ):
        print "Version num is not valid"
        sys.exit(0)
    cher = ConfigHelper()
    ver_dir = cher.get_ver_dir( options.version )
    if os.path.exists( ver_dir ):
        print "Target Dir already exist." 
    else:
        print "Create new EME generate dir :" ,
        os.makedirs( ver_dir )
        print "Success create new version dir , " ,  ver_dir
    eme_list = cher.load_eme_list( options.version , options.package )
    for eme in eme_list:
        ori_str= eme.throw_new_content
        chk_str= eme.new_throw_new_content
        #
        if isJavaThrowNewLine( ori_str ) and isJavaThrowNewLine( chk_str ):
            pass
        else:
            print "Fatal error eme TRANSLATE format NOT THROW NEW is not equal with original."
            sys.exit(1)
        ori_init_paras = getThrowInitParameters( ori_str )
        chk_init_paras = getThrowInitParameters( chk_str )
        ori_init_list = getThrowNewInitParaList( ori_init_paras )
        chk_init_list = getThrowNewInitParaList( chk_init_paras )
        if len( ori_init_list ) == len( chk_init_list ):    
            pass
        else:
            print ori_str
            print chk_str
            print "Fatal error eme TRANSLATE format LENGTH is not equal with original."
            sys.exit(1)        
        ori_cls = getThrowNewExceptionClass( ori_str )
        chk_cls = getThrowNewExceptionClass( chk_str )
        if ori_cls == chk_cls :
            pass
        else:
            print ori_str
            print chk_str
            print "Fatal error eme TRANSLATE format CLASS is not equal with original."
            sys.exit(1)
        '''
        比较翻译的文章中的静态字符串
        '''
        item_num = 0
        for item in ori_init_list:
            item = item.strip()
            #if SSW( item , '"' ):
            #    item_num += 1
            #    continue
            item_2 = chk_init_list[ item_num ].strip()
            n1 = get_double_quote_num( item )
            n2 = get_double_quote_num( item_2 )
            if n1 == n2:
                pass
            else:
                print ori_str
                print chk_str
                print item
                print item_2
                print "Fatal error eme TRANSLATE format ONE PARA is not equal with original."
                sys.exit(1)                
            item_num += 1
    print "Check Translated EME ok."
    pass
    pass
