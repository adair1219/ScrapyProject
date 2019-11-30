# -*- coding: utf-8 -*-
from scrapy import Request, Spider

from ..items import JingdongItem
# from ..items import CommentsItem

import re
import json
from scrapy_redis.spiders import RedisSpider

class FreshSpider(RedisSpider):
    name = 'fresh'
    # allowed_domains = ['fresh.jd.com']  通过注释这一行取消对域名的限制
    # start_urls = ['https://fresh.jd.com/']
    redis_key = 'fresh:start_urls'

    def __init__(self):
        self.pattern_one = re.compile(r"(https://search.jd.com/.*?)',")
        self.pattern_two = re.compile(r'keyword=(.*?)&.*')
        self.pattern_three = re.compile(r'(//item.jd.com/.*?)">')
        self.pattern_four = re.compile(r'.*原产地：(.*?)<')
        self.location = '四川'
        self.urls = []

    def parse(self, response):
        ''' 获取所有商品链接 '''
        urls = re.findall(self.pattern_one, response.text)
        for url in urls:
            yield Request(url, callback=self.get_all_pages, dont_filter=True)

        # url = 'https://search.jd.com/search?keyword=%E4%B8%91%E6%A9%98&enc=utf-8&qrst=1&stop=1&vt=2&wq=%E4%B8%91%E6%A9%98&stock=1&cid2=12221#J_searchWrap'
        # yield Request(url, callback=self.get_all_pages, dont_filter=True)

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
            if r'https:' in product_url:
                yield Request(product_url, callback=self.get_item_detail, headers=headers, dont_filter=True)
            else:
                # if 'https' not in product_url, then concat 'https://' to response.url
                product_url = r'https:' + product_url
                yield Request(product_url, callback=self.get_item_detail, headers=headers, dont_filter=True)

    def get_item_detail(self, response):
        '''
        get accurate detail with limitation by location field
        '''
        static = JingdongItem()  # 网页静态数据管道
        # headers = {
        #     'referer': response.url,
        #     'sec-fetch-mode': 'no-cors',
        #     'sec-fetch-site': 'same-site',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        # }
        try:
            location = re.search(self.pattern_four, response.text).group(1)
            print(location)
            if location == self.location:
                static['a_Loc'] = location
                static['b_Title'] = response.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li[1]/text()').extract_first()
                static['c_Mall'] = response.xpath('//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/text()').extract_first()
                static['d_Mall_url'] = response.xpath('//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/@href').extract_first()
                static['e_Brand'] = response.xpath('//*[@id="parameter-brand"]/li/a/text').extract_first()
                static['Z_Url'] = response.url
                try:
                    static['f_Sortable'] = re.search(r'类别：(.*?)<', response.text).group(1)
                    print('产品分类: ', static['f_Sortable'])
                except:
                    print('该商品没有类别，自动设为 ""')
                    static['f_Sortable'] = ''

                # 构遭 skuId，获取商品广告信息
                skuId = re.search(r'(\d+)', response.url).group(1)
                print('商品 ID 为', skuId)
                ad_url = f'https://cd.jd.com/promotion/v2?skuId={skuId}&area=22_1930_4284_0&cat=12218%2C13553%2C13573'
                yield Request(ad_url, callback=self.get_ad_info, dont_filter=True, meta={'static': static})
            else:
                print('原产地不在四川省，跳过')
                pass
        except:
            print('没有原产地字段，跳过')
            pass
                
    def get_ad_info(self, response):
        ''' 获取商品广告信息，利于挖掘出价值 '''
        print('正在获取商品广告信息.....')

        ad_info = JingdongItem()
        ad_info = response.meta['static']
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'browser.gwdang.com',
            'Referer': ad_info['Z_Url'],
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }

        ad_dict = json.loads(response.text)
        ads = ad_dict.get('ads')
        for num in range(0, len(ads)):
            ad_info['g_Ads'] = ads[num].get('ad')
        
        # 构造 skuId, venderId(mall_id), 获取价格，配送信息
        # 有些商家 venderId 并不在商家url 中，所有在 v2 API 
        # 接口获取 venderId，同时获取 skuId
        skuId = ad_dict.get('couponLimit')[0].get('sku')
        print('正在获取商品价格......')
        price_url = f'https://browser.gwdang.com/brwext/dp_query_latest?url=https%3A%2F%2Fitem.jd.com%2F{skuId}.html'
        yield Request(price_url, callback=self.get_price_info, headers=headers, dont_filter=True, meta={
            'ad_info': ad_info,
            'skuId': skuId,
            })

    def get_price_info(self, response):
        ''' 获取商品价格 '''
        skuId = response.meta['skuId']
        price_info = JingdongItem()
        price_info = response.meta['ad_info']

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'c0.3.cn',
            'Referer': price_info['Z_Url'],
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }

        result = json.loads(response.text)
        try:
            l_price = str(result.get('b2c').get('store')[0].get('price'))  # 价格转化为字符串，方便后续处理
            price = l_price[0:-2] + '.' + l_price[-2:]  # 对价格进行处理，如 4990 --> 49.90
        except:
            print('没有价格字段，自动设为 None')
            price = 'None'

        try:
            venderId = re.search(r'(\d+)', price_info['d_Mall_url']).group(0)
        except:
            print('商家 url 中未含有 venderId, 自动设为 0')
            venderId = 0

        param = '{%22originid%22:%221%22}'
        # 京东服务器端出现了问题，会出现 500 错误，只有等其修复才能爬取完整字段
        stock_url = f'https://c0.3.cn/stock?skuId={skuId}&area=22_1930_4284_0&venderId={venderId}&buyNum=1&choseSuitSkuIds=&cat=12218,12222,12242&extraParam={param}&fqsp=0&pdpin=&'
        # stock_url = f'https://c0.3.cn/stock?skuId={skuId}&area=22_1930_4284_0&venderId={venderId}&cat=12218,12222,12242&'
        yield Request(stock_url, self.get_extra_info, headers=headers, dont_filter=True, meta={
            'price_info': price_info,
            'price': price,
            'skuId': skuId,
        })

    def get_extra_info(self, response):
        ''' 获取商品价格，配送信息 '''
        print('广告信息已获取完，正在获取额外信息......')
        print(response.url)
        print(response.text)
        extra_info = JingdongItem()
        extra_info = response.meta['price_info']
        price = response.meta['price']
        skuId = response.meta['skuId']

        extra_dict = json.loads(response.text)
        extra_info['i_State'] = extra_dict.get('StockStateName')
        # extra_info['j_CashDesc'] = extra_dict.get('dcashDesc')
        extra_info['k_JdPrice'] = price
        # extra_info['l_PromiseMark'] = extra_dict.get('promiseMark')
        # extra_info['m_PromiseResult'] = extra_dict.get('promiseResult')

        province = extra_dict.get('area').get('provinceName')
        city = extra_dict.get('area').get('cityName')
        extra_info['h_StartCity'] = province + city
            
        # 构造 productId(skuId), page, 获取商品所有评价
        for page in range(0, 100):
            comment_url = f'https://sclub.jd.com/comment/productPageComments.action?productId={skuId}&score=0&sortType=5&page={page}&pageSize=10'
            yield Request(comment_url, callback=self.get_comments, dont_filter=True, meta={
                'product_info': extra_info,
                })
    
    def get_comments(self, response):
        '''
        通过接收 self.parse_product 传递的函数，去除内容
        中杂余的不需要的内容，如Jquery 这种标识每个信息的
        东西，其实它不重要，直接去除。
        网页数据格式为 json，用json.loads 方法转化为python
        的字典，方便处理
        '''
        print('正在获取商品评价..........')
        item = JingdongItem()
        item = response.meta['product_info']

        _dict = json.loads(response.text)
        item['D_commentCount'] = _dict.get('productCommentSummary').get('commentCount')
        item['E_afterCount'] = _dict.get('productCommentSummary').get('afterCount')
        item['F_generalCount'] = _dict.get('productCommentSummary').get('generalCount')
        item['G_goodCount'] = _dict.get('productCommentSummary').get('goodCount')
        item['H_goodRate'] = _dict.get('productCommentSummary').get('goodRate')
        item['I_poorCount'] = _dict.get('productCommentSummary').get('poorCount')
        item['J_score1Count'] = _dict.get('productCommentSummary').get('score1Count')
        item['K_score2Count'] = _dict.get('productCommentSummary').get('score2Count')
        item['L_score3Count'] = _dict.get('productCommentSummary').get('score3Count')
        item['M_score4Count'] = _dict.get('productCommentSummary').get('score4Count')
        item['N_score5Count'] = _dict.get('productCommentSummary').get('score5Count')

        # 获取 comments, hottag下的内容，为list，求个数，分别爬取
        # 较之 comments 爬虫，优化了算法
        comments_list = _dict.get('comments')
        for num in range(0, len(comments_list)):
            item['A_comments'] = comments_list[num].get('content')

        hottag_list = _dict.get('hotCommentTagStatistics')
        for length in range(0, len(hottag_list)):
            item['B_hottag'] = hottag_list[length].get('name')
            item['C_hottag_number'] = hottag_list[length].get('count')

        yield item



