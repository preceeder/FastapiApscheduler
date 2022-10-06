# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  __init__.py
    Description:  路由处理
    Author:      Chenghu
    Date:       2022/2/11 3:09 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
import importlib
import os
from pathlib import Path
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger


class GetRouters:
    def __init__(self, app: FastAPI):
        """
        自动生成路由配置，并添加到API中
            :param app: FastAPI 实例对象
        """
        self._app = app

    def load_router(self, p: Path, app_module: str):
        """导入指定目录下的路由文件"""
        file_name = p.name
        if not file_name.startswith("_"):
            # 导入 routers 目录下所有 非_ 作为起始文件名的模块
            file_name_no_suffix = p.stem
            try:
                moudle_path = f'apps.routers.{app_module}.{file_name_no_suffix}' if app_module else f'apps.routers.{file_name_no_suffix}'
                moudle = importlib.import_module(moudle_path)
            except ImportError as error:
                logger.warning(f"导入路由文件{file_name_no_suffix}失败：{error}")
                return
            # 跳过设置不自动解析的文件
            if getattr(moudle, "__no_router__", None):
                return
            _prefix = getattr(moudle, "__router_prefix__", None)
            if _prefix or _prefix == "":
                router_prefix = _prefix
            else:
                router_prefix = f"/api/{app_module}/{file_name_no_suffix}" if app_module else f"/api/{file_name_no_suffix}"

            # 直接获取 router 变量
            if hasattr(moudle, "router") and isinstance(router := getattr(moudle, "router"), APIRouter):
                self._app.include_router(router, prefix=router_prefix,
                                         tags=[f"{file_name_no_suffix.capitalize()}"])
                return
            # 解析 __router__ 变量
            elif hasattr(moudle, "__router__"):
                router = getattr(moudle, "__router__")
                if isinstance(router, str):
                    router = getattr(moudle, router)
                if isinstance(router, APIRouter):
                    self._app.include_router(router, prefix=router_prefix,tags=[f"{file_name_no_suffix.capitalize()}"])
                    return
            # 倒序解析模块下所有实例变量
            for ins in dir(moudle)[::-1]:
                if not ins.startswith("_") and not ins[0].isupper() and isinstance(
                        router := getattr(moudle, ins), APIRouter):
                    self._app.include_router(router, prefix=router_prefix,
                                             tags=[f"{file_name_no_suffix.capitalize()}"])
                    break

    async def set_routers(self):
        """
        获取routers目录下所有可导入的路由
        """
        parent = Path('apps/routers')
        for x in parent.iterdir():
            if x.exists() and x.is_dir():
                # 搜索 routers 目录下所有 py 文件
                for p in x.glob('*.py'):
                    self.load_router(p, app_module=x.name)
            elif x.exists() and x.is_file():
                self.load_router(x, app_module="")

    def mount_static_files(self):
        """
        挂载静态文件
        """
        self._app.mount("/static", StaticFiles(directory="static"), name="static")

    def set_cros(self):
        """
        添加 CORS 跨域访问
        """
        origins = [
            "*"
        ]
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def set_other_routers(self):
        """
        手动导入其他路由
        """
        pass


async def create_router(app: FastAPI):
    """
    创建APP的路由相关信息
        :param app: FastAPI实例对象
    """
    router = GetRouters(app)
    router.set_cros()
    await router.set_routers()
    router.mount_static_files()
    router.set_other_routers()