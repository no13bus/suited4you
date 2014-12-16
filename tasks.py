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
from db import db


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
# rd = settings.RD

@celery.task
def github_task(repo_owner_1, repo_name_1, repo_owner_2, repo_name_2):
    try:
        for repo_owner, repo_name in [(repo_owner_1, repo_name_1), (repo_owner_2, repo_name_2)]:
            repo_tmp = gh.repos(repo_owner)(repo_name)
            repo = repo_tmp.get()
            repo_attr = [repo.watchers_count, repo.stargazers_count, repo.forks_count, repo.open_issues_count]
            repo_ctb = repo_tmp.contributors().get()
            repo_ctb_count = len(repo_ctb)
            repo_lang = repo_tmp.languages().get()
            # repo_lang = sorted(repo_lang.iteritems(), key=lambda x:x[1], reverse=True)
            # repo_lang = repo_lang[0][0]
            repo_ca = repo_tmp.stats().commit_activity().get()
            ### mongo store
            coll = db.project
            one_repo = coll.find_one({"repo_owner": repo_owner, "repo_name": repo_name})
            if one_repo:
                one_repo['watchers_count'] = repo_attr[0]
                one_repo['stargazers_count'] = repo_attr[1]
                one_repo['forks_count'] = repo_attr[2]
                one_repo['open_issues_count'] = repo_attr[3]
                one_repo['repo_ctb_count'] = repo_ctb_count
                one_repo['language'] = repo_lang
                one_repo['commit_activity'] = repo_ca
                coll.save(one_repo)
            else:
                one_repo = {"repo_owner": repo_owner, "repo_name": repo_name,
                            "watchers_count":repo_attr[0], "stargazers_count":repo_attr[1],
                            "forks_count":repo_attr[2], "open_issues_count":repo_attr[3],
                            "repo_ctb_count":repo_ctb_count, "language":repo_lang,
                            "commit_activity":repo_ca}
                coll.insert(one_repo)

    except Exception as ex:
        print ex
        return False
    return True


## always 429. why??
@celery.task
def reddit_task(repo_owner_1, repo_name_1, repo_owner_2, repo_name_2):
    for key, value in [(repo_owner_1, repo_name_1), (repo_owner_2, repo_name_2)]:
        try:
            subscribers = reddit.get_sub_subscribers(key)
        except Exception as reddit_ex:
            print reddit_ex
            continue
        #mongo store
        coll = db.project
        one_reddit = coll.find_one({"repo_owner": key, "repo_name": value})
        if one_reddit:
            one_reddit['reddit_subscribers'] = subscribers
            coll.save(one_reddit)
        else:
            continue
    return True


@celery.task
def sof_task(repo_owner_1, repo_name_1, repo_owner_2, repo_name_2):
    try:
        tags_infos = sof.get_tags_info([repo_name_1, repo_name_2])
    except Exception as sof_ex:
        print sof_ex
        return False
    #mongo store
    coll = db.project
    one_sof = coll.find_one({"repo_owner": repo_owner_1, "repo_name": repo_name_1})
    if one_sof:
        print tags_infos
        one_sof['sof_count'] = tags_infos[repo_name_1]
        coll.save(one_sof)

    one_sof_2 = coll.find_one({"repo_owner": repo_owner_2, "repo_name": repo_name_2})
    if one_sof_2:
        print tags_infos
        one_sof_2['sof_count'] = tags_infos[repo_name_2]
        coll.save(one_sof_2)
    
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
    github_s = github_task(repo_owner_1, repo_name_1, repo_owner_2, repo_name_2)
    sof_s = sof_task(repo_owner_1, repo_name_1, repo_owner_2, repo_name_2)
    reddit_s = reddit_task(repo_owner_1, repo_name_1, repo_owner_2, repo_name_2)

    
    return [github_s, sof_s, reddit_s]
