#!/usr/bin/env python
#coding=utf8

import os
settings = {
    'gzip': True,
    'autoescape': 'xhtml_escape',
    'static_path':os.path.join(os.path.dirname(__file__), 'static'),
    'template_path':os.path.join(os.path.dirname(__file__), 'templates'),
    "xsrf_cookies": True,
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    'debug': True,
}

# DB_CONNECT_STRING = 'mysql+mysqldb://root:root@localhost/v2exfriends?charset=utf8'
import redis
pool = redis.ConnectionPool(host='localhost', port=6379, db=1)
RD = redis.Redis(connection_pool=pool)

#### libs settings
from libs.github import *
from libs.reddit import *
from libs.stackoverflow import *

GITHUB_TOKEN = '05aa6e1541ecdb53f473b8e32f2a4e45b1ea0a27'
gh = GitHub(GITHUB_TOKEN)
reddit = Reddit()
sof = Sof()




#celery settings
CELERYD_POOL_RESTARTS = True
CELERYD_FORCE_EXECV = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'users_chain_3600': {
        'task': 'tasks.users_chain',
        'schedule': timedelta(seconds=3620),
    },
    
}



####dev enviriment or deploy enviriment
import socket
if socket.gethostname() == 'jqh-virtual-machine' or socket.gethostname() == 'no13busdeMacBook-Air.local' or socket.gethostname() == 'localhost':
    try:
        from settings_dev import *
    except ImportError:
        pass