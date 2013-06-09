#!/usr/bin/python
#coding: utf-8
#filename cs_formal_rollback.py



import os
import os.path
import datetime
import sys
import string
import time
import re
import logging
import shutil
import traceback
from optparse import OptionParser 

from cs_exception_common         import *
from cs_formal_config             import *
from cs_formal_config_helper    import *
from cs_try_catch_analyzer        import *
from file_comp_lbl                import *
reload(sys) 
sys.setdefaultencoding('utf8')






class CloudStackExceptionRollback(   ):
    '''
    steps 
    1. read eme list to file
    2. for each file find replace piece  
        //DO NOT CHANGE ID:XXX
        //END
    3. replace to original throw new statement
    4. over.
    '''
    def __init__(self , version_num , package_name  ):
        self.version_num         =    version_num
        self.package        = package_name 
        self.cher = ConfigHelper()
        self.eme_list = self.cher.load_eme_list( version_num , package_name )
        self.eme_dict = self.cher.load_eme_dict( version_num , package_name )
        self.backup_dir        = self.cher.get_source_backup_dir( version_num  )  + os.sep + self.package  + "_rollback"      #指定默认的备份文件夹
        pass
    def start_rollback(self):
        for eme in self.get_next_eme():
            try:
                if not self.rollback( eme ):
                    print "Rollback error, re rollback now ..."
                    self.rollback_and_exit()
            except Exception as e:
                print "-"*30
                print e
                traceback.print_exc(file=sys.stdout)
                self.rollback_and_exit()

    def rollback(self , eme):
        '''
        
        '''
        print "="*40
        func_obj = self.curr_ojscm.get_obj_by_funcname_and_md5( eme.func_name  , eme.func_md5 )
        if func_obj is None:
            print "Fatal Error function  not match eme in source code ."
            self.rollback_and_exit()
        print "func name:", func_obj.func_name
        new_code_list = []
        is_find_ESECreater = False
        allow_replace = True # the same signiture in one func obj , keep sequence replace
        need_replace_line_list = []
        if func_obj.is_modified:
            need_replace_line_list = func_obj.new_code_list
        else:
            need_replace_line_list = func_obj.ori_code_list
        line_num_in_func = 0
        block_begin= False
        one_block_list=[]
        one_block_md5=''
        DONOTCHANGE="//DO NOT CHANGE ID:"
        prefix_str=''
        print "func line num:" , len( need_replace_line_list )
        for line in need_replace_line_list:
            line_num_in_func += 1
            #print line_num_in_func
            #
            # find ESECreater and replace
            #
            if SSW( line , DONOTCHANGE  ) and block_begin:
                print "ESECreater block not valid.  "
                self.rollback_and_exit()                
            if SSW( line , DONOTCHANGE  ):
                block_begin = True
                one_block_list=[]
                one_block_list.append( line )
                len_pre = len( DONOTCHANGE )
                int_b = line.find( DONOTCHANGE )
                prefix_str = line[ : int_b ]
                #print len_pre 
                one_block_md5=line[ len_pre + int_b : ].strip()
                continue
            if SSW( line , "//__END" ) and block_begin :
                block_begin = False
                one_block_list.append( line )
                #print one_block_md5,"===",eme.throw_new_md5
                if one_block_md5 == eme.throw_new_md5 and allow_replace:
                    allow_replace = False
                    is_find_ESECreater = True
                    new_code_list.append( prefix_str + eme.throw_new_content + self.curr_ojscm.slicer.cr_lf )
                else:
                    for tmp_line in one_block_list:
                        new_code_list.append( tmp_line )
                continue
            if SSW( line , "//__END" ) and not block_begin:
                print "ESECreater block not valid.  "
                self.rollback_and_exit()
            if block_begin :
                one_block_list.append( line )
                continue
            
            
            new_code_list.append( line )
            
                
            
        if not is_find_ESECreater:
            print "Fatal error rollback block not find in source code ."
            print eme.file_name
            print eme.func_name
            print eme.throw_new_content
            print "eme uuid:", eme.uuid
            print "\tStart auto re rollback... "
            self.rollback_and_exit()
        func_obj.is_modified = True
        func_obj.new_code_list = new_code_list
        print "new code list len:" , len( new_code_list )
        self.curr_ojscm.update_one_piece_obj_by_seq_no( func_obj )                        
        return True
    def get_next_eme(self):
        for source_name in self.eme_dict:
            print "source file :" , source_name
            find_skip = False
            for skip_line in config_skip_file_list:
                if skip_line in source_name:
                    print "skip file ", source_name
                    find_skip = True
                    break
            if find_skip :
                continue
            find_skip = False
            if config_only_allow_file_list is None:
                pass
            else:
                for allow_file in config_only_allow_file_list:
                    if allow_file not in source_name :
                        find_skip = True
                        break
            if find_skip :
                continue
            self.backup_ori_file( self.backup_dir , source_name )
            self.init_ojscm( source_name )
            fc_obj = self.check_slicer_is_valid( source_name  ) 
            if not fc_obj.is_equal:
                print "Error SLICER file is not valid  . " 
                print eme.file_name
                self.rollback_and_exit()
            for eme in self.eme_dict.get( source_name ):
                yield eme 
            self.sub_create_modify_file( source_name )         
            self.sub_replace_ori_with_modified( source_name )         
            
        pass
    def sub_create_modify_file( self , eme_file_name ):
        '''
                        删除源文件，并写回
        '''
        tmp_dir = self.cher.get_modify_code_test_dir( self.version_num , self.package )   
        tmp_dir += "_rollback"      
        file_name= tmp_dir  + os.sep + eme_file_name
        #print "modified file:",file_name
        dirname, filename = os.path.split(os.path.abspath( file_name ))
        if not os.path.exists( dirname ):
            os.makedirs( dirname )            
        self.curr_ojscm.save_changed_file( file_name ) 
    def sub_replace_ori_with_modified( self , eme_file_name ):
        ori_file =  config_cs_dir + os.sep + self.package + os.sep + eme_file_name ;
        modify_file = self.cher.get_modify_code_test_dir( self.version_num , self.package ) + "_rollback"    + os.sep + eme_file_name
        shutil.copy ( modify_file , ori_file )
        pass           
    def init_ojscm( self  , file_name ):
        self.curr_ojscm = None 
        file_name = config_cs_dir + os.sep + self.package + os.sep + file_name ;
        tmp_cache_file_list = None
        self.curr_ojscm = OneJavaSourceCodeManager( file_name , tmp_cache_file_list )
        self.curr_ojscm.is_debug = True
        self.curr_ojscm.parser()
    def backup_ori_file( self , backup_dir ,file_name ):
        '''
                    如果文件已经存在，则不操作
        '''
        src = config_cs_dir + os.sep + self.package + os.sep + file_name ;
        dest = backup_dir + os.sep + file_name 
        if os.path.isfile( dest ):
            return
        dirname, filename = os.path.split(os.path.abspath( dest ))
        if not os.path.exists( dirname ):
            os.makedirs( dirname )
        shutil.copy ( src , dest )
    def check_slicer_is_valid( self , eme_file_name ):
        '''
                    验证slicer 合并后的文件是否和源文件一样。
        1、生成一个 slicer 后的文件
        2、和源文件 line by line 的对比，要完全一样才行
                    是 rollback 专用的文件夹
        '''
        dest_dir = self.cher.get_slicer_no_change_check_dir( self.version_num )
        dest_dir += "_rollback"
        file_name = dest_dir + os.sep + self.package + os.sep + eme_file_name
        dirname, filename = os.path.split(os.path.abspath( file_name ))
        if not os.path.exists( dirname ):
            os.makedirs( dirname )
        fwrite = open( file_name , "w" )
        for obj in self.curr_ojscm.slicer.code_piece_list:
            line_list = obj.ori_code_list
            for line in line_list:
                fwrite.write( line )
        fwrite.close()
        #对比文件
        strict = 0
        file_ori_name = config_cs_dir + os.sep + self.package + os.sep + eme_file_name
        fc = file_compare_linebyline( file_ori_name , file_name , strict )
        fc_obj = fc.compare_file()
        return fc_obj 
    def rollback_and_exit(self):
        '''
        '''
        for file in getNextJavaFile( self.backup_dir  ):
            source_name = file.replace( self.backup_dir  + os.sep ,"")
            src =  self.backup_dir + os.sep  + source_name 
            dest = config_cs_dir +    os.sep +  self.package + os.sep + source_name #self.package +
            shutil.copy ( src , dest )
        print "Rollback end."
        sys.exit(0)               
                        
    
    
    
if "__main__" == __name__ :
    usage = "usage: %prog [options] arg1 arg2  "
    parser = OptionParser(usage=usage)    
    parser.add_option("-P" , "--package",default="default" ,  dest="package" , type="string")
    parser.add_option("-V" , "--version",default="default" ,  dest="version" , type="string")
    parser.add_option("-R" , "--rollback",default="default" ,  dest="rollback" , type="string")
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
    cser = CloudStackExceptionRollback( options.version , options.package ) 
    cser.start_rollback()
    
    
