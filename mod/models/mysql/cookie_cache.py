#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-03-24 12:46:36
# @Author  : jerry.liangj@qq.com
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import engine,Base

class CookieCache(Base):
    __tablename__ = 'cookie'
    cardnum = Column(Integer, primary_key=True)
    cookie = Column(String(256), nullable=False)
    date = Column(Integer, nullable=False)
