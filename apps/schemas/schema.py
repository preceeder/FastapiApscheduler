# -*- coding: UTF-8 -*-
"""
-------------------------------------------------
    File Name:  schema.py
    Description: schema 定义
    Author:      Chenghu
    Date:       2022/3/18 4:45 下午
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
import enum
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Union
from pydantic import BaseModel


class Job(BaseModel):
    id: Union[str, uuid.UUID]  # 任务id, 必须唯一
    name: Optional[str] = None  # 任务的名字
    func: Optional[str] = None  # 任务的方法映射字符串
    args: Optional[Sequence[Optional[str]]] = None  # 任务的 args参数
    kwargs: Optional[Dict[str, Any]] = None  # 任务的kwargs 参数表
    executor: Optional[str] = 'default'     # 执行期
    jobstore: Optional[str] = 'default'     # 存储器
    misfire_grace_time: Optional[int] = 30  # 任务执行的抖动时间
    coalesce: Optional[bool] = False  # 任务是否合并执行
    max_instances: Optional[int] = 1  # 每个任务的最大实例
    next_run_time: Optional[Union[str, datetime]] = None  # 任务的下次执行时间


class RequestJob(Job):
    replace_existing: bool = False
    trigger: Optional[str] = None
    trigger_args: Optional[Dict] = None


# 触发器
class TriggerEnum(str, enum.Enum):
    date = "date"
    interval = "interval"
    cron = "cron"


class Rescheduler(BaseModel):
    id: Union[str, uuid.UUID]
    trigger: TriggerEnum
    trigger_args: Optional[Dict[str, Any]]


class BaseResponse(BaseModel):
    message: str
    status_code: Union[int, str]


class QueryResponse(BaseResponse):
    jobs: List[Job]


class OperateResponse(BaseResponse):
    type: str
