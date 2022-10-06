# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  sale.py
    Description:  
    Author:      Chenghu
    Date:       2022/2/16 2:17 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
from datetime import datetime, date, timedelta


def time_remaining(type_: str = "Day") -> int:
    """
    获取距离指定时间剩余时间
        :param type_: 类型
            Day: 今天剩余时间
            Week: 本周剩余时间
            Month: 月末剩余时间
            Year: 今年剩余时间
    :return 剩余时间的秒数
    """
    type_ = type_.lower()
    now = datetime.now()
    today = datetime.strptime(str(date.today()), "%Y-%m-%d")
    if type_ == "week":
        expecte_time = today - timedelta(days=today.weekday()) + timedelta(days=7)
    elif type_ == "month":
        next_month = today.replace(day=28) + timedelta(days=4)
        expecte_time = next_month - timedelta(days=next_month.day - 1)
    elif type_ == "year":
        expecte_time = datetime(today.year + 1, 1, 1)
    else:
        expecte_time = today + timedelta(days=1)
    time_diff = expecte_time - now
    return time_diff.days * 24 * 3600 + time_diff.seconds


def rest_of_day():
    """
    :return: 截止到目前当日剩余时间
    """
    today = datetime.strptime(str(date.today()), "%Y-%m-%d")
    tomorrow = today + timedelta(days=1)
    nowTime = datetime.now()
    # return (tomorrow - nowTime).microseconds  # 获取毫秒值
    seconds = (tomorrow - nowTime).seconds
    if seconds < 5:
        seconds = 5
    return seconds  # 获取秒


def rest_of_next_half_hour(format="default"):
    """
    获取当前时间到下一个半小时的剩余时间
    format: default 返回剩余的时间戳； strf 返回下一次执行的时间
    """
    now = datetime.now()
    now_minute = now.minute
    now_second = now.second
    if now_minute < 30:
        dif_minute = 30 - now_minute
    else:
        dif_minute = 60 - now_minute

    next_time = now + timedelta(minutes=dif_minute, seconds=-now_second)
    if format == 'default':
        return dif_minute*60 - now_second
    else:
        return next_time.strftime("%Y-%m-%d %H:%M:%S")


def get_timestamp(date_time: str = None, days: int = 0, hours: int = 0, minutes: int = 0):
    """
    获取某一时间的时间戳
    :param date_time: %Y-%m-%d %H:%M:%S
    """
    if date_time:
        ti = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    else:
        ti = datetime.now()

    the_time = ti + timedelta(days=days, hours=hours, minutes=minutes)

    return int(the_time.timestamp())


def get_last_week_start(date=datetime.now()):
    """
    获取上周的周一
    :param date:
    :return:
    """
    last_week_start = date - timedelta(days=date.weekday() + 7)
    return last_week_start.strftime("%Y%m%d")


def target_monday(today, format="%Y%m%d"):
    """
    :function: 获取指定日期所在周的周一日期
    :param today: 指定的日期字符串
    :param format: 日期的字符串格式，用于转为datetime
    :return: 返回周一的日期字符串，格式"%Y%m%d"
    """
    today = datetime.strptime(today, format)
    return datetime.strftime(today - timedelta(today.weekday()), "%Y%m%d")
