# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  __init__.py
    Description:  使用orm框架的时候可以用到这个
    Author:      Chenghu
    Date:       2022/3/11 2:02 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
# 目前基本没有使用

from sqlalchemy.ext.declarative import declarative_base


def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# 创建基类
Base = declarative_base()


Base.to_dict = to_dict


