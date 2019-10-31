# -*- coding: utf-8 -*-
"""
1.不要被 jQuery....... 那串吓到了,虽然是动态的，但是把他剔除掉也没关系，照样可以返回数据
2.数据通过 meta 层层传递(因为 58 把数据分布在不同地方 wdnmd)
3.由于数据量很大，采用分布式 scrapy_redis
"""
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import Cd58Item
from .cateid import job_cate

import re 
from scrapy_redis.spiders import RedisCrawlSpider

class City58Spider(CrawlSpider):
    name = 'city58'
    # allowed_domains = ['cd.58.com']
    start_urls = ['https://cd.58.com/job.shtml']
    # redis_key = 'city58:start_urls'

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="sidebar-right"]/ul/li/a'), ), callback=None, follow=True),
        Rule(LinkExtractor(restrict_xpaths=('/html/body/div[3]/div[4]/div[1]/div[2]/a[2]'), ), callback=None, follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="list_con"]/li/div[1]/div[1]/a'), ), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="jingzhun"]/a'), ), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """ 
        1.爬取静态数据
        2.找 API 传递参数，从而获取到动态数据，交给 'parse_detail' 处理
        3.将数据放在 StaticItem 存储器中, 并传递
        4.传递 response.url 给下下个处理函数，用来构造请求头(这该死的反爬虫>.<_)
        """
        print(response.url)
    #     StaticItem = Cd58Item()

    #     StaticItem['aTitle'] = response.xpath('//div[@class="con"]//div[@class="leftCon"]//div[@class="pos_base_info"]//span[@class="pos_title"]//text()').extract_first()
    #     StaticItem['bSalary'] = response.xpath('/html/body/div[3]/div[3]/div[1]/div[2]/span[2]//text()').extract_first()
    #     StaticItem['cPos'] = response.xpath('/html/body/div[3]/div[3]/div[1]/span//text()').extract_first()
    #     StaticItem['dWelfare'] = '|'.join(response.xpath('//div[@class="con"]//div[@class="leftCon"]//div[@class="pos_welfare"]//span[@class="pos_welfare_item"]//text()').extract())
    #     StaticItem['eRequire'] = '|'.join(response.xpath('//div[@class="con"]//div[@class="leftCon"]//div[@class="pos_base_condition"]//span//text()').extract())
    #     StaticItem['fAddress'] = ''.join(response.xpath('/html/body/div[3]/div[3]/div[1]/div[5]/span//text()').extract())
    #     StaticItem['gDesc'] = ''.join(response.xpath('/html/body/div[3]/div[3]/div[2]/div[1]/div[1]/div[1]//text()').extract())
    #     StaticItem['hCom_intr'] = ''.join(response.xpath('//div[@class="subitem_con comp_intro"]//div[@class="shiji"]//text()').extract()).replace('\xa0', '')
    #     StaticItem['iCompany'] = response.xpath('/html/body/div[3]/div[4]/div[1]/div/div[1]//div[1]/a//text()').extract_first()
    #     # item['jCom_sign'] = response.xpath('/html/body/div[3]/div[4]/div[1]/div/div[1]//div/div[2]/i').re('(\d+)')
    #     StaticItem['kCom_belong'] = response.xpath('/html/body/div[3]/div[4]/div[1]/div//p[1]/a//text()').extract_first()
    #     StaticItem['lCom_num'] = response.xpath('/html/body/div[3]/div[4]/div[1]//div/p[2]//text()').extract_first()
    #     StaticItem['mCom_iden'] = response.xpath('/html/body/div[3]/div[4]/div[1]/div/div[2]//div[1]/span//text()').extract_first()
    #     StaticItem['nCom_detail'] = '|'.join(response.xpath('/html/body/div[3]/div[4]/div[1]/div/div[2]//div[2]/span/span//text()').extract())
    #     StaticItem['oJoin_58'] = response.xpath('/html/body/div[3]/div[4]/div[1]/div/div[3]//p[3]/span//text()').extract_first()

    #     info_base_url = 'https://statisticszp.58.com/position/totalcount/?infoId={infoId}&userId={userId}'
    #     infoId = re.search('.*com\/\D+\/(\d+)x\.shtml\?.*', response.url).group(1)
    #     # userId 被包含在 公司网址里
    #     company_url = re.search(r'(https://qy.58.com/.*)', response.text).group(1)
    #     userId = re.search('.*com\/(\d+)\/\?ent.*?', company_url).group(1)

    #     yield scrapy.Request(info_base_url.format(infoId=infoId, userId=userId), callback=self.parse_detail, dont_filter=True, meta={'static': StaticItem,
    #                                                                                                             'html': response.url})


    # def parse_detail(self, response):
    #     """
    #     1.获取网页申请人数，招聘人数，评论数，简历反馈率
    #     2.param：body 获得网页响应正文，byte类型，需 decode()转码为 str类型
    #     3.将数据放在 DynamicItem 存储器中, 并传递
    #     """
    #     pattern = response.body.decode()
    #     DynamicItem = Cd58Item()

    #     # item 本身是字典类型，传递的 response.meta['static'] 同样也是 字典类型，所以可以直接赋值
    #     DynamicItem = response.meta['static']
    #     DynamicItem['rApply'] = re.search(r'.*"deliveryCount":(\d+),.*', pattern).group(1)
    #     DynamicItem['tApply_num'] = re.search(r'.*"infoCount":(\d+),.*', pattern).group(1)
    #     DynamicItem['uCommentCount'] = re.search(r'.*"commentCount":(\d+),.*', pattern).group(1)
    #     DynamicItem['sFeedback'] = re.search(r'.*"resumeReadPercent":(\d+),.*', pattern).group(1)

    #     # API 获取浏览量
    #     view_base_url = 'https://jst1.58.com/counter?infoid={infoID}&userid=&uname=&sid=0&lid=0&px=0&cfpath='
    #     infoID = re.search(r'.*?infoId=(\d+).*', response.url).group(1)
    #     #  58 同城的反爬虫措施，不加 headers 无法获取到数据(一直显示 0, 不要踩我的坑'.')
    #     headers = {
    #         'Referer': response.meta['html'],
    #         'Sec-Fetch-Mode': 'no-cors',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    #     }

    #     yield scrapy.Request(view_base_url.format(infoID=infoID), headers=headers, method='get', callback=self.parse_view, dont_filter=True, meta={'dynamic': DynamicItem})

    # def parse_view(self, response):
    #     """
    #     1. 完成对 浏览量的数据解析获取
    #     2. yield item
    #     """
    #     item = Cd58Item()

    #     item = response.meta['dynamic']
    #     item['qView'] = re.search(r'.*Counter58.total=(\d+)$', response.body.decode()).group(1)

    #     yield item


        
