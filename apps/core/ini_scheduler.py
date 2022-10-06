# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  ini_scheduler.py
    Description:  初始化 apscheduler
    Author:      Chenghu
    Date:       2022/3/11 10:11 上午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
import json

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.events import JobEvent, JobExecutionEvent, JobSubmissionEvent
from loguru import logger as aps_logger
from apps.settings.task_config import JOBS
from apps.baseserver import SyncMysqlBaseService
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_MODIFIED, EVENT_JOB_ADDED, EVENT_JOB_REMOVED
from .MysqlJobStore import MysqlJobStore
from apps.settings import ApsMysqlConfig
# from logging import getLogger
from apps.utils.common import MyJsonEncoder
# async_logger = getLogger()
# from loguru import logger


class SchedulerStart:

    def __init__(self):
        self.jobstores = {
            "default": MysqlJobStore(ApsMysqlConfig, table_name="default_task_job"),
            "source_task": MysqlJobStore(ApsMysqlConfig, table_name="source_task",  echo=True),
        }

        self.executors = {
            "default": {"type": "threadpool", "max_workers": 20},  # 使用多线程执行
            "processpool": ProcessPoolExecutor(max_workers=5),  # 使用多进程执行
            # 'asyncio': AsyncIOExecutor()   # 使用 asyncio 执行
            'asyncio': {'type': 'asyncio'}   # 两种方法都行
        }

        self.job_defaults = {
            "coalesce": False,   # 是否合并运行， 错过的任务是否全部运行， False  只运行一次
            "max_instances": 1,  # 同一个任务 最大的任务实例数
            "misfire_grace_time": 60*30  # 超过作业运行时间 一定时间内还可以运行 s， 这样的话也就意味着 超过30s的任务不会在运行， 不设置的话超过30秒也可以运行
        }

        self.scheduler = AsyncIOScheduler()

    def job_error_listener(self, Event: JobExecutionEvent):
        # 结束的任务 拿不到信息
        job = self.scheduler.get_job(Event.job_id)
        aps_logger.error(f'job_id: {Event.job_id}, error: {Event.traceback}')
        if job:
            job_info = job.__getstate__()
            aps_logger.error(f'jon info {job_info}')
            aps_logger.error(f"""jobname={job.name}|jobtrigger={job.trigger}|errcode={Event.code}|
            exception=[{Event.exception}]|traceback=[{Event.traceback}]|scheduled_time={Event.scheduled_run_time}""")
            if job_info.get('trigger'):
                job_info.pop('trigger')
            job_info = json.dumps(job_info, ensure_ascii=False)
        else:
            job_info = None

        SyncMysqlBaseService().insert_or_update(table_name="aps_task_log", values={"job_id": Event.job_id, 'type': 4,
                                                                                 "job_info": job_info})

    def job_addedOrmodify_listener(self, Event: JobEvent):
        job = self.scheduler.get_job(Event.job_id)
        job_info = job.__getstate__()
        if job_info:
            if job_info.get('trigger'):
                job_info.pop('trigger')
            # job_info['trigger'] = job_infojob_info['trigger'].__getstate__() if job_info.get('trigger', None) else ''
            job_data = json.dumps(job_info, cls=MyJsonEncoder)
        else:
            job_data = None
        SyncMysqlBaseService().insert_or_update(table_name="aps_task_log", values={"job_id": Event.job_id, 'type': 0,
                                                                                 "job_info": job_data})

    def job_remove_listener(self, Event: JobEvent):
        # 删除任务监听
        SyncMysqlBaseService().insert_or_update(table_name="aps_task_log", values={"job_id": Event.job_id, 'type': 1,
                                                                                 "job_info": None})

    async def init_scheduler(self):
        other_config = {
            "timezone": 'Asia/Shanghai',
            "logger": aps_logger
        }
        self.scheduler.configure(jobstores=self.jobstores, executors=self.executors,
                                 job_defaults=self.job_defaults, **other_config)
        # self.scheduler.configure(jobstores=self.jobstores, job_defaults=self.job_defaults, logger=logger)

        self.scheduler.add_listener(self.job_error_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED)
        self.scheduler.add_listener(self.job_addedOrmodify_listener, EVENT_JOB_MODIFIED | EVENT_JOB_ADDED)
        self.scheduler.add_listener(self.job_remove_listener, EVENT_JOB_REMOVED)
        self.scheduler.start()
        aps_logger.info("apps is running...")

    async def add_config_job(self):
        """加载本地配置好的 定时任务"""
        self.init_db()
        for job in JOBS:
            sd = self.scheduler.add_job(**job)
            aps_logger.info(f'添加任务： {job["id"]}, {sd}')

    def init_db(self):
        sql = """
            CREATE TABLE IF NOT EXISTS `aps_task_log` (
              `id` bigint(20) NOT NULL AUTO_INCREMENT,
              `job_id` varchar(191) COLLATE utf8mb4_general_ci NOT NULL,
              `job_info` json DEFAULT NULL,
              `type` tinyint(3) DEFAULT NULL COMMENT '1 删除｜0添加或修改｜ 错误 4',
              `creamt_time` datetime DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`),
              KEY `task_log_job_id_idx` (`job_id`) USING BTREE
            ) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """
        SyncMysqlBaseService().execute(sql=sql)


scheduler_init = SchedulerStart()
scheduler = scheduler_init.scheduler
