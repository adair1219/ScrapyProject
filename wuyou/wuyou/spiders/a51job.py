# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from scrapy.selector import Selector

from ..items import ZhilianItem

class A51jobSpider(Spider):
    name = '51job'
    # allowed_domains = ['search.51job.com']
    
    def start_requests(self):
        '''
        构造页数索引 num ，循环请求所有页面
        '''
        for num in range(1, 66):
            url = f'https://search.51job.com/list/000000,000000,0000,00,9,99, \
                %25E5%258C%25BA%25E5%259D%2597%25E9%2593%25BE,2,{num}.html? \
                lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom \
                =99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius \
                =-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=& \
                specialarea=00&from=&welfare='
            yield Request(url, callback=self.get_item_links, dont_filter=True)

    def get_item_links(self, response):
        selector = Selector(response=response)
        item_links = selector.xpath('//*[@id="resultList"]/div/p/span/a/@href').extract()
    
        for link in item_links:
            yield Request(link, callback=self.get_detail, dont_filter=True)

    def get_detail(self, response):
        '''
        解析所有字段，Keyword 不是每个详情页都有，
        需要进行判断
        '''
        item = ZhilianItem()
        selector = Selector(response=response)
        
        item['a_JobName'] = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/text()').extract_first()
        item['b_ComName'] = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/text()').extract_first()
        item['c_Location'] = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[1]').extract_first().replace('\xa0', '')
        item['d_Salary'] = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()').extract_first()
        item['e_PubDate'] = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()').re_first(r'(\d+-\d+发布)')
        item['f_Require'] = ''.join(selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()').extract()).replace('\xa0', '')
        item['g_Walfare'] = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span/text()').extract()
        item['h_Info'] = ''.join(selector.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/p/text()').extract()).replace('\t', '')
        item['i_Type'] = selector.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/div[1]/p[1]/a/text()').extract()
        item['j_keyword'] = selector.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/div[1]/p[2]/a/text()').extract()
        item['k_CompInfo'] = ''.join(selector.xpath('/html/body/div[3]/div[2]/div[3]/div[3]/div/text()').extract()).replace('\xa0', '')

        yield item

        
