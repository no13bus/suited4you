#coding: utf-8


from lib.github import *
from settings import GITHUB_TOKEN


gh = GitHub(GITHUB_TOKEN)
# /repos/:owner/:repo branch is master default
# /repos/:owner/:repo/contributors
repo = gh.repos('angular')('angular').get()
repo_attr = [repo.watchers_count, repo.stargazers_count, repo.forks_count, repo.open_issues_count]
repo_ctb = gh.repos('angular')('angular').contributors().get()
repo_ctb_count = len(repo_ctb)
# /repos/:owner/:repo/languages  返回各个语言所占的行数 是个字典
repo_lang = gh.repos('angular')('angular').languages().get()
# GET /repos/:owner/:repo/branches
repos_branchs = gh.repos('angular')('angular').branches().get()

# GET /repos/:owner/:repo/stats/commit_activity  去年一年的每周每天的commit提交量
# {'days': [0, 0, 0, 0, 0, 0, 0], 'total': 0, 'week': 1418515200}] 类似这样的数据
repo_ca = gh.repos('angular')('angular').stats().commit_activity().get()

# GET /repos/:owner/:repo/events
# repo的最近活动情况 动态

# repos/:owner/:repo/commits
repo_commits = gh.repos('angular')('angular').commits().get(sha='master')
# ==================================
# reddit  # 这个里面得到的信息得到的 subscribers是订阅人的个数
# http://www.reddit.com/r/redis/about.json
# http://www.reddit.com/r/redis/top.json http://www.reddit.com/r/redis/new.json

# stackoverflow
# 获得几个tag的统计情况 items里面有个数
# http://api.stackexchange.com/2.2/tags/redis;python/info?order=desc&sort=popular&site=stackoverflow
# 最好的几个问题 经常被问到的一些问题  这个的参数还是分开写吧。 不能redis;python这样来写
# http://api.stackexchange.com/2.2/tags/redis/faq?site=stackoverflow