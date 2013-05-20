#!/bin/bash


echo "remove no need templates"



#mysql> select id,name from vm_template;
#+-----+------------------------------------------+
#| id  | name                                     |
#+-----+------------------------------------------+
#|   1 | SystemVM Template (XenServer)            |
#|   2 | CentOS 5.3(64-bit) no GUI (XenServer)    |
#|   3 | SystemVM Template (KVM)                  |
#|   4 | CentOS 5.5(64-bit) no GUI (KVM)          |
#|   5 | CentOS 5.6(64-bit) no GUI (XenServer)    |
#|   7 | CentOS 5.3(64-bit) no GUI (vSphere)      |
#|   8 | SystemVM Template (vSphere)              |
#|   9 | SystemVM Template (HyperV)               |
#| 100 | ApplianceVM Template (XenServer)         |
#| 101 | Monitor ApplianceVM Template (XenServer) |
#| 102 | Monitor ApplianceVM Template (KVM)       |
#| 103 | Monitor ApplianceVM Template (VMware)    |
#| 200 | xs-tools.iso                             |
#| 201 | vmware-tools.iso                         |
#| 202 | centos-mini                              |
#+-----+------------------------------------------+
#15 rows in set (0.00 sec)



mysql -uroot  -e 'show databases;'


mysql -uroot -e 'use cloud;SELECT COUNT(*) FROM vm_template ' 
mysql -uroot -e 'use cloud;SELECT id,name FROM vm_template ' 

mysql -uroot -e 'use cloud;SELECT id , host_id , template_id   FROM template_host_ref ' 



mysql -uroot -e 'use cloud;delete FROM template_host_ref where template_id = 2 or template_id = 4 or template_id = 5 or template_id = 7 ' 
mysql -uroot -e 'use cloud;delete FROM vm_template where id = 2 or id = 4 or id = 5 or id = 7 ' 
mysql -uroot -e 'use cloud;delete FROM vm_template where id = 4 ' 
mysql -uroot -e 'use cloud;delete FROM vm_template where id = 5 ' 
mysql -uroot -e 'use cloud;delete FROM vm_template where id = 7 ' 
mysql -uroot -e 'use cloud;delete FROM vm_template where id = 2 ' 
