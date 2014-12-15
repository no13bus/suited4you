#coding=utf8
from urlparse import urlparse
import tornado
# from models import *
# from db import ConnectDB
from datetime import datetime

from tornado.gen import coroutine
# from tasks import *
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from lib.github import *
from lib.reddit import *
from lib.stackoverflow import *


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # user = Users(userid=1,username='jqh')
        # self.session.add(user)
        # self.session.commit()
        
        self.render('index.html')

    # def post(self):
    #     v2ex_id = self.get_argument('v2ex_id')
    #     self.redirect('/u/%s' % v2ex_id, permanent=True)

