# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 15:43:36
# @Author  : xindervella@gamil.com yml_bright@163.com
import tornado.ioloop
import tornado.options
import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker

from log import getLogger
from mod.auth.handler import AuthHandler
from mod.bedRoom.handler import RoomHandler
from mod.commonHandler import CommonHandler
from mod.curriculum.curriculum_handler import CurriculumHandler
from mod.curriculum.sidebar_handler import SidebarHandler
from mod.curriculum.term_handler import TermHandler
from mod.emptyroom.handler import NewHandler
from mod.errorHandler import ErrorHandler
from mod.jwc.handler import JWCHandler
from mod.library.hothandler import HotHandler
from mod.library.renewhandler import LibRenewHandler
from mod.library.searchhandler import LibSearchHandler
from mod.models.mysql.db import engine
from mod.pc.handler import PCHandler
from mod.pe.handler import PEHandler, ticeInfoHandler
from mod.schoolbus.handler import SchoolBusHandler
from mod.simsimi.handler import SIMSIMIHandler
from mod.user.handler import UserHandler
from mod.yuyue.handler import YuyueHandler

# log = getLogger("webservice")

from tornado.options import define, options

define('port', default=7005, help='run on the given port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/webserv2/auth', AuthHandler),
            (r'/webserv2/term', TermHandler),
            (r'/webserv2/sidebar', SidebarHandler),
            (r'/webserv2/curriculum', CurriculumHandler),
            (r'/webserv2/pe', PEHandler),
            (r'/webserv2/simsimi', SIMSIMIHandler),
            (r'/webserv2/library_hot', HotHandler),
            (r'/webserv2/renew', LibRenewHandler),
            (r'/webserv2/search', LibSearchHandler),
            (r'/webserv2/pc', PCHandler),
            (r'/webserv2/jwc', JWCHandler),
            (r'/webserv2/schoolbus', SchoolBusHandler),
            (r'/webserv2/user', UserHandler),
            (r'/webserv2/query', NewHandler),
            (r'/webserv2/room', RoomHandler),
            (r'/webserv2/tice', ticeInfoHandler),
            (r'/webserv2/yuyue', YuyueHandler),
            (r'/webserv2/([\S]+)', CommonHandler),
            (r'.*', ErrorHandler)

        ]
        settings = dict(
            cookie_secret="7CA71A57B571B5AEAC5E64C6042415DE",
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))


def tornado_main():
    tornado.options.parse_command_line()
    Application().listen(options.port, address='127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()
