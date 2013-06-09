#! /usr/bin/python
#coding: utf-8
#filename test_extract_match_line.py

from cs_exception_common import *
from optparse import OptionParser 


if "__main__" == __name__ :  
	usage = "usage: %prog [options] arg1 arg2 such as python cs_code_exception_extractor.py  -p /home/source/trunk/ "
	parser = OptionParser(usage=usage)	
	parser.add_option("-p" , "--path",default="default" ,  dest="java_path" , type="string")
	(options, args) = parser.parse_args()
	if "default" != options.java_path and len(options.java_path ) > 1 :
		start_path = options.java_path
		skip_list = []
		skip_list.append( "AmazonEC2Stub" )
		skip_path_list = []
		skip_path_list.append( "test" )
		skip_path_list.append( "awsapi" )
		exception_clz_str = ''
		
		if True:
			sys.exit(0)
		#´òÓ¡exception ×¨ÓÃ
		for file in getNextJavaSourceFile( start_path , skip_list , skip_path_list ):
			if file.endswith("Exception.java"):
				int_s = file.find(os.sep+"src"+os.sep)
				if int_s > 0:
					file = file[int_s + 5 :]
				#int_i = file.rfind( os.sep )
				#if int_i > 0 :
				#	file = file[int_i+1:]
				file=file.replace(os.sep,".")
				file=file[:len(file)-5]
				exception_clz_str += "\"" + file + "\","
		print exception_clz_str
	else:
		print usage


