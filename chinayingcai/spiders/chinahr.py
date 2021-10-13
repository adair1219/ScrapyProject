# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy import Selector

from ..items import ChinayingcaiItem

import time
import re


class ChinahrSpider(Spider):
    name = 'chinahr'
    allowed_domains = ['chinahr.com', 'search.chinahr.com']

    def __init__(self):
        '''
        初始一些基本信息
        '''
        self.city_list = ['bj', 'sh', 'tj', 'cq',
            'hf', 'fz', 'sz', 'nn', 'gy', 'lz', 'haikou',
            'zz', 'hrb', 'wh', 'cs', 'sjz', 'su', 'nc',
            'cc', 'sy', 'yinchuan', 'hu', 'xn', 'qd',
            'ty', 'xa', 'cd', 'xj', 'lasa', 'km', 'hz', 'hk'
        ]

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'search.chinahr.com',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        }

    def start_requests(self):
        print('开始爬取......')
        for num in range(0, len(self.city_list)):
            province = self.city_list[num]
            url = f'http://search.chinahr.com/{province}/job/?key=%E5%8C%BA%E5%9D%97%E9%93%BE'
            yield Request(url, callback=self.get_areas, headers=self.headers, dont_filter=True)

    def get_areas(self, response):
        '''
        获取所有城市
        '''
        print('开始获取所有城市......')
        res = Selector(response=response)
        cityUrl_list = res.xpath('//div[@class="dropdown-menu"]/ul/li//a//@href').extract()
        print('爬取成功，开始请求链接......')
        for num in range(0, len(cityUrl_list)):
            worse_url = cityUrl_list[num]
            url = re.sub(r'&minxinzi=\d+_\d+|&worktype=\d+', '', worse_url)
            yield Request(url, headers=self.headers, callback=self.get_pages, dont_filter=True)

    def get_pages(self, response):
        '''
        获取所有页面
        '''
        print('开始获取所有网页......')
        res = Selector(response=response)
        pageUrl_list = res.xpath('//*[@id="container"]/div[2]/div/div[5]/a/@href').extract()
        if len(pageUrl_list) == 0:
            # 用切片方法构造 url
            worse_url = response.url[:-33]
            token = response.url[-33:]
            url = worse_url + r'/pn1' + token
            yield Request(url, headers=self.headers, callback=self.get_items, dont_filter=True)
        else:
            length = len(pageUrl_list)
            for num in range(1, length+1):
                # 用切片方法构造 url
                worse_url = response.url[:-33]
                token = response.url[-33:]
                url = worse_url + f'/pn{num}' + token
                yield Request(url, headers=self.headers, callback=self.get_items, dont_filter=True)

    def get_items(self, response):
        '''
        请求商品页
        '''
        print('开始获取商品链接......')
        res = Selector(response=response)
        pattern = r'data-detail="(.*?.shtml)">'
        item_links = res.xpath('//*[@id="container"]/div[2]/div/div[1]/div').re(pattern) 
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.chinahr.com',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        }
        for num in range(0, len(item_links)):
            item_link = item_links[num]
            yield Request(item_link, headers=headers, callback=self.get_info, dont_filter=True)

    def get_info(self, response):
        '''
        获取商品详细信息
        '''
        print('开始获取信息.................')
        item = ChinayingcaiItem()
        res = Selector(response=response)

        item['a_JobName'] = res.xpath('/html/body/div[4]/div/div[1]/h1/text()').extract_first()
        item['b_ComName'] = res.xpath('/html/body/div[4]/div/div[2]/div/span[1]/text()').extract_first()
        item['c_Location'] = res.xpath('/html/body/div[4]/div/div[1]/div[3]/span/text()').extract_first()
        item['d_Salary'] = res.xpath('/html/body/div[4]/div/div[1]/div[1]/span[1]/text()').extract_first()
        item['e_PubDate'] = res.xpath('/html/body/div[4]/div/div[1]/div[4]/span/text()').extract_first()
        item['f_Require'] = ''.join(res.xpath('/html/body/div[4]/div/div[1]/div[1]/span[2]/text()').extract()).replace(r'\n', '').strip()
        item['g_employment'] = ''.join(res.xpath('/html/body/div[4]/div/div[2]/div/span[2]/text()').extract()).replace(r'\n', '').strip()
        item['h_Info'] = ''.join(res.xpath('/html/body/div[5]/div[1]/div[1]/div[1]/div/text()').extract()).replace(r'\n', '').strip()
        item['k_CompInfo'] = ''.join(res.xpath('/html/body/div[5]/div[1]/div[2]/div[2]/div/text()').extract()).replace(r'\n', '').strip()

        yield item







        



