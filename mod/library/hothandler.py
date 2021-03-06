# -*- coding: utf-8 -*-
# @Date    : 2016-03-14 17:34:57
# @Author  : jerry.liangj@qq.com
import base64
import json
import re
from time import time

import tornado.gen
import tornado.web
from BeautifulSoup import BeautifulSoup
from sqlalchemy.orm.exc import NoResultFound
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

from config import TIME_OUT
from mod.models.mysql.library import LibraryHotCache


class HotHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db
    def on_finish(self):
        self.db.close()

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        HOT_URL = "http://www.libopac.seu.edu.cn:8080/top/top_lend.php"
        retjson = {
            'code':200,
            'content':''
        }
        try:
            status = self.db.query(LibraryHotCache).one()
            if status.date > int(time())-600000:
                self.write(base64.b64decode(status.text))
                self.db.close()
                self.finish()
                return
        except NoResultFound:
            status = LibraryHotCache(text='*', date=int(time()))

        try:
            client = AsyncHTTPClient()
            request = HTTPRequest(
                HOT_URL,
                method='GET',
                request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            soup = BeautifulSoup(response.body)
            td = soup.findAll('td', {'class': 'whitetext'})
            ret = []
            length = 80 if len(td)>80 else len(td)
            for i in range(0, length, 8):
                s = td[i+1].text.split('/')
                book = {
                    'name': self.entity_parser(td[i+1].text),
                    'author':self.entity_parser(td[i+2].text),
                    'count':td[i+6].text,
                    'place': self.entity_parser(td[i+4].text),
                }
                ret.append(book)
            retjson['content'] = ret
        except:
            retjson['code'] = 500
            retjson['content'] = 'error'
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()

        # refresh cache
        if retjson['code'] == 200:
            status.date = int(time())
            status.text = base64.b64encode(ret)
            self.db.add(status)
            try:
                self.db.commit()
            except:
                self.db.rollback()
            finally:
                self.db.remove()

    def entity_parser(self, string):
        x = re.findall('&#x(.{4});', string)
        s = ''
        for c in x:
            s += unichr(int(c,16))
        return s


