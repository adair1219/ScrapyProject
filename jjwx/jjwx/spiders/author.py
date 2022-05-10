import scrapy
import pandas as pd

import re
from ..items import AuthorItem

class AuthorSpider(scrapy.Spider):
    name = 'author'
    # 爬取作者相关信息

    def __init__(self):
        author_df = pd.read_csv(r'E:\爬虫\jjwx\data\author_links.csv')
        self.author_links = author_df['author_link'].unique().tolist()
        del author_df

    def start_requests(self):
        for link in self.author_links:
            url = f'https://www.jjwxc.net/{link}'
            yield scrapy.Request(url, self.get_info, dont_filter=True)

    def get_info(self, response):
        items = AuthorItem()
        text = response.text

        items['a_作者'] = re.findall(r'.*<title>(.*) 的专栏.*', text)[0]
        items['a_被收藏数'] = int(re.findall(r'.*被收藏数：(\d+).*', text)[0])
        items['a_最近更新作品'] = response.xpath('/html/body/table[3]/tbody/tr/td/font/a/text()').get()
        # 陷阱1：需要注意字体颜色
        d_state = response.xpath('/html/body/table[3]/tbody/tr/td/font/font[1]/font/text()').get()
        if isinstance(d_state, str):
            items['a_作品状态'] = d_state
        else:
            items['a_作品状态'] = response.xpath('/html/body/table[3]/tbody/tr/td/font/font[1]/text()').get()
        items['a_作品字数'] = int(response.xpath('/html/body/table[3]/tbody/tr/td/font/font[2]/text()').get())
        items['a_最后更新时间'] = response.xpath('/html/body/table[3]/tbody/tr/td/text()').getall()[1].strip()

        # 最难的一个指标完本率
        items['a_小说完本数'] = len(re.findall('.*>(完结)</font.*', text))
        items['a_小说连载数'] = len(re.findall('.*>(连载)</td.*', text))
        items['a_小说暂停数'] = len(re.findall('.*>(暂停)</font.*', text))

        # 作者发出的红包数通过 ajax 方法，即需要单独请求一个 网页来获取
        authorid = re.findall(r'.*authorid=(.*)', response.url)[0]
        ajax_url = f'https://my.jjwxc.net/backend/red_envelope.php?action=redtotal&authorid={authorid}'
        yield scrapy.Request(ajax_url, callback=self.get_red_envelope_number, cb_kwargs={'items': items})

    def get_red_envelope_number(self, response, items):
        items['a_作者所发送红包数'] = int(re.findall('.*total.*:"(.*)"', response.text)[0])
        yield items

