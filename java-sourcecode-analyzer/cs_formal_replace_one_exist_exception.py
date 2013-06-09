#coding: utf-8
#filename cs_formal_replace_one_exist_exception.py

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


#DO NOT CHANGE reference generate eme properties python file.
SPLITER_PARA = "_#_"
SPLITER_INNER = "_@_"



class ReplaceExceptionInfo():
    java_source_file=None
    exception_md5=None
    exception_from=None
    exception_to=None

class CloudStackReplaceOneExistException():
    def __init__(self , version_num , package ):
        self.version_num = version_num
        self.package    = package
        self.cher = ConfigHelper()
        self.backup_dir        = self.cher.get_source_backup_dir( version_num  )  + os.sep + self.package 
        if not os.path.exists( self.backup_dir ):
            print "create backup dir:", self.backup_dir
            os.makedirs( self.backup_dir )
        pass
    def start_replace(self):
        '''
        1. backup java source file
        
        '''
        if self.check_tmplt_file_exist():
            print "find template file , begin checking ... "
            except_info_list = self.get_tmplt_file_format()
            for expt_obj in except_info_list:
                file_name = config_cs_dir           + os.sep + expt_obj.java_source_file
                backup_to_file = self.backup_dir    + os.sep + expt_obj.java_source_file
                md5 = expt_obj.exception_md5
                if self.check_exception_exist_in_original_file(md5, file_name):
                    if not os.path.isfile(  backup_to_file ):
                        print "backup from:",file_name
                        print "to:",backup_to_file
                        dirname, filename = os.path.split(os.path.abspath( backup_to_file ))
                        if not os.path.exists( dirname ):
                            print "make dir:",dirname
                            os.makedirs( dirname )
                        shutil.copy ( file_name , backup_to_file )
                    else:
                        print "already backuped."
                    self.do_replace( expt_obj , file_name )
                    
                    #check by eyes and rollback if needed.
                    input_variable = raw_input ("Do you want rollback? y or n:")
                    if "y" == input_variable:
                        shutil.copy (   backup_to_file,file_name )
                        
                    pass
            pass
        else:
            print "template file not exist."
            sys.exit(1)
        pass
    def rollback_and_exit(self):
        
        sys.exit(0)
    def do_replace(self , expt_obj , file_name ):
        ojscm = OneJavaSourceCodeManager( file_name , None )
        ojscm.is_debug = True
        ojscm.parser()
        do_not_change_prefix="//DO NOT CHANGE ID:"
        need_line=do_not_change_prefix + expt_obj.exception_md5
        split_by = ojscm.slicer.cr_lf
        for obj in ojscm.get_all_funcname_obj_list():
            is_do_replace = False
            new_code_list=[]
            is_find_dest = False
            prefix_space=""
            for line in obj.ori_code_list:
                if is_find_dest:
                    is_do_replace=True
                    is_find_dest=False
                    new_code_list.append( prefix_space + expt_obj.exception_to + split_by )
                else:
                    line_new = line.strip()
                    if( line_new == need_line ):
                        is_find_dest=True
                        prefix_space = line[  : line.find( line_new ) ]
                        retrive_paras = retriveThrowInitParameters( expt_obj.exception_to )
                        fine_init_paras = removeThrowNewInitParaSpace( retrive_paras )
                        properties_md5 = get_msg_properties_md5( fine_init_paras )
                        print "properties md5 :" , properties_md5                        
                        #fip_md5 = get_md5( fine_init_paras )
                        new_do_not_change_line = prefix_space + do_not_change_prefix + properties_md5 + split_by 
                        new_code_list.append( new_do_not_change_line )
                    else:                    
                        new_code_list.append( line )
            if is_do_replace :
                obj.is_modified = True
                obj.new_code_list = new_code_list
                ojscm.update_one_piece_obj_by_seq_no( obj )
                break
        print "save changed file to :",file_name
        ojscm.save_changed_file( file_name )
        pass
    def check_tmplt_file_exist(self   ):
        file_name = "./template/replace_one_exception."+ self.version_num +".txt"
        if os.path.exists( file_name ) :
            return True
        else:
            return False
    def get_tmplt_file_format(self  ):
        file_name = "./template/replace_one_exception."+ self.version_num +".txt"
        file_content_list = ReadFileToList( file_name )
        except_info_list=[]
        one_part_begin=False
        one_except_info=None
        for line in file_content_list:
            #print line
            line=line.strip()
            if line == "#begin":
                one_part_begin=True
                one_except_info = ReplaceExceptionInfo()
                continue
            if line == "#end" :
                one_part_begin=False
                if one_except_info.java_source_file is None or one_except_info.exception_md5 is None or one_except_info.exception_from is None or one_except_info.exception_to is None :
                    print "format is not valid "
                    sys.exit(1)
                print "add new exception info obj."
                except_info_list.append( one_except_info )
                one_except_info=None
                continue
            if line.startswith(    "#" ) :
                continue
            if line.startswith( "java_source_file=" ) and one_part_begin :
                one_except_info.java_source_file = line[ 17 : ]
                pass
            if line.startswith( "exception_md5=" ) and one_part_begin :
                one_except_info.exception_md5  = line[ 14 : ]
                pass
            if line.startswith( "exception_from=" )  and one_part_begin :
                one_except_info.exception_from  = line[ 15: ]
                pass
            if line.startswith( "exception_to=" )  and one_part_begin :
                one_except_info.exception_to  = line[ 13: ]
                pass
        return except_info_list
    
    def check_exception_exist_in_original_file(self , md5_str , file_name):
        ojscm = OneJavaSourceCodeManager( file_name , None )
        ojscm.is_debug = True
        ojscm.parser()
        need_line="//DO NOT CHANGE ID:"+md5_str
        split_by = ojscm.slicer.cr_lf
        for obj in ojscm.get_all_funcname_obj_list():
            ori_code_line_num = len( obj.ori_code_list )
            curr_num = 0
            while curr_num < ori_code_line_num:
                line = obj.ori_code_list[ curr_num ]
                line_new = line.strip()
                if( line_new == need_line ):
                    print line
                    next_line = obj.ori_code_list[ (curr_num + 1) ]
                    next_line=next_line.strip()
                    print next_line
                    retrive_paras = retriveThrowInitParameters( next_line )
                    fine_init_paras = removeThrowNewInitParaSpace( retrive_paras )
                    properties_md5 = get_msg_properties_md5( fine_init_paras )
                    print "properties md5 :" , properties_md5
                    fip_md5 = get_md5( fine_init_paras )
                    print fip_md5
                    if fip_md5 == md5_str:
                        print "md5 check ok"
                        return True
                    else:
                        print "md5 check not match"
                        print next_line
                        sys.exit(1)
                curr_num += 1
        return False
        pass
    
    

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
    cser = CloudStackReplaceOneExistException( options.version , options.package ) 
    cser.start_replace()
