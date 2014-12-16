#coding=utf8
from celery import Celery,platforms,group,chain
import time
import settings
import requests
import json
import datetime

import re
import random
from bs4 import BeautifulSoup
import redis
import logging
import logging.handlers
from redis.exceptions import WatchError
from settings import *


celery = Celery('suited4you', broker='redis://localhost:6379/0', backend='redis://localhost')
celery.config_from_object('settings')


LOG_FILE = 'suited4you.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024 * 50, backupCount=5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('suited4you_log')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
rd = settings.RD



@celery.task
def github_task(repo_owner_1, repo_name_1, repo_owner_2, repo_name_2):
    try:
        for repo_owner, repo_name in [{repo_owner_1:repo_name_1}, {repo_owner_2:repo_name_2}]:
            repo_tmp = gh.repos(repo_owner)(repo_name)
            repo = repo_tmp.get()
            repo_attr = [repo.watchers_count, repo.stargazers_count, repo.forks_count, repo.open_issues_count]
            repo_ctb = repo_tmp.contributors().get()
            repo_ctb_count = len(repo_ctb)
            repo_lang = repo_tmp.languages().get()
            repo_ca = repo_tmp.stats().commit_activity().get()
            ### mongo store
    except Exception as ex:
        print ex
        return False
    return True



@celery.task
def reddit_task(repo_name_1, repo_name_2):
    for item in [repo_name_1, repo_name_2]:
        try:
            subscribers = reddit.get_sub_subscribers(item)
        except Exception as reddit_ex:
            print reddit_ex
            continue
        #mongo store

    return True


@celery.task
def sof_task(repo_name_1, repo_name_2):
    for item in [repo_name_1, repo_name_2]:
        try:
            tags_infos = sof.get_tags_info([repo_name_1, repo_name_2])
        except Exception as sof_ex:
            print sof_ex
            continue
        #mongo store

    return True


@celery.task
def diff_tasks(repo_owner_1, repo_name_1, repo_owner_2, repo_name_2):
    try:
        repo_1 = gh.repos(repo_owner_1)(repo_name_1).get()
    except Exception as ex1:
        print ex1
        return 1
    try:
        repo_2 = gh.repos(repo_owner_2)(repo_name_2).get()
    except Exception as ex2:
        print ex2
        return 2

    task_group = []
    github_s = github_task.s(repo_owner_1, repo_name_1, repo_owner_2, repo_name_2)
    sof_s = sof_task.s(repo_name_1, repo_name_2)
    reddit_s = reddit_task.s(repo_name_1, repo_name_2)

    task_group.append(github_s)
    task_group.append(sof_s)
    task_group.append(reddit_s)
    g1 = group(task_group)
    g_re = g1().get()
    return g_re
