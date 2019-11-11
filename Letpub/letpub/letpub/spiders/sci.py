# -*- coding: utf-8 -*-
from itertools import count

import numpy as np
from scrapy import Spider, Request
import pandas as pd

from ..items import LetpubItem
from scrapy_redis.spiders import RedisSpider


class SciSpider(RedisSpider):
    name = 'sci'
    allowed_domains = ['letpub.com.cn']
    redis_key = 'sci:start_urls http://www.letpub.com.cn'

    base_urls = 'http://www.letpub.com.cn/?page=grant&name=&person=&no=&company=&addcomment_s1=G&addcomment_s2='\
                +'G{addcomment_s2}&addcomment_s3=G{addcomment_s3}&addcomment_s4=&money1=&money2=&startTime={startTime}' \
                + '&endTime={endTime}&subcategory=&searchsubmit=true&'

    def __init__(self):
        self.time = range(2010, 2020)
        self.list_startTime = list(self.time)
        self.list_addcomment_s2 = ['01', '02', '03', '04']
        self.list_addcomment_s3 = [ ]
        for i in range(1, 19):
            number_s3 = str(i).rjust(2, '0')
            self.list_addcomment_s3.append(number_s3)

    def start_requests(self):
        # 循环查询
        for num_startT in range(len(self.list_startTime)):
            startTime = self.list_startTime[num_startT]
            endTime = startTime + 1
            for x in range(len(self.list_addcomment_s3)):
                for y in range(len(self.list_addcomment_s2)):
                    addcomment_s3 = self.list_addcomment_s2[y] + self.list_addcomment_s3[x]
                    addcomment_s2 = self.list_addcomment_s2[y]
                    urls = self.base_urls.format(addcomment_s2=addcomment_s2, addcomment_s3=addcomment_s3,
                                    startTime=startTime, endTime=endTime)
                    yield Request(urls, callback=self.parse_table)

    def parse_table(self, response):
        total_page = response.xpath('//*[@id="main"]/center[1]/div/text()').re_first('共(.*?)页。')
        try:
            for i in range(1, int(total_page)+1):
                currentUrl = response.url + 'currentpage=' + str(i)
                yield Request(currentUrl, callback=self.page_detail)
        except:
            pass

    def page_detail(self, response):
        item = LetpubItem()
        df = pd.read_html(response.url)[2]  # pandas read_html() 方法快速获取网页表格信息，dataframe 类

        num_df = len(df)  # len() 方法获取 dataframe 的行数
        result = df.drop([0, num_df-1])  # drop([, ]) 方法删除指定行
        principal = np.array(result.iloc[lambda x: x.index % 5 == 2, 0]).tolist()

        for n in range(len(principal)):
            item['principal'] = np.array(result.iloc[lambda x: x.index % 5 == 2, 0]).tolist()[n]  # iloc.[lambada, n] 方法获取指定行数
            item['unit'] = np.array(result.iloc[lambda x: x.index % 5 == 2, 1]).tolist()[n]
            item['amount'] = np.array(result.iloc[lambda x: x.index % 5 == 2, 2]).tolist()[n]
            item['numbering'] = np.array(result.iloc[lambda x: x.index % 5 == 2, 3]).tolist()[n]
            item['project_item'] = np.array(result.iloc[lambda x: x.index % 5 == 2, 4]).tolist()[n]
            item['department'] = np.array(result.iloc[lambda x: x.index % 5 == 2, 5]).tolist()[n]
            item['year'] = np.array(result.iloc[lambda x: x.index % 5 == 2, 6]).tolist()[n]
            item['topic'] = np.array(result.iloc[lambda x: x.index % 5 == 3, 1]).tolist()[n]
            item['classification'] = np.array(result.iloc[lambda x: x.index % 5 == 4, 1]).tolist()[n]
            item['coding'] = np.array(result.iloc[lambda x: x.index % 5 == 0, 1]).tolist()[n]
            item['excutionTime'] = np.array(result.iloc[lambda x: x.index % 5 == 1, 1]).tolist()[n]
            yield item

