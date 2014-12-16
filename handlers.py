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
from settings import gh
import tasks


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # user = Users(userid=1,username='jqh')
        # self.session.add(user)
        # self.session.commit()
        
        self.render('index.html')

    def post(self):
        onerepo = self.get_argument('onerepo')
        tworepo = self.get_argument('tworepo')
        repo_owner_1 = onerepo.split('/')[-2].lower()
        repo_name_1 = onerepo.split('/')[-1].lower()
        repo_owner_2 = tworepo.split('/')[-2].lower()
        repo_name_2 = tworepo.split('/')[-1].lower()

        tasks.diff_tasks.delay(repo_owner_1, repo_name_1, repo_owner_2, repo_name_2)
        
        self.write('ok');
        # self.redirect('/u/%s' % v2ex_id, permanent=True)