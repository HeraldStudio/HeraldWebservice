#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Date   : February 03, 2017
@Author : corvo

vim: set ts=4 sw=4 tw=99 et:
"""

import json

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
from mod.models.mysql.user_detail import UserDetail

from mod.models.redis.redis_db import redis_job, redis_cache
from sqlalchemy.orm.exc import NoResultFound

from config import API_JOB_KEY
from mod.models.mysql.jwc_cache import JWCCache

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


def common_generate_key(api_name, cardnum, param={}):
    return (cardnum + "-" + api_name, cardnum)


def card_generate_key(api_name, cardnum, param):
    return (cardnum + "-" + api_name + "-" + str(param["timedelta"]), cardnum + str(param["timedelta"]))


GenerateKeyMap = {
    'card': card_generate_key,
    'exam': common_generate_key,
    'gpa': common_generate_key,
    'lecture': common_generate_key,
    'library': common_generate_key,
    'jwc': common_generate_key,
    'nic': common_generate_key,
    'pedetail': common_generate_key,
    'phylab': common_generate_key,
    'room': common_generate_key,
    'srtp': common_generate_key,
    'user': common_generate_key
}


def read_from_redis_db(key):
    temp = redis_cache.get(key)
    if temp:
        return json.loads(temp)
    else:
        return None


# if read from mysql return data even thought timeout beacuse of no cache
def read_from_mysql_db(db, api_name, cardnum, password, cache_key):
    cacheDb = cacheMap[api_name]
    try:
        cache_instance = db.query(cacheDb).filter(cacheDb.cardnum == cache_key).one()
        return cache_instance.text
    except NoResultFound:
        pass


def read_from_cache(db, api_name, cardnum, password=None, param={}):
    """该函数负责从缓存中读取, 数据, 如若缓存中没有数据,
    那么本次请求将会加入到请求队列中, 同时, 返回上一次请求成功所获得的数据, 

    :param db:
    :param api_name: api名称
    :param cardnum:  一卡通号
    :param password: 密码
    :param param:    附加参数
    :return:
    """
    retjson = {'code': 201, 'content': 'refresh'}
    key = GenerateKeyMap[api_name](api_name, cardnum, param)
    redis_db_cache = read_from_redis_db(key[0])

    # 读取redis中的缓存数据
    if redis_db_cache:
        return json.dumps(redis_db_cache, ensure_ascii=False, indent=2)

    push_to_crawler_queue(api_name, cardnum, password, param)

    mysql_db_cache = read_from_mysql_db(db, api_name, cardnum, password, key[1])
    if mysql_db_cache:
        return json.dumps(json.loads(mysql_db_cache), ensure_ascii=False, indent=2)

    return json.dumps(retjson, ensure_ascii=False, indent=2)


'''
crawler queue data format
    {
        "api": "room",
        "cardnum": cardnum,
        "password": password
    }
    {
        "api": "card",
        "cardnum": cardnum,
        "password": password,
        "param": {
            "timedelta": 1
        }
    }
'''


def push_to_crawler_queue(api_name, cardnum, password, param={}):
    data = json.dumps({
        "api": api_name,
        "cardnum": cardnum,
        "password": password,
        "param": param
    })
    if redis_job.sismember(API_JOB_KEY, data):  # 判断此时任务已经在队列中
        return
    else:
        # redis_job.sadd(API_JOB_SET_KEY, data)
        redis_job.rpush(API_JOB_KEY, data)
