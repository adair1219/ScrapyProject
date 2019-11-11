# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import requests


class FzppSpider(scrapy.Spider):
    name = 'fzpp'
    allowed_domains = ['fz.people.com.cn']
    base_url = 'http://fz.people.com.cn/skygb/sk/index.php/Index/seach?xktype=%E5%9B%BE%E4%B9%A6%E9%A6%86%E3%80%81%E6%83%85%E6%8A%A5%E4%B8%8E%E6%96%87%E7%8C%AE%E5%AD%A6&p={page}'

    def start_requests(self):
        for i in range(1, 167):
            url = self.base_url.format(page=i)
            result = pd.read_html(url)[2]
            print(result)
            result.to_csv('result_book.csv', mode='a', encoding='utf-8', chunksize=20000)

        
