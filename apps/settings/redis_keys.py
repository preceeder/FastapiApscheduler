# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  redis_keys.py
    Description:  redis key 定义
    Author:      Chenghu
    Date:       2022/3/17 5:13 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
from apps.utils.time_handler import rest_of_day, rest_of_next_half_hour
REDIS_11 = '11'
REDIS_12 = '12'
REDIS_13 = '13'

# 推荐动态 缓存
RECOMMEND_FEED = {
    "db": REDIS_13,
    "key": "feed:recommend:all",
    "exp": rest_of_next_half_hour  # key的过期时间
}
