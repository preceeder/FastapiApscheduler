# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  task_config.py
    Description:  设置固定的定时任务
    Author:      Chenghu
    Date:       2022/3/21 3:33 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
from datetime import date, datetime, timedelta
from apps.utils.time_handler import rest_of_next_half_hour
# interval   类型并不会立马执行， 而是要到下一个执行周期才会开始， 除非设置了  start_time 或 next_run_time=datetime.now()

source_task = [
    {
        # 获取新的书
        'id': 'new_book',
        # 函数相当对于项目所在的位置
        'func': 'apps.tasks.sources.new_book:start_book',
        'args': '',
        'kwargs': {},
        'trigger': 'interval',
        'jobstore': 'source_task',
        'days': 2,  # 间隔时间为 一天
        'start_date': datetime.now() + timedelta(minutes=20),  # 开始执行的时间
        # 'start_date': datetime.now() + timedelta(seconds=20),
        # 'next_run_time':datetime.now()
        # 'hours': 1,
        # 'minutes': 1,
        # 'seconds': 30,
        'replace_existing': True

    },
    {
        # 获取新的电影
        'id': 'new_movie',
        # 函数相当对于项目所在的位置
        'func': 'apps.tasks.sources.new_movie:start_movie',
        'args': '',
        'kwargs': {},
        'trigger': 'interval',
        'days': 2,  # 间隔时间为 一天
        'jobstore': 'source_task',
        'start_date': datetime.now() + timedelta(hours=1),  # 开始执行的时间
        # 'start_date': datetime.now() + timedelta(seconds=10),  # 开始执行的时间
        # 'hours': 1,
        # 'minutes': 1,
        # 'seconds': 30
        'replace_existing': True

    },
    {
        # 获取音乐排行榜
        'id': 'new_music',
        # 函数相当对于项目所在的位置
        'func': 'apps.tasks.sources.hot_top_music:start_music',
        'args': '',
        'kwargs': {},
        'trigger': 'interval',
        'jobstore': 'source_task',
        'days': 2,  # 间隔时间为 一天
        'start_date': datetime.now() + timedelta(hours=2),  # 开始执行的时间
        # 'start_date': datetime.now() + timedelta(seconds=10),  # 开始执行的时间
        # 'hours': 1,
        # 'minutes': 1,
        # 'seconds': 30
        'replace_existing': True

    }
]


JOBS = source_task