# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  sale.py
    Description:  
    Author:      Chenghu
    Date:       2022/3/11 1:36 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

# from apps.settings.product.redis_config import Redis_Config
from enum import Enum
from loguru import logger
import json
ENV = None

class Environment(Enum):
    PRODUCT = "product"
    TEST = "test"
    DEV = "dev"


with open('store/env.json', 'r') as f:
    ENV = json.loads(f.read()).get('env', 'test')

if ENV == Environment.PRODUCT.value:
    logger.info("\n当前环境为 生产 环境！")
    from apps.settings.product import *
elif ENV == Environment.TEST.value:
    logger.info("\n当前环境为 测试 发环境！")
    from apps.settings.test import *
elif ENV == Environment.DEV.value:
    logger.info("\n当前环境为 开发 发环境！")
    from apps.settings.dev import *

else:
    raise ValueError("不识别的环境配置，正式环境请使用：product， 测试环境请使用：stag， 开发环境请使用：dev")
