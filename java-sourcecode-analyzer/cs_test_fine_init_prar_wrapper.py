#! /usr/bin/python
#coding: utf-8
#filename cs_test_fine_init_prar_wrapper.py

import os
import os
import os.path
import datetime
import sys
import string
import time
import re
from inspect import currentframe, getframeinfo


reload(sys) 
sys.setdefaultencoding('utf8')

from cs_common_slicer_helper import *
from cs_exception_common import * 
from cs_common_clz import *


one_para ='"first part"  +  e.getMessage(),obj.getMsg(),"second part",true,e'
print one_para
epw = ESFineInitParaWrapper( one_para )
refine_line = epw.get_refined_paras(  )
print refine_line


