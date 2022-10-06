# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  __init__.py
    Description:  
    Author:      Chenghu
    Date:       2022/3/11 1:45 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

from apps.dbdriver.redis import get_redis_connect_pool, get_sync_redis_connect_pool
from apps.dbdriver.mysql import get_database_pool, get_async_database_pool

redis = get_redis_connect_pool()
sync_redis = get_sync_redis_connect_pool()
mysql = get_database_pool()
async_mysql = get_async_database_pool()