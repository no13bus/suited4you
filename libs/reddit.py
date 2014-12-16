#coding: utf-8
import requests
import json


__version__ = '0.1'

class Reddit(object):
    ''' pay attention to status_code 429!!!'''
    # def __init__(self, subreddits):
    #     self.subreddits = subreddits

    def _get_json(self, url):
        try:
            r = requests.get(url, timeout=60)
        except:
            print 'can not get requests. url is %s' % url
            return False
        if r.status_code != 200:
            print 'status_code is not 200, it is %s' % r.status_code
            return False
        try:
            j = json.loads(r.content)
        except Exception as ex:
            print ex
            return False
        return j

    def get_sub_subscribers(self, subreddits):
        url = 'http://www.reddit.com/r/%s/about.json' % subreddits
        j = self._get_json(url)
        if not j:
            return False
        subscribers = j['data']['subscribers'] if j['data']['subscribers'] else 0
        return subscribers

    def get_sub_top(self, subreddits):
        url = 'http://www.reddit.com/r/%s/top.json' % subreddits
        j = self._get_json(url)
        if not j:
            return False
        # j['data']['children'][0]['data']['url']
        # j['data']['children'][0]['data']['selftext_html']
        # j['data']['children'][0]['data']['selftext']
        return j

    def get_sub_new(self, subreddits):
        url = 'http://www.reddit.com/r/%s/new.json' % subreddits
        j = self._get_json(url)
        if not j:
            return False
        return j
