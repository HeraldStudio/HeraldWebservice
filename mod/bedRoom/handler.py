#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-08-24 12:46:36
# @Author  : LiangJ

import base64
import json
from time import time

import tornado.gen
import tornado.web
from BeautifulSoup import BeautifulSoup
from sqlalchemy.orm.exc import NoResultFound
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

from config import *
from mod.models.mysql.room_cache import RoomCache
from ..auth.handler import authApi


class RoomHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    def on_finish(self):
        self.db.close()
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        number = self.get_argument('number',default=None)
        retjson = {'code':200, 'content':''}
        data = {
            'Login.Token1':number,
            'Login.Token2':self.get_argument('password'),
        }

        # read from cache
        try:
            status = self.db.query(RoomCache).filter(RoomCache.cardnum == number).one()
            if status.date > int(time())-10000 and status.text != '*':
                self.write(base64.b64decode(status.text))
                self.finish()
                return
        except NoResultFound:
            status = RoomCache(cardnum = number,text = '*',date = int(time()))
            self.db.add(status)
            try:
                self.db.commit()
            except:
                self.db.rollback()

        try:
            client = AsyncHTTPClient()
            response = authApi(number,self.get_argument("password"))
            
            if response['code'] == 200:
                cookie = response['content']
                request = HTTPRequest(
                    URL,
                    method='GET',
                    headers={'Cookie': cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                table2 = soup.findAll('td')
                room = table2[9].text
                bed = table2[10].text
                retjson['code'] = 200
                retjson['content'] = {
                    'bed': bed,
                    'room': room
                }
            else:
                retjson['code'] = 401
        except Exception,e:
            retjson['code'] = 200
            retjson['content'] = {'bed': "",'room': ""}
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(ret)
        self.finish()

        # refresh cache
        if retjson['code'] == 200:
            status.date = int(time())
            status.text = base64.b64encode(ret)
            self.db.add(status)
            try:
                self.db.commit()
            except Exception,e:
                self.db.rollback()
            finally:
                self.db.remove()

        