#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-23 09:51:00
# @Author  : jerry.liangj@qq.com

import redis

DB_HOST = '127.0.0.1'
DB_PORT = 6379
JOB_DB_INDEX = 0
CACHE_DB_INDEX = 1

redis_job = redis.Redis(host=DB_HOST, port=DB_PORT, db=JOB_DB_INDEX)
redis_cache = redis.Redis(host=DB_HOST, port=DB_PORT, db=CACHE_DB_INDEX)