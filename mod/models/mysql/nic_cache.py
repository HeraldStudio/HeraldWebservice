#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-01-09 12:54:58
# @Author  : yml_bright@163.com

from sqlalchemy import Column, String, Integer,Text
from db import engine, Base

class NicCache(Base):
    __tablename__ = 'nic'
    cardnum = Column(Integer, primary_key=True)
    text = Column(Text)
    date = Column(Integer, nullable=False)

