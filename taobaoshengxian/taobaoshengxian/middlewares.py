# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
import logging


class RandomProxyMiddleware(object):
    def __init__(self):
        self.proxy_url = 'http://localhost:5555/random'

    def get_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
            else:
                self.get_proxy()
        except:
            raise('获取proxy失败，正在重试')
            self.get_proxy()

    def process_request(self, requests, spider):
        self.logger.debug('正在获取代理...')
        if request.meta.get('retry_times'):
            proxy = self.get_proxy()
            if proxy:
                uri = 'http://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理', proxy)
                request.meta['proxy'] = uri
        


