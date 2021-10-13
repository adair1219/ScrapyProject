# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy import Selector

from ..items import LiepinwangItem

class LiepinSpider(Spider):
    name = 'liepin'
    allowed_domains = ['liepin.com']
    
    def start_requests(self):
        '''
        获取所有职位页数信息
        该网站很简单，只需去除一些不必要的 token，
        然后构造页数 参数，即可获取到所有区块链的招聘信息
        '''
        print('爬虫开始散播......')
        for pageNum in range(0, 100):
            base_url = f'https://www.liepin.com/zhaopin/?key=%E5%8C%BA%E5%9D%97%E9%93%BE&d_pageSize=40&curPage={pageNum}'
            yield Request(base_url, callback=self.get_items, dont_filter=True)

    def get_items(self, response):
        '''
        获取职位链接
        '''
        print('正在获取商品链接......')
        res = Selector(response=response)
        
        item_links = res.xpath('//div[@class="wrap"]//div//ul//li//div[@class="job-info"]//h3//a/@href').extract()
        for link in item_links:
            yield Request(link, callback=self.get_info, dont_filter=True)

    def get_info(self, response):
        '''
        获取职位详情信息
        猎聘网网页结构是 css, 采用 css 解析器
        猎聘网有 ip ban，建议使用 proxy 代理爬取，本人比较懒，没有写
        请在 middlewares 中间组件中写随机代理
        '''
        print('正在爬虫信息..........')
        res = Selector(response=response)
        item = LiepinwangItem()

        item['a_JobName'] = res.xpath('//div[@class="title-info"]/h1/text()').extract_first()
        item['b_ComName'] = res.xpath('//div[@class="title-info"]//h3/a/text()').extract_first()
        item['d_Salary'] = res.xpath('//p[@class="job-item-title"]/text()').extract_first().replace(r'\r\n', '').strip()
        item['c_Location'] = res.xpath('//span[@class="place"]/text()').extract_first().strip()
        item['e_PubDate'] = res.xpath('//time/text()').extract_first()
        item['f_Require'] = res.xpath('//div[@class="job-qualifications"]//span/text()').extract()
        item['g_tags'] = ','.join(res.xpath('//div[@class="comp-tag-box"]//ul//li/span/text()').extract())
        item['h_Info'] = ''.join(res.css('#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div.job-item.main-message.job-description > div::text').extract()).replace(r'\n\t', '').strip()
        item['i_Belong'] = res.css('#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div:nth-child(5) > div > ul > li > label::text').extract_first()
        item['j_Duixiang'] = res.css('#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div:nth-child(5) > div > ul > li:nth-child(3) > label::text').extract_first()
        item['k_Xiashu'] = res.css('#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div:nth-child(5) > div > ul > li:nth-child(4) > label::text').extract_first()
        item['l_CompInfo'] = ''.join(res.css('#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div.job-item.main-message.noborder > div > div.info-word::text').extract())
        item['m_Hangye'] = res.css('#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.side > div:nth-child(2) > div.right-post-top > div.company-infor > div > ul.new-compintro > li:nth-child(1) > a::text').extract_first()
        item['n_Guimo'] = res.css('#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.side > div:nth-child(2) > div.right-post-top > div.company-infor > div > ul.new-compintro > li:nth-child(2)::text').extract_first()
        item['o_Address'] = res.css('#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.side > div:nth-child(2) > div.right-post-top > div.company-infor > div > ul.new-compintro > li:nth-child(3)::text').extract_first()
        item['p_Time'] = res.css('#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.side > div:nth-child(2) > div.right-post-top > div.company-infor > div > ul.new-compdetail > li:nth-child(1)::text').extract_first()
        item['q_Ziben'] = res.css('#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.side > div:nth-child(2) > div.right-post-top > div.company-infor > div > ul.new-compdetail > li:nth-child(2)::text').extract_first()
        item['r_Date'] = res.css('#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.side > div:nth-child(2) > div.right-post-top > div.company-infor > div > ul.new-compdetail > li:nth-child(3)::text').extract_first()
        item['s_Range'] = res.css('#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.side > div:nth-child(2) > div.right-post-top > div.company-infor > div > ul.new-compdetail > li:nth-child(4)::text').extract_first()

        yield item


