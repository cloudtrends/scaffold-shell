#! /usr/bin/python
#coding: utf-8
#filename cs_formal_generate_eme.py

'''
这个文件的作用是，按照project，生成一份配置文件
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


LOG_FILENAME = '/home/es_formal_generate_eme.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)


'''
生成供翻译人员用的配置文件

目前只涉及 CloudStack 的Exception类
'''

uniq_not_allowed_class={}
if "__main__" == __name__ :
    usage = "usage: %prog [options] arg1 arg2  "
    parser = OptionParser(usage=usage)    
    parser.add_option("-P" , "--package",default="default" ,  dest="package" , type="string")
    parser.add_option("-V" , "--version",default="default" ,  dest="version" , type="string")
    parser.add_option("-D" , "--debug",default="default" ,  dest="debug" , type="string")    
    # the need replace java source code in a plain text file
    # used only for appending exception mode replacement when developing....
    parser.add_option("-F" , "--infile",default="default" ,  dest="infile" , type="string")    
    
    (options, args) = parser.parse_args()
    if "default" == options.package  or "default" == options.version :
        print parser.usage
        sys.exit( 0 )
        pass
    debug_mode = False
    if "yes" == options.debug   :
        debug_mode=True
    if options.package not in config_allow_package:
        print "package not int allow process list :" , options.package
        print parser.usage
        sys.exit( 0 )
        pass
    
    if not isVersionNumValid( options.version ):
        print "Version num is not valid"
        sys.exit(0)
    javafile_allowed_list=[] # only used for replace exceptions in files
    if "default" == options.infile:
        pass
    else:
        pass
        if not os.path.exists( options.infile ):
            print " infile must be absolutly path and exists ."
            print options.infile
            sys.exit()
        myfile = open( options.infile )
        javafile_allowed_list = [ line.strip() for line in myfile]
        for one_file in javafile_allowed_list:
            print one_file
    cher = ConfigHelper()
    ver_dir = cher.get_ver_dir( options.version )
    if os.path.exists( ver_dir ):
        print "Target dir  exist." 
    else:
        print "Create new EME generate dir :" ,
        os.makedirs( ver_dir )
        print "Success create new version dir , " ,  ver_dir
    #tcf 要写入的文件名
    #print "Must check md5 duplicated case!"
    #print "Must check md5 duplicated case!"
    #print "Must check md5 duplicated case!"
    ver_eme_config_file = cher.get_eme_config_filename( options.version, options.package ) 
    if debug_mode:
        ver_eme_config_file += ".debug"
    wfile = file( ver_eme_config_file,"w")
    #
    start_path = config_cs_dir + os.sep + options.package
    skip_file_list = config_skip_file_list
    skip_path_list = config_skip_path_list
    valid_throw_num = 0
    java_file_num = 0
    
    for file_name in getNextFile( start_path ):
        if not SEW( file_name , "java" ):
            continue
        java_file_num += 1
        sys.stdout.write("Java File Num %i  in package %s \r" % (java_file_num , options.package) )
        sys.stdout.flush()
    print "\n"
    print "Begin generate eme config file ... "
    java_file_num=0
    javafile_allowed_list_all = ",".join( javafile_allowed_list )
    for file_name in getNextJavaSourceFile( start_path , skip_file_list , skip_path_list  , config_only_allow_file_list ):
        java_file_num += 1
        if len( javafile_allowed_list ) > 0:
            java_basename = os.path.basename( file_name )
            if java_basename not in javafile_allowed_list_all:
                continue
        ojscm = OneJavaSourceCodeManager( file_name , None )
        ojscm.is_debug = True
        ojscm.parser()
        split_by = ojscm.slicer.cr_lf
        func_list = ojscm.get_all_funcname_obj_list()
        logging_line = file_name + "\n"
        for obj in func_list:
            throw_getter = ExtractThrowNewLineToList( obj )
            throw_new_list = throw_getter.extract( )
            tmp_is_func_have_throw = False
            logging_line_func = "func name:\t" + obj.func_name  + "\n"
            for line in throw_new_list:
                valid_throw_num += 1
                logging_line_func += "\t\t\t\t"+line + "\n"
                tmp_is_func_have_throw = True
                throw_new_class = getThrowNewExceptionClass( line )
                #判断是否允许的 class
                #更严格的判断是：判断import，防止重复的exception类名。
                allow_exception_list = cher.get_allow_exception_list(options.version,options.package )
                if throw_new_class not in allow_exception_list:
                    #print "Pass not registered throw new exception class. "
                    #print line
                    if uniq_not_allowed_class.get( throw_new_class ) is None:
                        uniq_not_allowed_class[ throw_new_class ] = throw_new_class
                    continue
                tmp_init_paras = getThrowInitParameters( line )
                tmp_fine_init_paras = removeThrowNewInitParaSpace( tmp_init_paras )
                tmp_fine_init_paras=tmp_fine_init_paras.strip()
                if 0 == len( tmp_fine_init_paras ):
                    continue
                
                fip_md5 = getJavaThrowNewLineMd5( line )
                #print fip_md5
                line = line.strip()
                wfile.write( "UUID=" + get_md5( obj.func_paras_md5 + fip_md5 ) +"\n" )
                wfile.write( "PAKG=" + file_name.replace( config_cs_dir+os.sep , "" ) + config_eme_line_spliter +obj.func_name + config_eme_line_spliter + obj.func_paras_md5 +"\n")
                wfile.write( "FROM="+line +  config_eme_line_spliter +  fip_md5  +  config_eme_line_spliter  +throw_new_class+"\n" )
                wfile.write( "T  O="+line + "\n" )
                if debug_mode:
                    init_paras = getThrowInitParameters( line )
                    tmp_para_list=getThrowNewInitParaList( init_paras )                        
                    for one_para in tmp_para_list:
                        wfile.write( "PARA="+ one_para + "\n" )
                    wfile.write("FINE="+fine_init_paras+"\n")
                wfile.write( "\n" )
            if tmp_is_func_have_throw:
                logging_line += logging_line_func
        logging.debug(logging_line)
    wfile.close()
    #check md5 duplicate in one or cross file?
    #just warning
    if debug_mode:
        sys.exit(0)
    cher = ConfigHelper()
    eme_list = cher.load_eme_list( options.version , options.package )
    print "eme list count :" , len( eme_list )
    for not_allow_class in uniq_not_allowed_class:
        print not_allow_class
    eme_dict={}
    num_tmp = 0
    for eme in eme_list:
        if eme_dict.get( eme.func_md5 ) is None:
            #print num_tmp
            eme_dict[ eme.func_md5 ] = eme
            #print "find new md5" , eme.func_md5
        else:
            #print num_tmp
            #print "duplicate md5 " , eme.func_md5 , ":", eme.file_name , ",",eme.func_name
            #print "\t\t\t",eme_dict.get( eme.func_md5 ).file_name
            pass
        num_tmp += 1
    print "total java files:" ,java_file_num
    print "Total valid_throw_num = ",valid_throw_num        
    #print "一共有多少个，重复的多少个"
    


    
    
    
'''
tcf
下面的代码，依赖于 catch 块的分析。暂时不使用这个方法。
            if True:
                continue
            func_try_blocks = SliceFuncToTryBlocks()
            func_try_blocks.convert_to_try_blocks( obj , split_by )
            try_catch_blocks = func_try_blocks.get_all_try_catch_blocks()
            for block in try_catch_blocks:
                catch_blocks_extractor = ExtractCatchBlocksFromTryCatchBlocks( block )
                new_block = catch_blocks_extractor.extract()                
                for catch_block_obj in new_block.catch_block_list:
                    catch_attr_analyzer = CatchAttrAnalyzer( catch_block_obj , split_by )
                    catch_attr = catch_attr_analyzer.analysis()
                    #如果没有 throw new 则继续
                    if not catch_attr.is_have_throw_new:
                        continue
                    throw_line = catch_attr.ori_throw_new_line
                    throw_line=throw_line.strip()
                    if 1 > len( throw_line ):
                        continue
                    #print "-    -    -    -    -    -    -"
                    #print throw_line
                    #package\src\com\...\XXXX.java;function name ;function paras md5
                    wfile.write( "UUID=" + get_md5( obj.func_paras_md5 + catch_attr.throw_init_paras_md5 ) +"\n" )
                    wfile.write( "PAKG=" + file_name.replace( config_cs_dir+os.sep , "" ) + "##"+obj.func_name +"##" + obj.func_paras_md5 +"\n")
                    wfile.write( "FROM="+throw_line +  "##"+  catch_attr.throw_init_paras_md5  +"\n" )
                    wfile.write( "T  O="+throw_line + "\n" )
                    wfile.write( "\n" )
                    valid_throw_num += 1
                    #print "e    e    e    e    e    e    e    e"
                    #md5_class = catch_attr.throw_init_paras_md5
                    break


'''