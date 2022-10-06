# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  db_config.py
    Description:  
    Author:      Chenghu
    Date:       2022/5/23 9:17 上午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
# 业务的数据库配置
BusinessConfig = {
    "default": {
        "host": '121.4.108.200',
        "port": 3306,
        "user": 'root',
        "pwd": '123456',
        "db": "test_001",
        "recycle": 30
    },
}

# apscheduler的数据库配置
ApsMysqlConfig = {
    "host": '121.4.108.200',
    "port": 3306,
    "user": 'root',
    "pwd": '123456',
    "db": "test_001",
    "recycle": 30
}

# DB  表明到数据库的映射
TABLE_DB_MAP = {
    'table_name': "default"
}
