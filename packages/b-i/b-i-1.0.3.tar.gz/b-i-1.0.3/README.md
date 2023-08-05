b-i
======

BI tools  for data developer use Python Language. 更快捷的BI数据开发工具

[![Build Status](https://img.shields.io/travis/otale/tale.svg?style=flat-square)](https://github.com/cppla/dblib)
[![](https://img.shields.io/badge/python-3.6%2B%20-blue.svg)](https://github.com/cppla/dblib)
[![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg?style=flat-square)](https://github.com/cppla/dblib)

用法
========

安装
```
pip3 install b-i
```

修改数据库配置文件
```
vim ~/.b-i
```

快速查询
```
from b_i import hive_client
hive_client.read_sql("show tables")

from b_i import mysql_client
mysql_client.read_sql("show tables")
```


高级示例
========

b_i 数据开发工具包维护了三个操作对象:   

hive数据库操作对象：hive_client   
mysql数据库操作对象：mysql_client    
elasticsearch数据库操作对象：elastic_client      


提供两个常用方法:    
 
read_sql()    
exec_sql()    
