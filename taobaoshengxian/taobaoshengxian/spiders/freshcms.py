# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

import json
import re

class FreshcmsSpider(scrapy.Spider):
    name = 'freshcms'
    # allowed_domains = ['taobao.com'] 通过注释这一行，取消域名限制
    # start_urls = ['https://tce.alicdn.com/api/data.htm?ids=222905']  

    def __init__(self):
        ''' 
        抓包并分析参数规律可以得出，ids 是取出
        每个商品链接必须的，可以根据爬取需求更改

        实现全部页面抓取,实现方法是 加 &s=0 规律是 +44
        '''
        self.ids = '222905'
        self.s = 44
        self.headers = {
            ':authority': 's.taobao.com',
            ':method': 'GET',
            ':path': '/search?q=%E8%8D%94%E6%9E%9D&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180724&ie=utf8',
            ':scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        }

    def start_requests(self):
        ''' 获取商品分类链接 '''
        base_url = 'https://tce.alicdn.com/api/data.htm?ids='
        start_url = base_url + self.ids
        yield Request(start_url, callback=self.extract_links, dont_filter=True)

    def extract_links(self, response):
        ''' json.loads()-- 提取商品分类链接 '''
        text = json.loads(response.text)
        # 字典广播式，获取链接列表
        links_list = text.get('222905').get('value').get('list')
        for num in range(1, len(links_list)):  #  获取列表长度，并遍历
            accurate_url = links_list[num].get('link') + '&ajax=true' # 添加ajax=true 网页返回 sjon 数据
            yield Request(accurate_url, callback=self.get_pages, dont_filter=True)

    def get_pages(self, response):
        '''
        获取网页界面，并重构 url，利用 re,目标是 
        https://s.taobao.com/search?q=海鲜&ajax=true&s=44
        以此达到爬取全部 100 页的商品
        '''
        pattern = re.compile(r'^(https://.*?)&s.*')
        base_url = re.search(pattern, response.url).group(1)  # 提取每个种类的 link
        for page_num in range(1, 101):
            s = page_num * self.s
            
            final_url = base_url + '&s=' + str(s) + '&ajax=true'  # 通过加 ajax 参数，淘宝会返回一个 sjon 数据
            yield Request(final_url, callback=self.get_items, headers=self.headers,dont_filter=True)

    def get_items(self, response):
        '''
        获取每一页上所有的商品
        '''
        print(response.url)
        pattern = re.compile(r'allNids.*?(\d+)')
        nids = re.findall(pattern, response.text)
        print(nids)


            

        

    



