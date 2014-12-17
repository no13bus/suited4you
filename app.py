# coding=utf8
__author__ = 'no13bus'

from tornado import web, ioloop, httpserver
from settings import settings
from tornado.options import options, define
# import tornadoredis
import os
import handlers
import pymongo
from db import db

define('port', default=8000, type=int, help='server port')
define('template_path', default=os.path.join(
    os.path.dirname(__file__), "templates"), type=str, help='template path')
define('static_path', default=os.path.join(
    os.path.dirname(__file__), "static"), help='static file path')


class SuitedApp(web.Application):

    def __init__(self):
        routes = [
            (r'/', handlers.IndexHandler),
            (r'/taskstatus/(.*)', handlers.TaskStatusHandler),
            (r'/diff', handlers.DiffHandler),

        ]
        web.Application.__init__(self, routes, **settings)
        conn = pymongo.Connection("localhost", 27017)
        self.db = db


if __name__ == '__main__':
    options.parse_command_line()
    app = SuitedApp()
    server = httpserver.HTTPServer(app)
    server.listen(options.port)
    print "port:%s" % options.port
    loop = ioloop.IOLoop.instance()

    loop.start()
