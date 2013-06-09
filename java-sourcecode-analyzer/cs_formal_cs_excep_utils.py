#! /usr/bin/python
#coding: utf-8
#filename cs_formal_cs_excep_utils.py

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

'''
这个工具主要用来验证CloudStack， CSExceptionErrorCode 提供的类。
'''

cs_excps='''
			ExceptionErrorCodeMap = new HashMap<String, Integer>();	
			ExceptionErrorCodeMap.put("com.cloud.utils.exception.CloudRuntimeException", 4250);
			ExceptionErrorCodeMap.put("com.cloud.utils.exception.ExceptionUtil", 4255);
			ExceptionErrorCodeMap.put("com.cloud.utils.exception.ExecutionException", 4260);
			ExceptionErrorCodeMap.put("com.cloud.utils.exception.HypervisorVersionChangedException", 4265);
			ExceptionErrorCodeMap.put("com.cloud.utils.exception.RuntimeCloudException", 4270);
			ExceptionErrorCodeMap.put("com.cloud.exception.CloudException", 4275);
			ExceptionErrorCodeMap.put("com.cloud.exception.AccountLimitException", 4280);
			ExceptionErrorCodeMap.put("com.cloud.exception.AgentUnavailableException", 4285);
			ExceptionErrorCodeMap.put("com.cloud.exception.CloudAuthenticationException", 4290);
			ExceptionErrorCodeMap.put("com.cloud.exception.CloudExecutionException", 4295);
			ExceptionErrorCodeMap.put("com.cloud.exception.ConcurrentOperationException", 4300);
			ExceptionErrorCodeMap.put("com.cloud.exception.ConflictingNetworkSettingsException", 4305);			
			ExceptionErrorCodeMap.put("com.cloud.exception.DiscoveredWithErrorException", 4310);
			ExceptionErrorCodeMap.put("com.cloud.exception.HAStateException", 4315);
			ExceptionErrorCodeMap.put("com.cloud.exception.InsufficientAddressCapacityException", 4320);
			ExceptionErrorCodeMap.put("com.cloud.exception.InsufficientCapacityException", 4325);
			ExceptionErrorCodeMap.put("com.cloud.exception.InsufficientNetworkCapacityException", 4330);
			ExceptionErrorCodeMap.put("com.cloud.exception.InsufficientServerCapacityException", 4335);
			ExceptionErrorCodeMap.put("com.cloud.exception.InsufficientStorageCapacityException", 4340);			
			ExceptionErrorCodeMap.put("com.cloud.exception.InternalErrorException", 4345);
			ExceptionErrorCodeMap.put("com.cloud.exception.InvalidParameterValueException", 4350);
			ExceptionErrorCodeMap.put("com.cloud.exception.ManagementServerException", 4355);
			ExceptionErrorCodeMap.put("com.cloud.exception.NetworkRuleConflictException", 4360);
			ExceptionErrorCodeMap.put("com.cloud.exception.PermissionDeniedException", 4365);
			ExceptionErrorCodeMap.put("com.cloud.exception.ResourceAllocationException", 4370);
			ExceptionErrorCodeMap.put("com.cloud.exception.ResourceInUseException", 4375);
			ExceptionErrorCodeMap.put("com.cloud.exception.ResourceUnavailableException", 4380);
			ExceptionErrorCodeMap.put("com.cloud.exception.StorageUnavailableException", 4385);
			ExceptionErrorCodeMap.put("com.cloud.exception.UnsupportedServiceException", 4390);
			ExceptionErrorCodeMap.put("com.cloud.exception.VirtualMachineMigrationException", 4395);
			
			ExceptionErrorCodeMap.put("com.cloud.exception.AccountLimitException", 4400);
			ExceptionErrorCodeMap.put("com.cloud.exception.AgentUnavailableException", 4405);
			ExceptionErrorCodeMap.put("com.cloud.exception.CloudAuthenticationException", 4410);
			ExceptionErrorCodeMap.put("com.cloud.exception.CloudException", 4415);
			ExceptionErrorCodeMap.put("com.cloud.exception.CloudExecutionException", 4420);
			ExceptionErrorCodeMap.put("com.cloud.exception.ConcurrentOperationException", 4425);
			ExceptionErrorCodeMap.put("com.cloud.exception.ConflictingNetworkSettingsException", 4430);
			ExceptionErrorCodeMap.put("com.cloud.exception.ConnectionException", 4435);
			ExceptionErrorCodeMap.put("com.cloud.exception.DiscoveredWithErrorException", 4440);
			ExceptionErrorCodeMap.put("com.cloud.exception.DiscoveryException", 4445);
			ExceptionErrorCodeMap.put("com.cloud.exception.HAStateException", 4450);
			ExceptionErrorCodeMap.put("com.cloud.exception.InsufficientAddressCapacityException", 4455);
			ExceptionErrorCodeMap.put("com.cloud.exception.InsufficientCapacityException", 4460);
			ExceptionErrorCodeMap.put("com.cloud.exception.InsufficientNetworkCapacityException", 4465);
			ExceptionErrorCodeMap.put("com.cloud.exception.InsufficientServerCapacityException", 4470);
			ExceptionErrorCodeMap.put("com.cloud.exception.InsufficientStorageCapacityException", 4475);
			ExceptionErrorCodeMap.put("com.cloud.exception.InsufficientVirtualNetworkCapcityException", 4480);
			ExceptionErrorCodeMap.put("com.cloud.exception.InternalErrorException", 4485);
			ExceptionErrorCodeMap.put("com.cloud.exception.InvalidParameterValueException", 4490);
			ExceptionErrorCodeMap.put("com.cloud.exception.ManagementServerException", 4495);
			ExceptionErrorCodeMap.put("com.cloud.exception.NetworkRuleConflictException", 4500);
			ExceptionErrorCodeMap.put("com.cloud.exception.PermissionDeniedException", 4505);
			ExceptionErrorCodeMap.put("com.cloud.exception.ResourceAllocationException", 4510);
			ExceptionErrorCodeMap.put("com.cloud.exception.ResourceInUseException", 4515);
			ExceptionErrorCodeMap.put("com.cloud.exception.ResourceUnavailableException", 4520);
			ExceptionErrorCodeMap.put("com.cloud.exception.StorageUnavailableException", 4525);
			ExceptionErrorCodeMap.put("com.cloud.exception.UnsupportedServiceException", 4530);
			ExceptionErrorCodeMap.put("com.cloud.exception.VirtualMachineMigrationException", 4535);			
			ExceptionErrorCodeMap.put("com.cloud.api.ServerApiException", 9999);
'''

code_dict={}
main_dict ={}
full_name_dict={}
excp_num = 0
for line in cs_excps.split("\n"):
	line=line.strip()
	if "=" in line :
		continue
	if line:
		line = line.replace("ExceptionErrorCodeMap.put(\"","")
		line = line.replace("\"","")
		line = line.replace(");","")
		lines=line.split(",")
		if 2 != len(lines):
			continue
		full_name = lines[0].strip()
		tmp_names = full_name.split(".")
		main_name = tmp_names[ len( tmp_names ) - 1 ].strip()
		err_code = lines[1].strip()
		if full_name_dict.get( full_name ) is None:
			full_name_dict[ full_name ] = full_name
		else:
			continue #仅仅忽略
		if main_dict.get( main_name ) is None:
			main_dict[ main_name ] = main_name
		else:
			print "\t\t\t\tFatal Error duplicate main_name",main_name
			sys.exit(1)
		if code_dict.get( err_code ) is None:
			code_dict[ err_code ] = err_code
		else:
			print "Fatal Error duplicate err_code:",err_code
			sys.exit(1)
		print full_name
		excp_num += 1
