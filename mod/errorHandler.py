#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Date   : February 03, 2017
@Author : corvo

vim: set ts=4 sw=4 tw=99 et:
"""

import tornado

class ErrorHandler(tornado.web.RequestHandler):
    """错误处理"""

    def get(self):
        self.write("Herald Web Service")

    def post(self):
        self.write("Herald Web Service")
