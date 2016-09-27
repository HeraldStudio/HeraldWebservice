# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 15:43:36
# @Author  : xindervella@gamil.com yml_bright@163.com
from sqlalchemy.orm import scoped_session, sessionmaker
from mod.models.db import engine
from mod.curriculum.term_handler import TermHandler
from mod.curriculum.sidebar_handler import SidebarHandler
from mod.curriculum.curriculum_handler import CurriculumHandler
from mod.simsimi.handler import SIMSIMIHandler
from mod.pe.handler import PEHandler,ticeInfoHandler
from mod.auth.handler import AuthHandler
from mod.library.renewhandler import LibRenewHandler
from mod.library.searchhandler import LibSearchHandler
from mod.library.hothandler import HotHandler
from mod.pc.handler import PCHandler
from mod.jwc.handler import JWCHandler
from mod.schoolbus.handler import SchoolBusHandler
from mod.emptyroom.handler import CommonQueryHandler, QuickQueryHandler,NewHandler
from mod.lecture.noticehandler import LectureNoticeHandler
from mod.user.handler import UserHandler
from mod.bedRoom.handler import RoomHandler
from mod.yuyue.handler import YuyueHandler

import tornado.web
import tornado.ioloop
import tornado.options

from tornado.options import define, options
define('port', default=7005, help='run on the given port', type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/webserv2/auth', AuthHandler),
            (r'/webserv2/term',TermHandler),
            (r'/webserv2/sidebar', SidebarHandler),
            (r'/webserv2/curriculum', CurriculumHandler),
            (r'/webserv2/pe', PEHandler),
            (r'/webserv2/simsimi', SIMSIMIHandler),
            (r'/webserv2/library_hot',HotHandler),
            (r'/webserv2/renew', LibRenewHandler),
            (r'/webserv2/search', LibSearchHandler),
            (r'/webserv2/pc', PCHandler),
            (r'/webserv2/jwc', JWCHandler),
            (r'/webserv2/schoolbus', SchoolBusHandler),
            (r'/webserv2/lecturenotice', LectureNoticeHandler),
            (r'/webserv2/user', UserHandler),
            (r'/webserv2/query', NewHandler),
            (r'/webserv2/room',RoomHandler),
            (r'/webserv2/tice',ticeInfoHandler),
            (r'/webserv2/yuyue',YuyueHandler),
            (r'/webserv2/[\S]+', CommonHandler)
        ]
        settings = dict(
            cookie_secret="7CA71A57B571B5AEAC5E64C6042415DE",
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))
class CommonHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def on_finish(self):
        self.db.close()

    @property
    def unitsmap(self):
        return {
            'card': self.card,
            'exam': self.exam,
            'gpa': self.gpa,
            'lecture': self.lecture,
            'library': self.library,
            'nic': self.nic,
            'pedetail': self.pedetail,
            'phylab': self.phylab,
            'room': self.room,
            'srtp': self.srtp
        }
    def get(self, API):
        self.write('Herald Web Service')

    def post(self, API):
        try:
            self.unitsmap(API)
        except KeyError:
            raise tornado.web.HTTPError(400)
        except Exception,e:
            retjson = {"code":500,"content":str(e)}
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))

    def card(self):
        cardnum = self.get_argument('cardnum', default = None)
        password = self.get_argument('password', default = None)
        timedelta = self.get_argument('timedelta', default = 0)
        retjson = read_from_cache(self.db,"card", cardnum, password, {"timedelta":timedelta})
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)

    def srtp(self):
        number = self.get_argument('number', default=None)
        retjson = read_from_cache(self.db,"srtp", number)
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)

    def exam(self):
        cardnum = self.get_argument('cardnum', default = None)
        password = self.get_argument('password', default = None)
        retjson = read_from_cache(self.db,"exam", cardnum, password)
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)

    def gpa(self):
        cardnum = self.get_argument('username', default = None)
        password = self.get_argument('password', default = None)
        retjson = read_from_cache(self.db,"gpa", cardnum, password)
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)

    def lecture(self):
        cardnum = self.get_argument('cardnum', default = None)
        password = self.get_argument('password', default = None)
        retjson = read_from_cache(self.db,"lecture", cardnum, password)
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)

    def nic(self):
        cardnum = self.get_argument('cardnum', default = None)
        password = self.get_argument('password', default = None)
        retjson = read_from_cache(self.db,"nic", cardnum, password)
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)

    def pedetail(self):
        cardnum = self.get_argument('cardnum', default = None)
        password = self.get_argument('password', default = None)
        retjson = read_from_cache(self.db,"pedetail", cardnum, password)
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)

    def phylab(self):
        cardnum = self.get_argument('number', default = None)
        password = self.get_argument('password', default = None)
        term = self.get_argument('term', default = None)
        retjson = read_from_cache(self.db,"phylab", cardnum, password, {"term":term})
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)

    def room(self):
        cardnum = self.get_argument('number', default = None)
        password = self.get_argument('password', default = None)
        retjson = read_from_cache(self.db,"room", cardnum, password)
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)
    
    


if __name__ == '__main__':
    tornado.options.parse_command_line()
    Application().listen(options.port, address='127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()
