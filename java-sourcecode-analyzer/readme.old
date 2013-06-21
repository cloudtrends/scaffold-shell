
=	=	=	=	=	=	1. Java Section
||			in package api and utils add dynamic create exception class 
||			name is : ESECreater  and ESEBCreater
||
=	=	=	=	=	=	


The rules about md5 :
1. throw new exception initialize parameters.(remove space and not include brackets it self)
2.

=	=	=	=	=	=	2. specify declare 
||			when using python script , the must needed parameters is : -P package -V  version
=	=	=	=	=	=	
备注：
    eme 配置文件是：ExceptionMapEntry 的缩写，每个throw new exception
                    都对应 eme  配置文件的一项。
    版本号：版本号是本次操作的一个标识，用于做备份，回滚用。
            每个版本号对应一个目录，所有的操作记录都放在这个目录里。
            
            
            
=	=	=	=	=	=	3. Exception 替换的方式（一次替换只针对一个package）
|| 第一种： 以package为单位进行替换		
||			cs_formal_generate_eme.py -P package -V  vXXX	
|| 第二种：以 某个文件，或几个文件为单位进行替换（测试状态下用很方便）
||			参考cs_formal_config.py 配置文件
|| 第三种：替换某个包的一批文件 （增量替换，边开发边替换）
||			指定包含文件列表的文件名 ( 用-F指定输入的 java source code  文件列表)
|| 			python cs_formal_generate_eme.py -P server -Vb -F X:xxx.txt
||			文件列表的格式最关键的是java文件名。
||	每次替换都要一个 version ，不能重复，防止覆盖以前替换的eme文件。
||  每次替换完后的eme，要备份单独保存。
|| 以上三种方法，每次生成的eme放在api package的 l10n 下。
|| 			 
||			文件名分别为：（ 和package 一一对应）
||			utils__eme_generate_config.txt
||			server__eme_generate_config.txt
||			core__eme_generate_config.txt
||			api__eme_generate_config.txt
||			agent__eme_generate_config.txt
||			按照package，把每次操作的 eme 合并到对应的eme文件中。
||			( 比如：执行了一次增量的exception替换，那么把生成的 eme 配置文件合并到对应的文件中。 )
|| 第四: 更新一个已经存在的被替换过的Exception update ONE already exist replaced exception
||		  purpose : amend the english exception message 
		    比如：需要修改Exception中的提示信息。  
||        steps:
||			1.  copy and rename to a new file from : template/replace_one_exception.tmp.txt
||				fulfill the required fields.
||				provide md5 value of the exception , 
||					find it at //DO NOT CHANGE ID: xxx , above the exception line.
||			    provide the full file name which, the exception in it
||					format package\src\com\xxx\xxx\xxx\XxxXxx.java
||			
||
||			reference: template/replace_one_exception.tmp.txt
||			2. python cs_formal_replace_one_exist_exception.py -V -P
||					replace_one_exception.VERSION_NUM.txt
||			3. 
|| 第五： 新增一个Exception
||			step 1.  写好一个Exception
||			step 2.  执行替换        
||			step 3.  把替换后的配置文件更新到 api 包的l10n包中。
被替换的Exception语句为以下格式：
throw new CloudRuntimeException("Caught exception even though it should be handled.", e);
说明：
1、以throw new 开头
2、 CloudStack的常用Exception
3、Exception的参数不限制

替换方法如下：
1、在 utils 中找到 com.tcloud.utils.ESEBCreater 这个类。
       直接运行会出现以下提示：

For example : 
throw new CloudRuntimeException("Caught exception even though it should be handled.", e);
throw new CloudRuntimeException("Caught exception even though it should be handled.", e);

替换后的格式如下：
Replace code:
	//DO NOT CHANGE ID:354946ee381369a52ca00dd4a5d149f5
	CloudRuntimeException _ex_=(CloudRuntimeException) ESECreater.create("CloudRuntimeException", "_B_Caught exception even though it should be handled._E_",e);throw _ex_;
properties code:
	d4ef2697487c3370b17ad887b90f2253="_B_Caught exception even though it should be handled._E_",e
把替换的参数md5=参数的格式，放进配置文件
中文：api\src\com\cloud\l10n\Messages_except_zh_CN.properties
英文：英文的不用放。

最后：替换完成后，发邮件给我备案。

=	=	=	=	=	=	
        
        
=	=	=	=	=	=	4. 要保存好每次替换excetion 的eme文件
||		eme文件的作用：
||		1. 是每次 替换的依据，以后可以据此来进行回滚
||		2. 可以对比翻译人员提交的 翻译后的eme 防止遗漏和重复
||		
||      3. eme文件是按照包生成的，生成的翻译放在properties文件里,名称：Messages_except_zh_CN.properties
||		         放到 api package 下的 l10n中
||		4. 
||		
=	=	=	=	=	=	        
        





第一步：生成翻译配置文件
    cs_formal_generate_eme.py -P package -V  vXXX
第二步：让翻译人员翻译：
    翻译人员完成翻译后，要检查翻译的格式。
    cs_formal_eme_trans_checker.py -P package -V vXXX
    (文件编码：无BOM的utf-8)
第三步：替换源代码中的Throw new
    cs_formal_replace_main.py  -P  -V vXXX
    注意：替换完成后，程序会暂停提示你是否回滚。
            这个时候可以Eclipse刷一下看有没有错误，然后根据需要操作。
第四步：生成properties文件
    (文件编码：无BOM的utf-8)
    cs_formal_gene_eme_properties.py   -P  -V vXXX




代码说明
cs_formal_config.py 是目录配置文件；
cs_formal_generate_eme.py 是生成供翻译人员使用的 Throw new 中英文配置文件；
	     调用格式：Cs_formal_generate_eme.py –P package_name –V version_num
	Cs_formal_replace_main.py  用来做代码替换。
		调用格式：Cs_formal_replace_main.py  –P package_name –V version_num
	Package_name 就是 server,api,core等CloudStack包
	Version_num  是一个名字，按照这个名字保存每次的执行结果，供恢复，备份等。

cs_formal_replace_main.py
	


Exception 的替换类，放到了2个包里：
分别是： utils 和 api ,类名 ESEBCreater.java 和 ESECreater.java

替换的包有5个，分别是：
agent,utils,api,core,server。



-		-		-		-生成  eme 配置文件
eme文件是从Java代码中抽出Throw new 语句生成的文件，供翻译人员使用。
eme文件格式如下：
UUID=a4bbc6ede8570c2d02d53d93fd81a85f
PAKG=api\src\com\cloud\api\commands\AddSwiftCmd.java__##__execute__##__ec0cd3cb91fe82b9501f62a528eb07a9
FROM=throw new ServerApiException(BaseCmd.INTERNAL_ERROR, "Failed to add Swift");__##__fe259409bd9177acec1413ea1f2a3792__##__ServerApiException
T  O=throw new ServerApiException(BaseCmd.INTERNAL_ERROR, "Failed to add Swift");

比如：
源代码中的每一行 throw new  exception 都被替换成了：以下4行。
UUID=165f95ae08416e45833c472604492505
PAKG=server\src\com\cloud\acl\DomainChecker.java__##__checkAccess__##__3666e798822cfe6c58297daee27e509e
FROM=throw new PermissionDeniedException(caller + " does not have permission to operate within domain id=" + domain.getId());__##__12b5be291990bd6e2acec8d44a40c0fd__##__PermissionDeniedException
T  O=throw new PermissionDeniedException(caller + " does not have permission to operate within domain id=" + domain.getId());
对翻译人员的要求：
1、	只能改动以T  O开始的行，其他行不能动；
2、	只改动 T  O 行中：引号内的英文”” 为中文，其他的都不能动。


-		-		-		-生成 properties 配置文件
ExceptionMsg.[cn|en].properties 是国际化替换文件

properties文件从eme配置文件自动生成。
properties的格式：
	md5=_B_错误信息_E__B_错误信息_E__B_错误信息_E_
	比如：
		throw new Exception("a"+ obj.name + "b","c",obj.name+"d");
	英文：md5=_B_a_E__@__B_b_E__#__B_c_E__#__B_d_E_
	中文：md5=_B_国家化_E__@__B_的字符_E__#__B_串_E__#__B_替换_E_

md5产生：
	在Throw new 构造函数中所有字符串相加组成的串。	
	比如：
		throw new Exception("a"+ obj.name + "b","c",obj.name+"d");
	则 md5串为：abcd
	
采用 md5作为key的原因：
	1、 使用md5，一次就可以取到该Exception所有的初始化构造参数
	2、exception太多了，参数原字符长短不齐，还有空格，作为key不适合
	3、在国际化的时候，如果是2个串的组合，一次取到能保留翻译的含义
	4、在下一次CloudStack升级后，凡是Throw new 参数改变都能发现
		
properties文件的生成：
python cs_formal_gene_eme_properties.py -P package -V version -L cn or en
生成文件的依赖：
[package]__eme_generate_config.txt  这个文件。





原来的Exception代码会被替换为：
//
CloudRuntimeException eseee=(CloudRuntimeException) ESECreater.create("CloudRuntimeException","_B_Concurrent operation while trying to allocate resources for the VM_E_",e);throw eseee;





日常开发自动生成工具
	Utils包中：ESEBCreater 类；
	运行后会提示：
		"Enter throw new exception line :
	输入 throw new 的行后会自动生成替换后的代码。
	
	输入 throw new 会生成 替换好的类
 