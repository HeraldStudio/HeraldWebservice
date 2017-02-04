#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-23 09:51:00
# @Author  : jerry.liangj@qq.com

import json, traceback
import tornado
from log import getLogger
from utils.RedisUtils import read_from_cache

log = getLogger("webservice")

class CommonHandler(tornado.web.RequestHandler):
    """api查询
       CommonHandler中的api均通过爬虫队列进行获取
    """

    @property
    def db(self):
        return self.application.db

    def on_finish(self):
        self.db.close()

    @property
    def unitsmap(self):
        return {
            'card': self.card,
            'exam': self.exam,
            'gpa': self.gpa,
            'lecture': self.lecture,
            'library': self.library,
            'nic': self.nic,
            'pedetail': self.pedetail,
            'phyLab': self.phylab,
            'room': self.room,
            'srtp': self.srtp
        }

    def get(self, API):
        self.write('Herald Web Service')

    def post(self, API):
        try:
            self.unitsmap[API]()
        except KeyError:
            self.write("This is an error request, Check!!!")
            # raise tornado.web.HTTPError(400)       # 防止向客户端返回详细错误
        except Exception, e:
            log.error("%s-%s\n%s" % (self.get_argument('cardnum', default=None), API, traceback.print_exc()))
            retjson = {"code": 500, "content": str(e)}
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
            self.finish()

    def card(self):
        cardnum = self.get_argument('cardnum', default=None)
        password = self.get_argument('password', default=None)
        timedelta = self.get_argument('timedelta', default=0)
        retjson = read_from_cache(self.db, "card", cardnum, password, {"timedelta": timedelta})
        self.write(retjson)
        self.finish()

    def srtp(self):
        number = self.get_argument('number', default=None)
        retjson = read_from_cache(self.db, "srtp", number)
        self.write(retjson)
        self.finish()

    def exam(self):
        cardnum = self.get_argument('cardnum', default=None)
        password = self.get_argument('password', default=None)
        retjson = read_from_cache(self.db, "exam", cardnum, password)
        self.write(retjson)
        self.finish()

    def gpa(self):
        cardnum = self.get_argument('username', default=None)
        password = self.get_argument('password', default=None)
        retjson = read_from_cache(self.db, "gpa", cardnum, password)
        self.write(retjson)
        self.finish()

    def lecture(self):
        cardnum = self.get_argument('cardnum', default=None)
        password = self.get_argument('password', default=None)
        retjson = read_from_cache(self.db, "lecture", cardnum, password)
        self.write(retjson)
        self.finish()

    def library(self):
        cardnum = self.get_argument('cardnum', default=None)
        password = self.get_argument('password', default=None)
        retjson = read_from_cache(self.db, "library", cardnum, password)
        self.write(retjson)
        self.finish()

    def nic(self):
        cardnum = self.get_argument('cardnum', default=None)
        password = self.get_argument('password', default=None)
        retjson = read_from_cache(self.db, "nic", cardnum, password)
        self.write(retjson)
        self.finish()

    def pedetail(self):
        cardnum = self.get_argument('cardnum', default=None)
        password = self.get_argument('password', default=None)
        retjson = read_from_cache(self.db, "pedetail", cardnum, password)
        self.write(retjson)
        self.finish()

    def phylab(self):
        cardnum = self.get_argument('number', default=None)
        password = self.get_argument('password', default=None)
        term = self.get_argument('term', default=None)
        retjson = read_from_cache(self.db, "phylab", cardnum, password, {"term": term})
        self.write(retjson)
        self.finish()

    def room(self):
        cardnum = self.get_argument('number', default=None)
        password = self.get_argument('password', default=None)
        retjson = read_from_cache(self.db, "room", cardnum, password)
        self.write(retjson)
        self.finish()
