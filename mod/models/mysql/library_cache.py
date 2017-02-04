# -*- coding: utf-8 -*-
# @Date    : 2016/9/20  21:35
# @Author  : 490949611@qq.com
from sqlalchemy import Column, String, Integer,Text
from db import engine, Base

class ListLibrary(Base):
    __tablename__ = 'library'
    cardnum = Column(Integer, primary_key=True)
    text = Column(Text)
    date = Column(Integer, nullable=False)