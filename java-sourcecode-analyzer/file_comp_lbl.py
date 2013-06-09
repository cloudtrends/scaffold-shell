#! /usr/bin/python
#coding: utf-8
#filename file_comp_lbl.py

import os
import os
import os.path
import datetime
import sys
import string
import time
import re
import logging

class file_compare_obj:
	def __init__( self ):
		self.desc = ''
		self.is_equal = False
		pass
		
class file_compare_linebyline:
	'''
	给定输入的2个文件，打印两个文件是否相等。
	参数：file_name_ori , file_name_comp , comp_level
	
	
	comp_level : 只有两个：strict(0) 严格相等 , strip(1) 相等(去掉行的空格 \t \r\n )
	'''
	def __init__(self , file_name_ori , file_name_comp , comp_level ):
		self.is_debug = False
		self.file_name_ori = file_name_ori
		self.file_name_comp = file_name_comp
		self.comp_level = comp_level
		self.ori_list = []
		self.comp_list = []
		self.ori_line_num = 0
		self.comp_line_num = 0
		f = open( self.file_name_ori ,"r")
		for line in f.readlines():
			self.ori_list.append( line )
			self.ori_line_num += 1
		f.close()
		f = open( self.file_name_comp ,"r")
		for line in f.readlines():
			self.comp_list.append( line )
			self.comp_line_num += 1
		f.close()
		if self.is_debug:
			print self.ori_line_num
			print self.comp_line_num
	def compare_file(self):
		#print "a"
		fcobj = file_compare_obj()
		#print "b"
		if not self.ori_line_num == self.comp_line_num :
			fcobj.is_equal = False
			fcobj.desc = 'File line number is not equal . ' , self.ori_line_num , ':' , self.comp_line_num  
			return fcobj
		fcobj.is_equal = True # asume is match
		fcobj.desc = 'file match'
		for num in range( self.ori_line_num ):
			ori_line = self.ori_list[ num ]
			comp_line = self.comp_list[ num ]
			if ori_line == comp_line :
				continue
			else:
				fcobj.is_equal = False
				fcobj.desc = "File line not match " ,"ori file line ", num , " content" , ori_line
				break
			print num
		return fcobj
		pass
		