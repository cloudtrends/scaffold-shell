#! /usr/bin/python
#coding: utf-8
#filename cs_formal_config_helper.py

import os
import os.path
from cs_exception_common import *
from cs_formal_config             import *
from cs_exception_common_clz import *

class ConfigHelper:
    def __init__(self):
        pass
    def get_modify_code_test_dir( self , version_num  , package ):
        modify_code_dir = self.get_ver_dir( version_num ) + os.sep + config_cs_modify_code_test_dir +  os.sep + package
        #print "modify_code_dir,",modify_code_dir
        if not os.path.exists( modify_code_dir ):
            os.makedirs( modify_code_dir )
        return modify_code_dir
    def get_slicer_no_change_check_dir( self , version_num ):
        slicer_check_dir = self.get_ver_dir( version_num ) + os.sep + config_cs_slicer_no_change_check_dir 
        if not os.path.exists( slicer_check_dir ):
            os.makedirs( slicer_check_dir )
        return slicer_check_dir
    def get_processed_eme_file_name( self ,version, package  ):
        rep_process_dir = self.get_ver_dir( version ) + os.sep + package
        if not os.path.exists( rep_process_dir ):
            os.makedirs( rep_process_dir )
        eme_file = rep_process_dir + os.sep + package + "_" + config_processed_eme_file_name
        if not os.path.isfile( eme_file ):
            open( eme_file,"w" ).close()
        return eme_file
    def get_source_backup_dir(self , version_num   ):
        '''
        
        '''
        backup_dir = self.get_ver_dir( version_num ) + os.sep + config_cs_source_backup_dir  
        if not os.path.exists( backup_dir ):
            os.makedirs( backup_dir )
        return backup_dir
    def get_ver_dir(self , version_num):
        ver_dir = config_replace_root_dir + os.sep + version_num 
        if not os.path.exists( ver_dir ):
            print "make new dir:",ver_dir
            try:
                os.makedirs( ver_dir )
            except Exception as e:
                print e
                sys.exit(0)
        return ver_dir
    def get_eme_generate_dir( self, version_num ):
        dir_str = self.get_ver_dir( version_num ) + os.sep + config_eme_generate_dir
        if not os.path.exists( dir_str ):
            os.makedirs( dir_str )
        return dir_str
    def get_eme_config_filename( self , version_num , package_name ):
        
        
        filename = self.get_eme_generate_dir(version_num) + os.sep + package_name  + "__" + config_eme_generate_filename 
        return filename
    def load_eme_dict( self , version_num , package_name ):
        eme_dict = {}
        eme_list = self.load_eme_list( version_num , package_name )
        for eme in eme_list:
            tmp_list = []
            if eme_dict.get( eme.file_name ) is None:
                tmp_list.append( eme )
            else:
                tmp_list = eme_dict.get( eme.file_name )
                tmp_list.append( eme )
            eme_dict[ eme.file_name ] = tmp_list
        return eme_dict
    def get_allow_exception_list(self , version , package):
        lines = config_allow_exception.split("\n")
        allow_exception_list = []
        for line in lines:
            line=line.strip()
            if 0 == len(line):
                continue
            tmp_lines = line.split(".")
            excep_name = tmp_lines[ len( tmp_lines ) - 1 ].strip()
            allow_exception_list.append( excep_name )
        return allow_exception_list
    def load_eme_list( self , version_num , package_name ):
        '''
        读取这样的文件
        UUID=42a3c002255455b7366ce48238880fc4
        PAKG=D:\java\workspaces\server\src\com\cloud\agent\VmmAgentShell.java##loadProperties##4e1140e2146ef21fd6cf823404523d29
        FROM=throw new CloudRuntimeException("Cannot find the file: " + file.getAbsolutePath(), ex);##9e4033b4425d2c8fa8aef8703989dd61
        T  O=throw new CloudRuntimeException("Cannot find the file: " + file.getAbsolutePath(), ex);        
        '''
        file_name = self.get_eme_config_filename( version_num,package_name   )
        if not os.path.isfile( file_name ):
            print "Config eme file not exist :", file_name
            sys.exit(1)
        file_content_list = ReadFileToList( file_name )
        list_return = []
        section_start = False
        eme = None
        for line in file_content_list:
            if SSW( line , "UUID="):
                section_start = True
                if eme is not None:
                    list_return.append( eme )
                #整理 格式....
                eme = ExceptionMapEntry()
                eme.uuid = line[ 5: ]
            if SSW( line , "PAKG=" ):
                lines = line[5:].strip().split( config_eme_line_spliter )
                if 3 != len( lines ):
                    print "Severe Error: parser eme config file format is not valid."
                    sys.exit(0)
                eme.file_name=lines[0]
                if not SSW( eme.file_name , package_name ):
                    print eme.file_name
                    print "package_name :", package_name
                    print "Severe Error: parser eme config file format is not valid,  package_name " ,package_name
                    sys.exit(0)
                # file name 是以不包括 package 开头的路径和文件名 src\com ....java 
                eme.file_name = eme.file_name[ len( package_name ) + 1 : ]
                eme.func_name=lines[1]
                eme.func_md5=lines[2]
            if SSW( line , "FROM=" ):
                lines = line[5:].strip().split( config_eme_line_spliter )
                if 3 != len( lines ):
                    print "Severe Error: parser eme config file format is not valid." , line
                    sys.exit(0)
                eme.throw_new_content = lines[0]
                eme.throw_new_md5 = lines[1]
                eme.throw_new_class  = lines[2]
            if SSW( line , "T  O=" ):
                eme.new_throw_new_content = line[5:]
        if eme is not None:
            list_return.append( eme )
        return list_return
    pass
    
    
