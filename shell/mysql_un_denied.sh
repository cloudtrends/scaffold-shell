#!/bin/bash
mysql dbnane<<EOFMYSQL


 GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '' WITH GRANT OPTION;

FLUSH PRIVILEGES;

EOFMYSQL


