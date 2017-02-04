#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-23 09:51:00
# @Author  : jerry.liangj@qq.com


# crawler中使用了python中的协程, 此数字为协程中实例的个数
CLIENT_NUMBER = 5

# 分布式爬虫地址
CRAWLER_URL = "http://127.0.0.1:7000/crawler/"

API_JOB_KEY = "api"

API_JOB_SET_KEY = "api_set"

# redis缓存时间设置
CACHE_TIME = {
    'card': 3600,
    'exam': 3600,
    'gpa': 3600,
    'lecture': 3600,
    'library': 3600,
    'jwc': 3600,
    'nic': 3600,
    'pedetail': 3600,
    'phylab': 3600,
    'room': 3600,
    'srtp': 3600,
    'user': 3600
}
