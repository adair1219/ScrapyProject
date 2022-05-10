import scrapy
import pandas as pd
import re

from ..items import ScoreItems

class ScoresSpider(scrapy.Spider):
    name = 'scores'

    def start_requests(self):
        article_df = pd.read_csv(r'E:\爬虫\jjwx\无关数据\article_url.csv')
        article_urls = article_df['piece_url']
        del article_df
        for url in article_urls:
            novelid = re.findall(r'novelid=(.*)', url)[0]
            ajax_url = f'https://www.jjwxc.net/novelreview.php?callback=novelreviewCallback&action=getByNovelid&novelid={novelid}'
            yield scrapy.Request(ajax_url, callback=self.get_avgscores, dont_filter=True,
                                 cb_kwargs={'url': url})

    def get_avgscores(self, response, url):
        items = ScoreItems()
        items['piece_url'] = url
        try:
            items['b_评分'] = float(re.findall(r'"avgscore":"(.*?)".*', response.text)[0])
        except:
            items['b_评分'] = '暂无'

        yield items


