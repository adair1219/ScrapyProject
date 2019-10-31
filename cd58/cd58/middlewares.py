# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent

import requests

class ProxyMiddleware(object):
    def get_random_proxy(self):
        try:
            response = requests.get('http://localhost:5555/random')
            if response.status_code == 200:
                proxy = response.text
                return proxy
            else:
                get_random_proxy()
        except:
            get_random_proxy()

    def process_request(self, request, spider):
        request.meta['proxy'] = self.get_random_proxy()


class RandomUserAgentMiddlware(object):
    #随机更换user-agent
    def __init__(self,crawler):
        super(RandomUserAgentMiddlware,self).__init__()
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self,request,spider):
        request.headers.setdefault("User-Agent",self.ua.random)
