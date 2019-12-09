# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from scrapy.selector import Selector

from ..items import ZhihuBluestarItem

import json
import re

class BluestarSpider(Spider):
    name = 'bluestar'
    allowed_domains = ['www.zhihu.com']
    # 小蓝星推荐是通过 ajax 传送数据

    def start_requests(self):
        url = 'https://www.zhihu.com/api/v4/topics/rank_list/total_rank_list/1185985066819276800'
        headers = {
            'referer': 'https://www.zhihu.com/blue-star/ranking',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }
        yield Request(url, headers=headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        ''' 解析返回的 json 数据，提取 url_token '''
        headers = {
            'referer': response.url,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }
        res = json.loads(response.text)
        rank_list = res.get('rank_list')
        for num in range(0, len(rank_list)):
            url_token = rank_list[num].get('url_token')
            print(url_token)
            ranking_url = f'https://www.zhihu.com/blue-star/ranking/{url_token}'
            yield Request(ranking_url, headers=headers, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        ''' 
        比较简单，单纯的 html 网页，直接用 xpath 或者 css 定位提取数据
        值得一提的是，scrapy>=2.0 做了一次大更新，selector 选择器逻辑
        更加严密，他会将所有结果全部爬在 extract() 中，extract_first()
        只会提取列表中第一个，而不是全部，这也就能解释为什么 我的 jingdong
        评论只有这么点, haha，看来得去更新下 jingdongcms 代码了
        '''
        item = ZhihuBluestarItem()
        selector = Selector(response=response)

        pro_name = selector.xpath('//*[@id="root"]/div/main/div[1]/div/div[2]/p[1]/text()').extract()

        if pro_name:
            for num in range(0, len(pro_name)):
                item['title'] = selector.xpath('//*[@id="root"]/div/main/header/div/div[3]/span/text()').extract_first()
                item['pro_name'] = pro_name[num]
                item['score'] = selector.xpath('//*[@id="root"]/div/main/div[1]/div/div[2]/p[2]/span').re(r'(\d.\d)')[num]

                yield item
        



