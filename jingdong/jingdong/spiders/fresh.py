# -*- coding: utf-8 -*-
from scrapy import Request, Spider

from ..items import JingdongItem

import re

class FreshSpider(Spider):
    name = 'fresh'
    # allowed_domains = ['fresh.jd.com']  通过注释这一行取消对域名的限制
    start_urls = ['https://fresh.jd.com/']

    def __init__(self):
        self.pattern_one = re.compile(r"(https://search.jd.com/.*?)',")
        self.pattern_two = re.compile(r'keyword=(.*?)&.*')
        self.pattern_three = re.compile(r'(//item.jd.com/.*?)">')
        self.pattern_four = re.compile(r'(原产地)')
        self.pattern_five = re.compile(r'.*原产地：(.*?)<')
        self.location = '四川'

    def parse(self, response):
        ''' 获取所有商品链接 '''
        urls = re.findall(self.pattern_one, response.text)
        for url in urls:
            yield Request(url, callback=self.get_all_pages, dont_filter=True)

    def get_all_pages(self, response):
        ''' 
        构造网页，获取单个商品的全部网页
        meanwhile, make a url to request the rest of the single url by ajax
        if ajax_url doesn't exist, only request the item_url that contains the details of product
        '''
        keyword = re.search(self.pattern_two, response.url).group(1)
        for page in range(1, 101):
            index_page = page * 2
            headers = {
                'refer': response.url,
                'sec-fecth-mode': 'cors',
                'sec-fecth-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            }
            ajax_urls = 'https://search.jd.com/s_new.php?keyword={keyword}&enc=utf-8$page={page}'.format(keyword=keyword, page=index_page)
            item_urls = response.url + '&page=' + str(index_page)
            if ajax_urls:
                yield Request(ajax_urls, callback=self.get_items, headers=headers, dont_filter=True)
                yield Request(item_urls, callback=self.get_items, headers=headers, dont_filter=True)
            else:
                yield Request(item_urls, callback=self.get_items, headers=headers, dont_filter=True)

    def get_items(self, response):
        '''
        in this function, we will get the product's url, and
        pass it to next function to parse more detail.
        the way of getting url has much trouble like headers-ban
        , containing the 'https://' in some item_url
        '''
        headers = {
            'cache-control': 'max-age=0',
            'referer': response.url,
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': 1,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        }
        product_urls = response.xpath('//*[@id="J_goodsList"]/ul/li/div/div[3]/a/@href').extract()
        # # re'speed is slower than xpath, but it never make a mistake
        # product_urls = re.findall(self.pattern_three, response.text)
        for product_url in product_urls:
            if u'https:' in product_url:
                yield Request(product_url, callback=self.get_item_detail, headers=headers, dont_filter=True)
            else:
                # if 'https' not in product_url, then concat 'https://' to response.url
                product_url = 'https:' + product_url
                yield Request(product_url, callback=self.get_item_detail, headers=headers, dont_filter=True)

    def get_item_detail(self, response):
        '''
        get accurate detail with limitation by location field
        '''
        static = JingdongItem()  # 网页静态数据管道

        if re.search(self.pattern_four, response.text).group(1):
            location = re.search(self.pattern_five, response.text).group(1)
            if location == self.location:
                static['a_Location'] = location
                static['b_Title'] = response.xpath('/html/body/div[6]/div/div[2]/div[1]/text()').extract()  # 商品标题
                static['c_Mall'] = response.xpath('//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/text()').extract_first()  # 店铺
                static['d_Brand'] = response.xpath('//*[@id="parameter-brand"]/li/a/text').extract_first()  # 商品品牌
                static['e_sortable'] = re.search(r'类别：(.*?)<', response.text).group(1)  # 商品类别

                # stock  review 
            else:
                print('原产地不在四川省，跳过')
                pass
        else:
            print('没有原产地字段，跳过')
            pass
            




