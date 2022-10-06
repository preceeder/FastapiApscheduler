# -*- coding: UTF-8 -*-
"""
-------------------------------------------------
    File Name:  common.py
    Description: 通用的公共方法
    Author:      Chenghu
    Date:       2022/3/18 4:45 下午
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

import json
import hashlib
import decimal
from dateutil import tz
from datetime import datetime, timedelta
from typing import Union, Optional, List, Dict
from pytz.tzinfo import DstTzInfo

tz_sh = tz.gettz('Asia/Shanghai')


def get_string_md5(s: str) -> str:
    """
    获取字符串的MD5计算值
        :param s: 待处理的字符串
    :return: MD5值
    """
    md5 = hashlib.md5()
    md5.update(s.encode('utf-8'))
    return md5.hexdigest()


# json 序列化 特殊对象处理
class MyJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime, timedelta)):
            return str(obj)
        elif isinstance(obj, DstTzInfo):
            return str(obj)
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

# 字典列表 合并
def _cal_index_key(rec: dict, index_name: Union[str, list]) -> str:
    if isinstance(index_name, list):
        sk = '_'.join(rec[i] for i in index_name)
    else:
        sk = rec[index_name]
    return sk


def combine(recodes: list, pre_recodes: List, index_key: Union[str, list], default: Optional[Dict] = None) -> list:
    pre_map = {}
    for prec in pre_recodes:
        # 这样即使要融入数据 是多个也能很好的 整合在一起
        pre_map.setdefault(_cal_index_key(prec, index_key),  {}).update(prec)
    # pre_map = {_cal_index_key(prec, index_key): prec for prec in pre_recodes}
    for rec in recodes:
        sk = _cal_index_key(rec, index_key)
        if sk in pre_map:
            if any(set(rec.keys()).intersection(set(pre_map[sk])).difference(
                    index_key if isinstance(index_key, list) else [index_key])):
                raise
            else:
                rec.update(pre_map[sk])
        else:
            # 没有就使用默认值
            if default is not None:
                rec.update(default)
    return recodes
