# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  __init__.py
    Description:  
    Author:      Chenghu
    Date:       2022/3/11 1:35 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
from pydantic import BaseModel


class Page(BaseModel):
    page: int = 0
    size: int = 20