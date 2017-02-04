#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-11 19:23:24
# @Author  : yml_bright@163.com

import pe_models, pc_cache, jwc_cache, lecture_cache, card_cache, nic_cache, phylab_cache,gpa_cache
#import lecturedb, 
import user_detail, cookie_cache, exam_cache, library_cache, srtp_cache, tice_cache, library
import room_cache
#import empty_room
from db import engine, Base

Base.metadata.create_all(engine)
