
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
��ע��
    eme �����ļ��ǣ�ExceptionMapEntry ����д��ÿ��throw new exception
                    ����Ӧ eme  �����ļ���һ�
    �汾�ţ��汾���Ǳ��β�����һ����ʶ�����������ݣ��ع��á�
            ÿ���汾�Ŷ�Ӧһ��Ŀ¼�����еĲ�����¼���������Ŀ¼�
            
            
            
=	=	=	=	=	=	3. Exception �滻�ķ�ʽ��һ���滻ֻ���һ��package��
|| ��һ�֣� ��packageΪ��λ�����滻		
||			cs_formal_generate_eme.py -P package -V  vXXX	
|| �ڶ��֣��� ĳ���ļ����򼸸��ļ�Ϊ��λ�����滻������״̬���úܷ��㣩
||			�ο�cs_formal_config.py �����ļ�
|| �����֣��滻ĳ������һ���ļ� �������滻���߿������滻��
||			ָ�������ļ��б���ļ��� ( ��-Fָ������� java source code  �ļ��б�)
|| 			python cs_formal_generate_eme.py -P server -Vb -F X:xxx.txt
||			�ļ��б�ĸ�ʽ��ؼ�����java�ļ�����
||	ÿ���滻��Ҫһ�� version �������ظ�����ֹ������ǰ�滻��eme�ļ���
||  ÿ���滻����eme��Ҫ���ݵ������档
|| �������ַ�����ÿ�����ɵ�eme����api package�� l10n �¡�
|| 			 
||			�ļ����ֱ�Ϊ���� ��package һһ��Ӧ��
||			utils__eme_generate_config.txt
||			server__eme_generate_config.txt
||			core__eme_generate_config.txt
||			api__eme_generate_config.txt
||			agent__eme_generate_config.txt
||			����package����ÿ�β����� eme �ϲ�����Ӧ��eme�ļ��С�
||			( ���磺ִ����һ��������exception�滻����ô�����ɵ� eme �����ļ��ϲ�����Ӧ���ļ��С� )
|| ����: ����һ���Ѿ����ڵı��滻����Exception update ONE already exist replaced exception
||		  purpose : amend the english exception message 
		    ���磺��Ҫ�޸�Exception�е���ʾ��Ϣ��  
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
|| ���壺 ����һ��Exception
||			step 1.  д��һ��Exception
||			step 2.  ִ���滻        
||			step 3.  ���滻��������ļ����µ� api ����l10n���С�
���滻��Exception���Ϊ���¸�ʽ��
throw new CloudRuntimeException("Caught exception even though it should be handled.", e);
˵����
1����throw new ��ͷ
2�� CloudStack�ĳ���Exception
3��Exception�Ĳ���������

�滻�������£�
1���� utils ���ҵ� com.tcloud.utils.ESEBCreater ����ࡣ
       ֱ�����л����������ʾ��

For example : 
throw new CloudRuntimeException("Caught exception even though it should be handled.", e);
throw new CloudRuntimeException("Caught exception even though it should be handled.", e);

�滻��ĸ�ʽ���£�
Replace code:
	//DO NOT CHANGE ID:354946ee381369a52ca00dd4a5d149f5
	CloudRuntimeException _ex_=(CloudRuntimeException) ESECreater.create("CloudRuntimeException", "_B_Caught exception even though it should be handled._E_",e);throw _ex_;
properties code:
	d4ef2697487c3370b17ad887b90f2253="_B_Caught exception even though it should be handled._E_",e
���滻�Ĳ���md5=�����ĸ�ʽ���Ž������ļ�
���ģ�api\src\com\cloud\l10n\Messages_except_zh_CN.properties
Ӣ�ģ�Ӣ�ĵĲ��÷š�

����滻��ɺ󣬷��ʼ����ұ�����

=	=	=	=	=	=	
        
        
=	=	=	=	=	=	4. Ҫ�����ÿ���滻excetion ��eme�ļ�
||		eme�ļ������ã�
||		1. ��ÿ�� �滻�����ݣ��Ժ���Ծݴ������лع�
||		2. ���ԶԱȷ�����Ա�ύ�� ������eme ��ֹ��©���ظ�
||		
||      3. eme�ļ��ǰ��հ����ɵģ����ɵķ������properties�ļ���,���ƣ�Messages_except_zh_CN.properties
||		         �ŵ� api package �µ� l10n��
||		4. 
||		
=	=	=	=	=	=	        
        





��һ�������ɷ��������ļ�
    cs_formal_generate_eme.py -P package -V  vXXX
�ڶ������÷�����Ա���룺
    ������Ա��ɷ����Ҫ��鷭��ĸ�ʽ��
    cs_formal_eme_trans_checker.py -P package -V vXXX
    (�ļ����룺��BOM��utf-8)
���������滻Դ�����е�Throw new
    cs_formal_replace_main.py  -P  -V vXXX
    ע�⣺�滻��ɺ󣬳������ͣ��ʾ���Ƿ�ع���
            ���ʱ�����Eclipseˢһ�¿���û�д���Ȼ�������Ҫ������
���Ĳ�������properties�ļ�
    (�ļ����룺��BOM��utf-8)
    cs_formal_gene_eme_properties.py   -P  -V vXXX




����˵��
cs_formal_config.py ��Ŀ¼�����ļ���
cs_formal_generate_eme.py �����ɹ�������Աʹ�õ� Throw new ��Ӣ�������ļ���
	     ���ø�ʽ��Cs_formal_generate_eme.py �CP package_name �CV version_num
	Cs_formal_replace_main.py  �����������滻��
		���ø�ʽ��Cs_formal_replace_main.py  �CP package_name �CV version_num
	Package_name ���� server,api,core��CloudStack��
	Version_num  ��һ�����֣�����������ֱ���ÿ�ε�ִ�н�������ָ������ݵȡ�

cs_formal_replace_main.py
	


Exception ���滻�࣬�ŵ���2�����
�ֱ��ǣ� utils �� api ,���� ESEBCreater.java �� ESECreater.java

�滻�İ���5�����ֱ��ǣ�
agent,utils,api,core,server��



-		-		-		-����  eme �����ļ�
eme�ļ��Ǵ�Java�����г��Throw new ������ɵ��ļ�����������Աʹ�á�
eme�ļ���ʽ���£�
UUID=a4bbc6ede8570c2d02d53d93fd81a85f
PAKG=api\src\com\cloud\api\commands\AddSwiftCmd.java__##__execute__##__ec0cd3cb91fe82b9501f62a528eb07a9
FROM=throw new ServerApiException(BaseCmd.INTERNAL_ERROR, "Failed to add Swift");__##__fe259409bd9177acec1413ea1f2a3792__##__ServerApiException
T  O=throw new ServerApiException(BaseCmd.INTERNAL_ERROR, "Failed to add Swift");

���磺
Դ�����е�ÿһ�� throw new  exception �����滻���ˣ�����4�С�
UUID=165f95ae08416e45833c472604492505
PAKG=server\src\com\cloud\acl\DomainChecker.java__##__checkAccess__##__3666e798822cfe6c58297daee27e509e
FROM=throw new PermissionDeniedException(caller + " does not have permission to operate within domain id=" + domain.getId());__##__12b5be291990bd6e2acec8d44a40c0fd__##__PermissionDeniedException
T  O=throw new PermissionDeniedException(caller + " does not have permission to operate within domain id=" + domain.getId());
�Է�����Ա��Ҫ��
1��	ֻ�ܸĶ���T  O��ʼ���У������в��ܶ���
2��	ֻ�Ķ� T  O ���У������ڵ�Ӣ�ġ��� Ϊ���ģ������Ķ����ܶ���


-		-		-		-���� properties �����ļ�
ExceptionMsg.[cn|en].properties �ǹ��ʻ��滻�ļ�

properties�ļ���eme�����ļ��Զ����ɡ�
properties�ĸ�ʽ��
	md5=_B_������Ϣ_E__B_������Ϣ_E__B_������Ϣ_E_
	���磺
		throw new Exception("a"+ obj.name + "b","c",obj.name+"d");
	Ӣ�ģ�md5=_B_a_E__@__B_b_E__#__B_c_E__#__B_d_E_
	���ģ�md5=_B_���һ�_E__@__B_���ַ�_E__#__B_��_E__#__B_�滻_E_

md5������
	��Throw new ���캯���������ַ��������ɵĴ���	
	���磺
		throw new Exception("a"+ obj.name + "b","c",obj.name+"d");
	�� md5��Ϊ��abcd
	
���� md5��Ϊkey��ԭ��
	1�� ʹ��md5��һ�ξͿ���ȡ����Exception���еĳ�ʼ���������
	2��exception̫���ˣ�����ԭ�ַ����̲��룬���пո���Ϊkey���ʺ�
	3���ڹ��ʻ���ʱ�������2��������ϣ�һ��ȡ���ܱ�������ĺ���
	4������һ��CloudStack�����󣬷���Throw new �����ı䶼�ܷ���
		
properties�ļ������ɣ�
python cs_formal_gene_eme_properties.py -P package -V version -L cn or en
�����ļ���������
[package]__eme_generate_config.txt  ����ļ���





ԭ����Exception����ᱻ�滻Ϊ��
//
CloudRuntimeException eseee=(CloudRuntimeException) ESECreater.create("CloudRuntimeException","_B_Concurrent operation while trying to allocate resources for the VM_E_",e);throw eseee;





�ճ������Զ����ɹ���
	Utils���У�ESEBCreater �ࣻ
	���к����ʾ��
		"Enter throw new exception line :
	���� throw new ���к���Զ������滻��Ĵ��롣
	
	���� throw new ������ �滻�õ���
 