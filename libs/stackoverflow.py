#coding: utf-8
import requests
import json

__version__ = '0.1'

sof_api_url = 'http://api.stackexchange.com/2.2'

class Sof(object):
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

    ''' tags is list. get_tags_info return dict'''
    def get_tags_info(self, tags):
        tags_str = ';'.join(tags)
        url = '%s/tags/%s/info?order=desc&sort=popular&site=stackoverflow' % (sof_api_url, tags_str)
        j = _get_json(url)
        if not j:
            return False
        result = {item['name']:item['count'] for item in j['items']}
        return result


    def get_tag_faq(self, tag):
        url = '%s/tags/%s/faq?site=stackoverflow' % (sof_api_url, tag)
        j = _get_json(url)
        if not j:
            return False
        ## return all of faqs items
        result = j['items']
        return result
        

# GET /repos/:owner/:repo

# watch数量 fork数量 star数量 创建时间  issue 数量