# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  log.py
    Description:  初始化日志
    Author:      Chenghu
    Date:       2022/3/11 10:11 上午
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

from pathlib import Path
from loguru import logger
from apps.settings.settings import LOG


def create_log_dir() -> Path:
    """创建日志文件所在目录"""
    parent = Path(LOG.get('path', 'logs/out.log'))
    file_name, pa_dir = [parent.name, parent.parent] if '.' in parent.name else ['', parent]
    file_name = file_name if file_name else "out.log"
    log_file = pa_dir.joinpath(file_name)
    return log_file


logger_handle = logger.add(create_log_dir(),
                           format="{time:HH:mm:ss.SSS} | {level} | {name}.{function}| {line} | {message}",
                           catch=True,          # 是否应自动捕获接收器处理日志消息时发生的错误
                           enqueue=True,        # 要记录的消息是否应在到达接收器之前首先通过多进程安全队列
                           rotation="00:00",    # 指示何时应关闭当前记录的文件并开始新的文件
                           encoding="utf-8",    # 指定日志文件的编码方式
                           retention="7 days"  # 保留7天后删除
                           )
