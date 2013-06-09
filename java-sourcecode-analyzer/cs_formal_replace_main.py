#!/usr/bin/python
#coding: utf-8
#filename cs_formal_replace_main.py

import os
import os.path
import datetime
import sys
import string
import time
import re
import logging
import shutil
from optparse import OptionParser 



from cs_exception_common         import *
from cs_formal_config             import *
from cs_formal_config_helper    import *
from cs_try_catch_analyzer        import *
from file_comp_lbl                import *
reload(sys) 
sys.setdefaultencoding('utf8')



class CloudStackExceptionReplace:
    '''
            替换代码的总控制函数
            第一步：输入版本号，根据版本号创建目录
    '''
    def __init__( self , version_num , package_name ):
        '''
        '''
        self.test_process_eme_count = 0
        self.opened_file_dict    ={}
        self.is_debug             = False
        self.version_num         =    version_num
        self.cher = ConfigHelper()
        self.package        = package_name            #当前的package
        self.backup_dir        = self.cher.get_source_backup_dir( version_num  )  + os.sep + self.package        #指定默认的备份文件夹
        self.curr_ojscm        = None # 当前的eme分析器
        tmp_file_name = self.cher.get_eme_config_filename( version_num,package_name   )
        if not os.path.isfile( tmp_file_name ):
            print "Fatal error no eme config file, generate one first."
            self.rollback_and_exit()
        self.eme_list = self.cher.load_eme_list( version_num , package_name )
        self.eme_dict = self.cher.load_eme_dict( version_num , package_name )
        self.eme_status_file = self.cher.get_processed_eme_file_name(  version_num , package_name )
        #为查找方便使用的。
        #比如：中断后重新再来。。。tcf 
        self.eme_processed_dict = {}        # dictionary ExceptionMapEntry
        eme_processed_list = ReadFileToList( self.eme_status_file )
        for eme_uuid in eme_processed_list:
            if self.eme_processed_dict.get( eme_uuid ) is None:
                self.eme_processed_dict[ eme_uuid ] = eme_uuid
            else:
                print "Fatal error EME processed duplicated."
                self.rollback_and_exit()
        #for eme in eme_list:
        #    self.need_process_dict[ eme.uuid ] = eme
        self.total_item_num = len( self.eme_list )
        self.curr_num = 0
        self.already_processed_list ={} # dictionary
        self.not_include_file_list = []
        #self.
        
        print "backup dir:", self.backup_dir
        if not os.path.exists( self.backup_dir ):
            print "create backup dir:", self.backup_dir
            os.makedirs( self.backup_dir )
        pass
    def get_next_eme( self ):
        for source_name in self.eme_dict:
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
            #print "Begin check slicer is valid ."
            fc_obj = self.check_slicer_is_valid( source_name  ) 
            if not fc_obj.is_equal:
                print "Error SLICER file is not valid  . " 
                print eme.file_name
                self.rollback_and_exit()
            for eme in self.eme_dict.get( source_name ):
                yield eme
            #
            self.sub_add_necessary_package(  )
            #
            self.sub_create_modify_file( source_name )
            #
            #self.check_ori_against_modify_file( eme )
            self.sub_replace_ori_with_modified( source_name )
    def start( self ):
        for eme in self.get_next_eme():
            '''
                                问题所在：以eme为单位，粒度太细，要频繁打开关闭，修改文件
                                最好把eme按照文件groupby 然后以文件轮训，然后在以eme循环
            '''
            '''
            if self.test_process_eme_count < 100:
                self.test_process_eme_count += 1
            else:
                break
            '''
            if not self.check_src_file_is_valid( eme ):
                '''
                check for each eme element.
                                        这种机制不支持持续更新。
                                        应该备份 eme 列表并维护状态，支持持续更新。
                '''
                print "Error SRC file is not valid by check file . " 
                print eme.file_name
                self.rollback_and_exit()
            # check if processed in this version
            #uuid 重复，暂时不启用
            '''
            #if self.sub_is_eme_processed(eme):
            #    print "Fatal error eme already processed."
            #    self.rollback_and_exit()
            '''
            #add into processed list
            if self.replace_exception_to_i18n( eme ):
                pass
            else:
                print "File replace exception error "
                self.rollback_and_exit()
            #uuid 重复，暂时不启用
            '''
            #self.sub_update_eme_status( eme )
            '''
            pass
        pass
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
    def sub_add_necessary_package( self ):
        obj = self.curr_ojscm.get_package_func_obj()
        obj.replace_code_list =  obj.ori_code_list
        import_num = 0
        line_list = []
        line_dict={}
        line_num = 0
        import_str = "import com.tcloud.utils.ESECreater;\n\n"
        if self.package == "utils":
            import_str = "import com.tcloud.utils.ESEBCreater;\n\n"
        for line in obj.replace_code_list:
            line_list.append( line )
            if SSW( line , "import " ) and SEW( line , ";" ):
                import_num += 1
                line_dict[  ( import_num ) ] = line_num
            line_num += 1
        import_insert_to = line_dict.get(  ( import_num ) )
        #print "insert:",import_insert_to
        if import_insert_to is None:
            line_list.append(  import_str )
            print "print file name"
        else:
            line_list.insert( import_insert_to , import_str )
        obj.new_code_list = line_list
        obj.is_modified = True
        self.curr_ojscm.update_one_piece_obj_by_seq_no( obj )
        pass
    def sub_update_eme_status(self , eme ):
        appendOneLine( self.eme_status_file, eme.uuid )
        self.eme_processed_dict[ eme.uuid ] = eme.uuid
        pass
    def sub_is_eme_processed(self  ,eme ):
        if self.eme_processed_dict.get( eme.uuid ) is None:
            return False
        else:
            return True
        pass
    def init_ojscm( self  , file_name ):
        self.curr_ojscm = None 
        file_name = config_cs_dir + os.sep + self.package + os.sep + file_name ;
        #cache 提高速度 针对解析后的对象，暂不用
        tmp_cache_file_list = None
        #if self.opened_file_dict.get( file_name ) is None:
        #    tmp_cache_file_list = ReadFileToList( file_name )
        #    self.opened_file_dict[ file_name ] = tmp_cache_file_list
        #else:
        #    #print "..."
        #    tmp_cache_file_list = self.opened_file_dict[ file_name ]
        self.curr_ojscm = OneJavaSourceCodeManager( file_name , tmp_cache_file_list )
        self.curr_ojscm.is_debug = True
        self.curr_ojscm.parser()
        # reformat ori_code_list to throw new one line format
        # and replace replace_code_list
        all_func_obj_list = self.curr_ojscm.get_all_func_name_list()
        for obj in all_func_obj_list:
            throw_formatter    = JavaFunctionThrowNewFormatter( obj )
            format_code_list = throw_formatter.format()
            obj.replace_code_list = format_code_list
            self.curr_ojscm.update_one_piece_obj_by_seq_no( obj )
        pass
    def init_not_include_file_list( self  ):
        pass
    def replace_exception_to_i18n(self , eme):
        '''
                    步骤：
                    1、从eme中找到需要替换的func
                        sub_is_func_exist
                    2、从eme中找到需要替换的 throw new line
                        sub_is_throw_new_exist
                        如果找不到 throw new 那么看一下是否被替换过了！
                        替换过得标志是什么？
                    3、开始替换
                        sub_replace_exception
                    4、修改 obj 的状态为 modified = True
                        sub_....
                    5、删除源文件
                        sub_delete_ori_file()
                    6、合并，并写回文件。
                        sub_create_new_ori_file()
                    7、验证文件,按照行对比，找不不一样的行。
                        sub_check_ori_and_new_ori
                    以上7个步骤的 func name 都以 sub 开头
        '''
        #step three
        try:
            self.sub_replace_exception( eme )
        except Exception as e :
            print e
            self.rollback_and_exit()
        #step six
        
        #step chech file
        #
        # delete ori file
        # copy modified file to ori file
        #
        return True
        pass
    def sub_replace_ori_with_modified( self , eme_file_name ):
        ori_file =  config_cs_dir + os.sep + self.package + os.sep + eme_file_name ;
        modify_file = self.cher.get_modify_code_test_dir( self.version_num , self.package )   + os.sep + eme_file_name
        shutil.copy ( modify_file , ori_file )
        pass
    def check_ori_against_modify_file( self , eme ):
        '''
        对比2个文件的函数名是否匹配，md5是否匹配
        随机抽查不是 throw new  的行匹配
        '''
        ori_file =  config_cs_dir + os.sep + self.package + os.sep + eme.file_name ;
        modify_file = self.cher.get_modify_code_test_dir( self.version_num , self.package )   + os.sep + eme.file_name
        ori_ojscm = OneJavaSourceCodeManager( ori_file , None )
        ori_ojscm.parser()
        modify_ojscm = OneJavaSourceCodeManager( modify_file ,None)
        modify_ojscm.parser()        
        for obj in ori_ojscm.get_all_func_name_list():
            func_name_tmp = obj.func_name
            #print obj
            func_obj = modify_ojscm.get_obj_by_funcname_and_md5( obj.func_name  , obj.func_paras_md5 )
            if func_obj is None:
                print "Fatal Error modify and ori source code is not match."
                self.rollback_and_exit()
        #MaxLineNum = 
        return True
        pass
    def compare_modify_and_ori_file( self , eme ):
        '''
        random line compare
        '''
        pass
    def sub_replace_exception( self ,eme  ):
        '''
        Replace throw new with ElasterStack International Code
        '''
        func_obj = self.curr_ojscm.get_obj_by_funcname_and_md5( eme.func_name  , eme.func_md5 )
        if func_obj is None:
            print "Fatal Error eme not match in source code ."
            self.rollback_and_exit()
        new_code_list = []
        line_num_in_func = 0
        find_line = ''
        is_find_line = False
        allow_replace = True
        replace_to_line = ''
        #
        need_replace_line_list = []
        if func_obj.is_modified:
            need_replace_line_list = func_obj.new_code_list
        else:
            '''
                                考虑到要处理换行exception的情况，需要使用
                                throw_formated_code_list
                                formated_code_list 只是处理了 function声明换行的部分。
                                能不能也加上 throw new 换行呢？
            '''
            need_replace_line_list = func_obj.replace_code_list
        pre_line = '' # if pre line is if without {} skip this line
        line_num = 0
        for line in need_replace_line_list:
            line_num_in_func += 1
            fip_md5=''
            init_paras=''
            fine_init_paras=''
            if isJavaThrowNewLine( line ):
                #print line
                
                if isNewObjInThrowNewLine( line ):
                    new_code_list.append( line )
                    pre_line = line
                    continue
                #print "need replace line:",line
                init_paras = getThrowInitParameters( line )
                fine_init_paras = removeThrowNewInitParaSpace( init_paras )
                #print "fine_init_paras=",fine_init_paras
                fip_md5 = get_md5( fine_init_paras )
                if fip_md5 == eme.throw_new_md5 and  allow_replace:                
                    is_find_line = True
                    allow_replace = False
                    prefix_str = get_throw_new_line_prefix_str( line )
                    new_line = line
                    #
                    epw = ESFineInitParaWrapper( fine_init_paras )
                    wrap_fine_init_paras = epw.get_refined_paras(  )
                    wrap_fine_init_paras=wrap_fine_init_paras.strip()
                    if 0 == len( wrap_fine_init_paras ):
                        new_code_list.append( line )
                        is_processed = True
                        pre_line = line
                        continue    
                    else:
                        ins_name = "_ex_"
                        creater_name = ""
                        if self.package == "utils":
                            creater_name = "ESEBCreater"
                        else:
                            creater_name = "ESECreater"
                        wrap_throw_new = eme.throw_new_class +' '+ ins_name +'=(' + eme.throw_new_class + ') '+ creater_name +'.create("' + eme.throw_new_class + '",' + wrap_fine_init_paras + ");throw "+ ins_name +";" + self.curr_ojscm.slicer.cr_lf
                    #
                    
                    is_processed = False
                    if SCOMPARE( pre_line , "else" ) and not is_processed:
                        new_code_list.append( line )
                        is_processed = True
                        pre_line = line
                        continue                        
                    if SEW( pre_line , ")" ) and ( not SSW( pre_line , "if" )  ) and not is_processed:
                        new_code_list.append( line )
                        is_processed = True
                        pre_line = line
                        continue
                    if SSW( pre_line, "if" ) and SEW( pre_line,")" ) and not is_processed:
                        #new_code_list.append( "//1 " + str(line_num) +"\n" )
                        new_code_list.append( line )
                        is_processed = True
                        pre_line = line
                        continue
                    if SSW( pre_line , "}" ) and SEW( pre_line, "else" ) and not is_processed:
                        #new_code_list.append( "//2 " + str(line_num) +"\n"  )
                        new_code_list.append( line )
                        pre_line = line
                        is_processed = True
                        continue
                    if not is_processed:
                        #new_code_list.append( "//3 " + str(line_num)  +"\n" )
                        # add tips to code
                        new_code_list.append( prefix_str + "//DO NOT CHANGE ID:" + eme.throw_new_md5+ self.curr_ojscm.slicer.cr_lf  )
                        new_code_list.append( prefix_str + wrap_throw_new   )
                        new_code_list.append( prefix_str + "//__END" + self.curr_ojscm.slicer.cr_lf   )
                else:
                    new_code_list.append( line )
            else:
                new_code_list.append( line )
            pre_line = line
            line_num += 1
        if not is_find_line:
            print "Fatal error cause eme not find in source code ."
            print eme.file_name
            print eme.func_name
            print eme.throw_new_content
            print "eme uuid:", eme.uuid
            print "\tStart auto rollback... "
            self.rollback_and_exit()
        func_obj.is_modified = True
        func_obj.new_code_list = new_code_list
        self.curr_ojscm.update_one_piece_obj_by_seq_no( func_obj )
        pass
    def sub_create_modify_file( self , eme_file_name ):
        '''
                        删除源文件，并写回
        '''
        tmp_dir = self.cher.get_modify_code_test_dir( self.version_num , self.package )         
        file_name= tmp_dir  + os.sep + eme_file_name
        #print "modified file:",file_name
        dirname, filename = os.path.split(os.path.abspath( file_name ))
        if not os.path.exists( dirname ):
            os.makedirs( dirname )            
        self.curr_ojscm.save_changed_file( file_name )
        
    def check_slicer_is_valid( self , eme_file_name ):
        '''
                    验证slicer 合并后的文件是否和源文件一样。
        1、生成一个 slicer 后的文件
        2、和源文件 line by line 的对比，要完全一样才行
        '''
        dest_dir = self.cher.get_slicer_no_change_check_dir( self.version_num )
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
        
        
    def check_src_file_is_valid( self , eme ):
        '''
        check 什么呢？
        1.文件中是否包含该方法，md5签名是否一致
        2.catch中是否包含 eme 的throw new exception ，md5签名是否一致
        '''
        #print "-        -        -        -"
        split_by = self.curr_ojscm.slicer.cr_lf
        func_obj = self.curr_ojscm.get_obj_by_funcname_and_md5( eme.func_name  , eme.func_md5 )
        is_func_md5_match = False
        if func_obj is None:
            print eme.package , " file is :", eme.file_name
            print " func md5 is not match or find ", eme.func_name
        else:
            #if func_obj.func_paras_md5 == eme.func_md5:
            is_func_md5_match = True
        if not is_func_md5_match:
            print "Error source code function md5 not match"
            return False
        is_throw_md5_match = False
        for line in func_obj.ori_code_list:
            #print line
            if isJavaThrowNewLine( line ):
                #print line
                fip_md5=getJavaThrowNewLineMd5( line )
                #print "Dyn:",fip_md5
                #print "EME:",eme.throw_new_md5
                if fip_md5 == eme.throw_new_md5:
                    is_throw_md5_match = True
                    break
        if is_func_md5_match and is_throw_md5_match:
            return True
        else:
            self.curr_ojscm = None # 文件部分符合条件
            if not is_throw_md5_match:
                print "eme uuid:",eme.uuid
                print eme.file_name
                print eme.throw_new_md5
                print "Throw New md5 is not match " , eme.throw_new_content
        return False
    def allow_continue( self ):
        pass
    def get_next_need_process_item( self ):
        eme = ExceptionMapEntry()
        return eme
    def read_map_list( self ):
        pass
    def backup_ori_file( self , backup_dir ,file_name ):
        '''
        return if file already exist.
        '''
        src = config_cs_dir + os.sep + self.package + os.sep + file_name ;
        dest = backup_dir + os.sep + file_name 
        if os.path.isfile( dest ):
            return
        dirname, filename = os.path.split(os.path.abspath( dest ))
        if not os.path.exists( dirname ):
            os.makedirs( dirname )
        shutil.copy ( src , dest )

    def create_version_dir( self , dir_name ):
        pass
        
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
    cseReplace = CloudStackExceptionReplace( options.version , options.package )
    start = time.time()
    print start
    if "default" != options.rollback    :
        if "yes" == options.rollback:
            print "Start rollback ... "
            cseReplace.rollback_and_exit()
            sys.exit(0)
    else:    
        print "Start replace ..."
        cseReplace.start()
        tips="recommend: STAY here and submit code to svn for test( such as refresh eclipse project to check error  ), then rollback"
        print tips
        input_variable = raw_input ("Do you want rollback? y or n:")
        print ("your input is:" + input_variable) 
        if "y" == input_variable:
            cseReplace.rollback_and_exit()
        else:
            # if not rollback , means accept the replacement result ,then,
            # we shoud better backup the original eme file , more see ReadMe.txt
            #
            cher_tmp = ConfigHelper()
            ori_eme_file_name = cher_tmp.get_eme_config_filename( options.version , options.package   )
            new_eme_file_name = "replace_"+ori_eme_file_name+"_ok_so_backup" + ".bak"
            shutil.copy ( ori_eme_file_name , new_eme_file_name )
            pass
    elapsed = (time.time() - start)
    print "elapsed:",elapsed
    #start = time.time()
    #... do something
    #elapsed = (time.time() - start)
    
'''
    def check_src_file_is_valid( self , eme ):
        
        check 什么呢？
        1.文件中是否包含该方法，md5签名是否一致
        2.catch中是否包含 eme 的throw new exception ，md5签名是否一致
        
        file_name = config_cs_dir + os.sep + self.package + os.sep + eme.file_name ;
        self.curr_ojscm = OneJavaSourceCodeManager( file_name )
        self.curr_ojscm.is_debug = True
        self.curr_ojscm.parser()
        split_by = self.curr_ojscm.slicer.cr_lf
        func_obj = self.curr_ojscm.get_obj_by_funcname_and_md5( eme.func_name  , eme.func_md5 )
        is_func_md5_match = False
        if func_obj is None:
            print eme.package , " file is :", eme.file_name
            print " func md5 is not match or find ", eme.func_name
        else:
            #if func_obj.func_paras_md5 == eme.func_md5:
            is_func_md5_match = True
        func_try_blocks = SliceFuncToTryBlocks()
        func_try_blocks.convert_to_try_blocks( func_obj , split_by )
        try_catch_blocks = func_try_blocks.get_all_try_catch_blocks()
        is_throw_md5_match = False
        for block in try_catch_blocks:
            catch_blocks_extractor = ExtractCatchBlocksFromTryCatchBlocks( block )
            new_block = catch_blocks_extractor.extract()                
            for catch_block_obj in new_block.catch_block_list:
                catch_attr_analyzer = CatchAttrAnalyzer( catch_block_obj , split_by )
                catch_attr = catch_attr_analyzer.analysis()
                if not catch_attr.is_have_throw_new:
                    continue
                if catch_attr.throw_init_paras_md5 == eme.throw_new_md5 :
                    is_throw_md5_match = True
                    break
        if is_func_md5_match and is_throw_md5_match:
            return True
        else:
            self.curr_ojscm = None # 文件部分符合条件
            if not is_throw_md5_match:
                print "throw new md5 is not match " , eme.throw_new_content
        return False
'''