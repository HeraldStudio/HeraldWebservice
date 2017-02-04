# -*- coding: utf-8 -*-
# @Date    : 2016-03-24 16 16:34:57
# @Author  : jerry.liangj@qq.com

import time

from sqlalchemy.orm.exc import NoResultFound

from config import *
from handler import authApi
from mod.models.mysql.cookie_cache import CookieCache


def getCookie(db,cardnum,card_pwd):
	state = 1
	ret = {'code':200,'content':''}
	try:
		result = db.query(CookieCache).filter(CookieCache.cardnum==cardnum).one()
		if (result.date+COOKIE_TIMEOUT<int(time.time())):
			state = 0
		else:
			ret['content'] = result.cookie
	except NoResultFound:
		result = CookieCache(cardnum=cardnum,cookie="",date=int(time.time()))
		state = 0
	except Exception,e:
		ret['code'] = 500
		ret['content'] = str(e)
	if state==0:
		result = authApi(cardnum,card_pwd)
		if result['code']==200:
			ret['content'] = cookie
			result.cookie = cookie
			try:
				db.add(result)
				db.commit()
			except:
				db.rollback()
		else:
			ret['code'] = 500
			ret['content'] = cookie
	return ret
