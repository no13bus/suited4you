#coding=utf8
from urlparse import urlparse
import tornado
from datetime import datetime

from tornado.gen import coroutine
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from settings import gh
import tasks
from celery.result import AsyncResult
from db import db


class TaskStatusHandler(tornado.web.RequestHandler):
    def get(self):
        taskid = self.get_argument('taskid', '')
        if not taskid:
            self.write('')
        work = AsyncResult(taskid)
        state_str = work.state

        self.write(state_str)
        

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        data = {}
        taskid = self.get_argument('taskid', '')
        onerepo_owner = self.get_argument('onerepo_owner', '')
        onerepo_name = self.get_argument('onerepo_name', '')
        tworepo_owner = self.get_argument('tworepo_owner', '')
        tworepo_name = self.get_argument('tworepo_name', '')
        self.render('index.html', taskid=taskid, onerepo_owner=onerepo_owner, onerepo_name=onerepo_name, tworepo_owner=tworepo_owner,tworepo_name=tworepo_name)

    def post(self):
        onerepo = self.get_argument('onerepo')
        tworepo = self.get_argument('tworepo')
        onerepo_owner = onerepo.split('/')[-2].lower()
        onerepo_name = onerepo.split('/')[-1].lower()
        tworepo_owner = tworepo.split('/')[-2].lower()
        tworepo_name = tworepo.split('/')[-1].lower()

        mytask = tasks.diff_tasks.delay(onerepo_owner, onerepo_name, tworepo_owner, tworepo_name)
        taskid = mytask.id
        
        self.render('index.html', taskid=taskid, onerepo_owner=onerepo_owner, onerepo_name=onerepo_name, tworepo_owner=tworepo_owner,tworepo_name=tworepo_name)



class DiffHandler(tornado.web.RequestHandler):
    def get(self):
        onerepo_owner = self.get_argument('onerepo_owner', '')
        onerepo_name = self.get_argument('onerepo_name', '')
        tworepo_owner = self.get_argument('tworepo_owner', '')
        tworepo_name = self.get_argument('tworepo_name', '')
        coll = db.project
        onerepo = coll.find_one({"repo_owner": onerepo_owner, "repo_name": onerepo_name})
        if onerepo:
            del onerepo['_id']
        tworepo = coll.find_one({"repo_owner": tworepo_owner, "repo_name": tworepo_name})
        if tworepo:
            del tworepo['_id']
        self.render("diff.html", onerepo=onerepo, tworepo=tworepo)

    def post(self):
        pass