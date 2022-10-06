# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  table.py
    Description:  数字格式化输出
    Author:      Chenghu
    Date:       2022/3/18 4:45 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""


def cal_percent(a, b, error_value=0):
    if a is None or b is None:
        return error_value
    try:
        e = float(a)/(float(b))
    except ZeroDivisionError:
        return error_value
    except BaseException:
        return error_value
    else:
        return float(e)


def float_2_str(value, fix=2, fillna='--', split=None, **kwargs):
    if isinstance(value, list):
        return [_format_str(v, fix=fix, fillna=fillna, split=split) for v in value]
    else:
        return _format_str(value, fix=fix, fillna=fillna, split=split)


def _format_str(value, fix=2, fillna='--', split=None):
    if isinstance(value, str):
        return value
    if value < 0:
        return fillna
    else:
        if split == ',':
            fmt = '{:,.' + str(fix) + 'f}'
        else:
            fmt = '{:.0' + str(fix) + 'f}'
        return fmt.format(value)