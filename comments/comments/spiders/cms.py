# -*- coding: utf-8 -*-
from scrapy import Spider, Request

from ..items import CommentsItem

import re
import time
import json
from scrapy_redis.spiders import RedisSpider

class CmsSpider(RedisSpider):
    name = 'cms'
    # allowed_domains = ['fresh.jd.com']
    # start_urls = ['https://fresh.jd.com/']  #  爬取京东农产品的所有评论内容
    redis_key = 'cms:start_urls'

    def __init__(self):
        '''
        精准爬取四川产地的农产品，可根据需求自定义城市
        京东没有比较复杂的反爬虫措施，1.对数据的展示数量
        做了限制，跟 letpub 一样。
        2. 每个网页请求都需要 referer 这个字段，否则无法爬取

        每个网页不同需要的字段都通过 meta 参数传递
        '''
        self.location = '四川'


    def parse(self, response):
        ''' 获取所有农产品的编码 '''
        urls = re.findall(r"(https://search.jd.com/.*?)',", response.text)
        for url in urls:
            yield Request(url, callback=self.get_pages, dont_filter=True)

    def get_pages(self, response):
        ''' 获取网页页数，爬虫全站农产品 '''
        base_page_url = 'https://search.jd.com/search?keyword={keyword}&enc=utf-8&page={page}'
        keyword = re.search(r'keyword=(.*?)&.*', response.url).group(1)
        
        for pg in range(1, 101):
            page = pg * 2
            headers = {
                'refer': response.url,
                'sec-fecth-mode': 'cors',
                'sec-fecth-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            }
            ajax_url = 'https://search.jd.com/s_new.php?keyword={keyword}&enc=utf-8$page={page}'.format(keyword=keyword, page=page)
            #  网页通过 JS 异步处理方式，加载余下的商品数量（20），通过请求异步网页获取一页的全部商品
            yield Request(base_page_url.format(keyword=keyword, page=page), callback=self.parse_product, dont_filter=True)
            yield Request(ajax_url, callback=self.parse_product, headers=headers, dont_filter=True)

    def parse_product(self, response):
        ''' 获取每个具体商品的详情页面 '''
        urls = response.xpath('//*[@id="J_goodsList"]/ul/li/div/div[3]/a/@href').extract()
        headers = {
            'cache-control': 'max-age=0',
            'referer': response.url,
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': 1,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        }
        for url_worse in urls:
            url = 'https://' + url_worse
            yield Request(url, callback=self.parse_detail, headers=headers, dont_filter=True)

    def parse_detail(self, response):
        ''' 通过原产地字段的限制，获取四川境内的农产品 '''
        static = CommentsItem()
        try:
            location = re.search(r'.*原产地：(.*?)<', response.text).group(1)
            if location == self.location:
                static['url'] = response.url
                static['b_brand'] = response.xpath('//*[@id="parameter-brand"]/li/a/text()').extract_first()
                static['a_location'] = location
                try:
                    static['c_sortable'] = re.search(r'类别：(.*?)<', response.text).group(1)
                    comment_url = 'https://sclub.jd.com/comment/productPageComments.action?productId={id}&score=0&sortType=5&page={page}&pageSize=10'
                    headers = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'none',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests':1,
                        'cookie': '__jdu=1570883944805363619319; PCSYCityID=CN_510000_510100_0; shshshfpa=e6af0dfe-946f-244b-cc3e-92e03fad1c1f-1570883949; unpl=V2_ZzNtbUFeFkJ0DUFVKB5YAmIDE1lLBUEXIg0VBihNW1cyARtdclRCFX0URlVnGVkUZAIZXkVcQRxFCEdkfh1eAmUzIlxyVEMlfThGUH0YVQxlCxdYS1ZHF3IKQVRzG1wNVzMVbXIMFntwD0AHKxkMBWcAQApKZ0MQdwhBVX4bXw1XAiJdR15EHXEKRVJ%2fKRdrZk4SWURWShx3AENRchhYB2ABFV1KVUMdRQl2Vw%3d%3d; areaId=2; ipLoc-djd=2-2815-51975-0; __jdv=76161171|www.infinitynewtab.com|t_45363_|tuiguang|28df0460b65641058c33f4bcbe6cd381)|1571062268679; UM_distinctid=16dce2aa6de1ce-0e9791677412df-396a4507-e1000-16dce2aa6df121; shshshfpb=crXFr3eHVqzp%2FD4fGjVKEnQ%3D%3D; __jda=122270672.1570883944805363619319.1570883945.1571188508.1571206370.11; __jdc=122270672; 3AB9D23F7A4B3C9B=6AVXYQ3RGYS36VTILBVPDH27R5IMXZHKJSTSQD3NZKDY2DQ4LLCLXIKUBUV3JN6GV5UHAZXPXSFIN3FJQRGLOX6H2Y; shshshfp=4ddf86fb372fc0ae2c769289b0493c85; __jdb=122270672.5.1570883944805363619319|11.1571206370; shshshsID=8a7086feb122ec6f82b48522785b6331_4_1571206753783; CNZZDATA1256793290=2058792165-1571121576-%7C1571205840; JSESSIONID=0A994E9F8E3592C8F702A0C0D5F29CFC.s1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
                    }
                    id = re.search(r'.*com/(\d+).html', response.url).group(1)
                    for page in range(0, 100):
                        yield Request(comment_url.format(id=id, page=page), headers=headers, callback=self.parse_comment, dont_filter=True, meta={'static': static})
                except:
                    static['c_sortable'] = 'N/A'
                    comment_url = 'https://sclub.jd.com/comment/productPageComments.action?productId={id}&score=0&sortType=5&page={page}&pageSize=10'
                    headers = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'none',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests':1,
                        'cookie': '__jdu=1570883944805363619319; PCSYCityID=CN_510000_510100_0; shshshfpa=e6af0dfe-946f-244b-cc3e-92e03fad1c1f-1570883949; unpl=V2_ZzNtbUFeFkJ0DUFVKB5YAmIDE1lLBUEXIg0VBihNW1cyARtdclRCFX0URlVnGVkUZAIZXkVcQRxFCEdkfh1eAmUzIlxyVEMlfThGUH0YVQxlCxdYS1ZHF3IKQVRzG1wNVzMVbXIMFntwD0AHKxkMBWcAQApKZ0MQdwhBVX4bXw1XAiJdR15EHXEKRVJ%2fKRdrZk4SWURWShx3AENRchhYB2ABFV1KVUMdRQl2Vw%3d%3d; areaId=2; ipLoc-djd=2-2815-51975-0; __jdv=76161171|www.infinitynewtab.com|t_45363_|tuiguang|28df0460b65641058c33f4bcbe6cd381)|1571062268679; UM_distinctid=16dce2aa6de1ce-0e9791677412df-396a4507-e1000-16dce2aa6df121; shshshfpb=crXFr3eHVqzp%2FD4fGjVKEnQ%3D%3D; __jda=122270672.1570883944805363619319.1570883945.1571188508.1571206370.11; __jdc=122270672; 3AB9D23F7A4B3C9B=6AVXYQ3RGYS36VTILBVPDH27R5IMXZHKJSTSQD3NZKDY2DQ4LLCLXIKUBUV3JN6GV5UHAZXPXSFIN3FJQRGLOX6H2Y; shshshfp=4ddf86fb372fc0ae2c769289b0493c85; __jdb=122270672.5.1570883944805363619319|11.1571206370; shshshsID=8a7086feb122ec6f82b48522785b6331_4_1571206753783; CNZZDATA1256793290=2058792165-1571121576-%7C1571205840; JSESSIONID=0A994E9F8E3592C8F702A0C0D5F29CFC.s1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
                    }
                    id = re.search(r'.*com/(\d+).html', response.url).group(1)
                    for page in range(0, 100):
                        yield Request(comment_url.format(id=id, page=page), headers=headers, callback=self.parse_comment, dont_filter=True, meta={'static': static})
            else:
                pass
        except:
            pass

    def parse_comment(self, response):
        '''
        通过接收 self.parse_product 传递的函数，去除内容
        中杂余的不需要的内容，如Jquery 这种标识每个信息的
        东西，其实它不重要，直接去除。
        网页数据格式为 json，用json.loads 方法转化为python
        的字典，方便处理
        '''
        item = CommentsItem()
        item = response.meta['static']

        _dict = json.loads(response.text)
        for num in range(0, 10):
            try:
                item['d_comments'] = _dict.get('comments')[num].get('content')
                item['e_hottag'] = _dict.get('hotCommentTagStatistics')[num].get('name')
            except:
                pass
        item['f_afterCount'] = _dict.get('productCommentSummary').get('afterCount')
        item['g_commentCount'] = _dict.get('productCommentSummary').get('commentCount')
        item['h_generalCount'] = _dict.get('productCommentSummary').get('generalCount')
        item['i_goodCount'] = _dict.get('productCommentSummary').get('goodCount')
        item['j_goodRate'] = _dict.get('productCommentSummary').get('goodRate')
        item['k_poorCount'] = _dict.get('productCommentSummary').get('poorCount')

        yield item



        



        

        
        
        
            


