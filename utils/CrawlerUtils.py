#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-23 09:51:00
# @Author  : jerry.liangj@qq.com


from gevent import monkey

monkey.patch_all()
import gevent

from mod.models.redis.redis_db import redis_job
from mod.models.redis.redis_db import redis_cache

from mod.models.mysql.card_cache import CardCache
from mod.models.mysql.exam_cache import ExamCache
from mod.models.mysql.gpa_cache import GpaCache
from mod.models.mysql.lecture_cache import LectureCache
from mod.models.mysql.library_cache import ListLibrary
from mod.models.mysql.nic_cache import NicCache
from mod.models.mysql.pe_models import PeDetailCache
from mod.models.mysql.phylab_cache import PhylabCache
from mod.models.mysql.room_cache import RoomCache
from mod.models.mysql.srtp_cache import SRTPCache
from mod.models.mysql.jwc_cache import JWCCache
from mod.models.mysql.user_detail import UserDetail

from mod.models.mysql.db import mysql_db

from config import *
from log import getLogger

import time, json, urllib
import requests
from sqlalchemy.orm.exc import NoResultFound

'''
    redis db 0:
        api # crawler job queue
        api_set # set of crawler job queue to avoid repush crawler job
    redis db 1:
        cache #all cache
'''


def commonHandler(api, content):
    return (content["cardnum"] + "-" + api, content["cardnum"])


def cardHandler(api, content):
    return (content["cardnum"] + "-" + api + "-" + str(content["param"]["timedelta"]),
            content["cardnum"] + str(content["param"]["timedelta"]))


def run_crawler(log, apiMap, cacheMap):
    while True:
        try:
            # 从请求队列中读取
            redis_api = redis_job.blpop(API_JOB_KEY)
            content = json.loads(redis_api[1])

            # 拼接请求
            api = content["api"]
            cardnum = content["cardnum"]
            url = CRAWLER_URL + api

            data = {
                "cardnum": cardnum,
                "password": content["password"]
            }
            if "param" in content:
                for key in content["param"].keys():
                    data[key] = content["param"][key]
            response = requests.post(url, data=data).text
            response = json.loads(response)
            if response['code'] == 200:
                api_key = apiMap[api](api, content)
                redis_cache.set(api_key[0], json.dumps(response))  # store data into redis
                redis_cache.expire(api_key[0], CACHE_TIME[api])  # set cache time into redis
                redis_job.srem(API_JOB_SET_KEY, json.dumps(content))  # delete job from set from redis
                # mysql update
                try:
                    cache = cacheMap[api]
                    cache_instance = mysql_db.query(cache).filter(cache.cardnum == cardnum).one()
                    cache_instance.text = json.dumps(response)
                    cache_instance.date = int(time.time())
                    mysql_db.add(cache_instance)
                except NoResultFound:
                    cache_instance = cache(cardnum=cardnum, text=json.dumps(response), date=int(time.time()))
                    mysql_db.add(cache_instance)
                mysql_db.commit()
            else:
                log.error("%s - in %s\ncode:%s\ncontent:%s\n" % (
                    content["cardnum"], api, response["code"], response["content"]))
        except Exception, e:
            redis_job.srem(API_JOB_SET_KEY, redis_api[1])
            log.error("%s - in %s\nerror:%s\n" % (content["cardnum"], api, str(e)))


def start(log, apiMap, cacheMap):
    jobs = []
    for x in xrange(0, CLIENT_NUMBER):
        jobs.append(gevent.spawn(run_crawler, log, apiMap, cacheMap))
    gevent.joinall(jobs)


def crawler_main():
    log = getLogger("webcrawler")
    apiMap = {
        'card': cardHandler,
        'exam': commonHandler,
        'gpa': commonHandler,
        'lecture': commonHandler,
        'library': commonHandler,
        'jwc': commonHandler,
        'nic': commonHandler,
        'pedetail': commonHandler,
        'phylab': commonHandler,
        'room': commonHandler,
        'srtp': commonHandler,
        'user': commonHandler
    }

    cacheMap = {
        'card': CardCache,
        'exam': ExamCache,
        'gpa': GpaCache,
        'lecture': LectureCache,
        'library': ListLibrary,
        'jwc': JWCCache,
        'nic': NicCache,
        'pedetail': PeDetailCache,
        'phylab': PhylabCache,
        'room': RoomCache,
        'srtp': SRTPCache,
        'user': UserDetail
    }
    start(log, apiMap, cacheMap)
