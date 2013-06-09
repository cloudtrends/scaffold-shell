#! /usr/bin/python
#coding: utf-8
#filename cs_formal_config.py

import os

'''
global config file , dir's , java classes , skipped file or path etc.
'''

# location of workspace of ElasterStack
config_cs_dir="C:\Users\chunfeng\workspace42_maintrunk"

# dir of backup file when replacing
config_replace_root_dir="c:\java\exception-replace-formal"

#备份文件夹
config_cs_source_backup_dir = "cs_source_backup"
config_cs_slicer_no_change_check_dir = "cs_slicer_source_check"
#生成新文件测试目录
config_cs_modify_code_test_dir = "cs_modify_code_test"
#生成配置文件夹
config_eme_generate_dir ="eme_generate_config" 
config_eme_generate_filename ="eme_generate_config.txt"
config_eme_properties_file_name="eme.properties";
config_eme_line_spliter="__##__"



#翻译后的，只读的文件夹
config_eme_lang_trans_dir = "eme_readonly_config"
#替换进度控制文件夹
config_replace_process_dir = "replace_process_control"
config_processed_eme_file_name = "eme_processed.txt"




#根据版本号，作为分类，每个类下都有以上4个目录
# "utils"  中的exception很底层，暂不支持
#允许的package 列表
config_allow_package= ["utils" ,"server" ,   "agent" , "api" , "core" ]
# sikp file list
config_skip_file_list = ["Networks", "AmazonEC2Stub","Base64Coder" ]

#tcf for test 
config_only_allow_file_list= None
#config_only_allow_file_list= ["StorageManagerImpl"]


#比较 path 的时候会自动加上 sep
config_skip_path_list = [ "test" ,"tcloud"]

#通过 cs_formal_cs_excep_utils 来保证 exception的唯一性
#这份白名单是必须的！
#和Java类要一一对应
#下面的exception要和ESECreater中的一一对应。
#com.cloud.utils.exception.ExceptionUtil  不支持
#可以执行这个脚本，生成java 中的数组
#  
config_allow_exception='''
javax.naming.ConfigurationException
com.cloud.utils.exception.CloudRuntimeException
com.cloud.utils.exception.ExecutionException
com.cloud.utils.exception.HypervisorVersionChangedException
com.cloud.utils.exception.RuntimeCloudException
com.cloud.exception.CloudException
com.cloud.exception.AccountLimitException
com.cloud.exception.AgentUnavailableException
com.cloud.exception.CloudAuthenticationException
com.cloud.exception.CloudExecutionException
com.cloud.exception.ConcurrentOperationException
com.cloud.exception.ConflictingNetworkSettingsException
com.cloud.exception.DiscoveredWithErrorException
com.cloud.exception.HAStateException
com.cloud.exception.InsufficientAddressCapacityException
com.cloud.exception.InsufficientCapacityException
com.cloud.exception.InsufficientNetworkCapacityException
com.cloud.exception.InsufficientServerCapacityException
com.cloud.exception.InsufficientStorageCapacityException
com.cloud.exception.InternalErrorException
com.cloud.exception.InvalidParameterValueException
com.cloud.exception.ManagementServerException
com.cloud.exception.NetworkRuleConflictException
com.cloud.exception.PermissionDeniedException
com.cloud.exception.ResourceAllocationException
com.cloud.exception.ResourceInUseException
com.cloud.exception.ResourceUnavailableException
com.cloud.exception.StorageUnavailableException
com.cloud.exception.UnsupportedServiceException
com.cloud.exception.VirtualMachineMigrationException
com.cloud.exception.ConnectionException
com.cloud.exception.DiscoveryException
com.cloud.exception.InsufficientVirtualNetworkCapcityException
com.cloud.api.ServerApiException
com.cloud.exception.OperationTimedoutException
java.lang.Exception
java.rmi.ServerException
com.cloud.resource.UnableDeleteHostException
javax.servlet.ServletException
java.lang.RuntimeException
com.cloud.cluster.ActiveFencingException
java.lang.IllegalArgumentException
com.cloud.agent.manager.authn.AgentAuthnException
java.security.InvalidParameterException
java.io.IOException
java.util.ConcurrentModificationException
java.rmi.RemoteException
com.cloud.exception.UsageServerException
java.lang.IllegalStateException
com.cloud.utils.fsm.NoTransitionException
java.lang.UnsupportedOperationException
com.cloud.exception.UnsupportedVersionException
com.cloud.exception.AgentControlChannelException
'''

if __name__ == "__main__":
	lines = config_allow_exception.split("\n")
	result = ''
	for line in lines:
		line = line.strip();
		if not line:
			continue
		result += '"' + line + '",'
	f = open("d:/excep.txt","w")
	print result
	f.write( result )
	f.close()