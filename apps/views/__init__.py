# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  __init__.py
    Description:  
    Author:      Chenghu
    Date:       2022/3/16 3:19 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
import json
from typing import Union
from copy import deepcopy
from datetime import datetime


def data_format(data: Union[list, dict], default_data: dict = {}, replace: dict = {}, op_data: dict = {}):
    _data = deepcopy(data)
    if isinstance(_data, dict):
        _data = [_data]
    for value in _data:
        v_keys = value.keys()
        # 先把数据补齐
        if default_data:
            d_keys = default_data.keys()
            v_keys = set(d_keys) - set(v_keys)
            for _de in v_keys:
                value[_de] = default_data[_de]

        # 然后在数据替换
        for key, it in value.items():
            if it is None:
                value[key] = ''

            if key in default_data and it == '' or it is None:
                value[key] = default_data.get(key, '')
            if key in replace:
                value[key] = replace[key].get(value[key], '')

            if key in op_data and value[key] is not None:
                "对数据做具体的操作， json.loads"
                try:
                    opd = op_data[key].format(value[key])
                except Exception as e:
                    opd = op_data[key]
                try:
                    value[key] = eval(opd)
                except Exception as e:
                    pass

                # value[key] = op_data[key](value[key])

    if isinstance(data, dict):
        return _data[0]
    return _data