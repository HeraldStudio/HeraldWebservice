#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-01-09 12:11:23
# @Author  : yml_bright@163.com

from sqlalchemy import Column, String, Integer, Text
from db import engine, Base

class LectureCache(Base):
    __tablename__ = 'lecture'
    cardnum = Column(Integer, primary_key=True)
    text = Column(Text)
    date = Column(Integer, nullable=False)
