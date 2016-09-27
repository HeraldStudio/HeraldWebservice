#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-23 09:51:00
# @Author  : jerry.liangj@qq.com

from sqlalchemy.orm.exc import NoResultFound
from time import time
import json

from mod.models.redis_db import redis_job,redis_cache

API_JOB_KEY = "api"

API_JOB_SET_KEY = "api_set"

cacheMap = {
		'card': CardCache,
		'exam': ExamCache,
		'gpa': GpaCache,
		'lecture': LectureCache,
		'library': ListLibraryCache,
		'jwc': JWCCache,
		'nic': NicCache,
		'pedetail': PeDetailCache,
		'phylab': PhylabCache,
		'room': RoomCache,
		'srtp': SRTPCache,
		'user': UserDetail
	}

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

def common_generate_key(api_name,cardnum,param={}):
	return (cardnum + "-" + api_name,cardnum)

def card_generate_key(api_name,cardnum,param):
	return (cardnum + "-" + api_name + "-" + param["timedelta"], cardnum + param["timedelta"])

def read_from_redis_db(key):
	return redis_cache.get(key)

# if read from mysql return data even thought timeout beacuse of no cache
def read_from_mysql_db(db, api_name, cardnum, password, cache_key):
	cacheDb = cacheMap[api_name]
	try:
		cache_instance = db.query(cacheMap[cacheDb]).filter(cacheDb.cardnum == cache_key).one()
		return cache_instance.text
	except Exception,e:
		retjson['code'] = 500
		retjson['content'] = 'error'
	return None

def read_from_cache(db, api_name, cardnum, password=None, param={}):
	retjson = {'code': 201,'content': 'refresh'}
	key = GenerateKeyMap[api_name](api_name, cardnum, param)
	redis_db_cache = read_from_redis_db(key(0))
	if redis_db_cache:
		return redis_db
	mysql_db_cache = read_from_mysql_db(db, api_name, cardnum, password, key(1))
	if mysql_db_cache:
		return mysql_db_cache
	push_to_crawler_queue(api_name, cardnum, password, param)
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
def push_to_crawler_queue(api_name, cardnum, number, param={}):
	data = json.dumps({
		"api": api_name,
		"cardnum": cardnum,
		"password": password,
		"param": param
	})
	if redis_job.sismember(API_JOB_SET_KEY, data):
		return
	else:
		redis_job.rpush(API_JOB_KEY, data)


