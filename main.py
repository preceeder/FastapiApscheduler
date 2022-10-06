# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  main.py
    Description:  
    Author:      Chenghu
    Date:       2022/3/11 10:13 上午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from apps.core.ini_scheduler import scheduler_init
from apps.core.log import logger_handle
from apps.schemas.response import HttpException
from loguru import logger
import time
from apps.routers import create_router
from apps.dbdriver import mysql, redis, sync_redis  #  , arq_worker
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)


# 初始化API
app = FastAPI(
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/app/api/redoc",
    title="FastapiApscheduler",
    description="fastapi apscheduler时任务",
)

@app.on_event("startup")
async def startup():
    """
    APP启动配置
        1. 异步启动数据库连接池
        2. 异步启动Redis连接池
    """

    for key, db in mysql.items():
        await db.connect_pool()

    for rdb, pool in redis.items():
        await pool.redis_connect_pool()

    for sy_db, sy_pool in sync_redis.items():
            sy_pool.redis_connect_pool()

    # 初始化 定时器
    await scheduler_init.init_scheduler()
    logger.info('开始加载 静态任务')
    await scheduler_init.add_config_job()

    # 导入路由
    await create_router(app)

    logger.info(
        f"********************  START:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))} ********************")


@app.get("/app/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.on_event("shutdown")
async def shutdown():
    """
    APP停止运行时配置
        1. 异步关闭数据库连接池
        2. 异步关闭Redis连接池
    """
    try:
        for key, db in mysql.items():
            logger.info(f"关闭数据库连接池 {key}")
            await db.close()
    except Exception as error:
        logger.error(error)
    try:
        logger.info("关闭Redis连接池")
        for rdb, pool in redis.items():
            logger.info(f"关闭redis连接池:{rdb}")
            await pool.close()

        for rdb, pool in sync_redis.items():
            logger.info(f"关闭sync_redis连接池: {rdb}")
            pool.close()
    except Exception as error:
        logger.error(error)

    try:
        logger.info(f"*********  END:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))} *********")
    except:
        pass


#  注册捕获异常
@app.exception_handler(HttpException)
async def unicorn_exception_handler(request: Request, exc: HttpException):
    """服务异常捕获处理程序"""
    if exc.code == 500:
        try:
            kwargs = {
                "error": exc.error,
                "url": request.url.path,
                "method": request.method,
                "host": request.client.host,
                "path": request.path_params,
                "query": request.query_params,
            }
            logger.critical(f""" 请求出现错误,详细信息如下：

                {kwargs}
            """)
        except Exception as error:
            logger.error(f"处理异常消息错误：{error}")
    return JSONResponse(
        status_code=401 if exc.code == 401 else 200,
        content={
            "code": exc.code,
            "success": False,
            "msg": exc.message
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """服务实体校验错误捕获程序"""
    url = request.url.path
    method = request.method
    host = request.client.host
    err = f"""
        Host: {host}
        URL Path: {method} {url}
        Body:
            {exc.body}
        Error:
            {exc.errors()}
    """
    logger.critical(f""" 请求参数实体解析出现错误,详细信息如下：
        {err}
    """)
    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "success": False,
            "msg": "参数错误！",
        },
    )


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=5100, debug=False, reload=False)