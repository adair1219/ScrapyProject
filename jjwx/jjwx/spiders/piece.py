import scrapy
import pandas as pd
import re

from ..items import PieceItems

class PieceSpider(scrapy.Spider):
    name = 'piece'

    def __init__(self):
        '''
        陷阱：所有的 try except 都是因为有两套不同情况下的返回格式，需要
        分别处理
        '''
        piece_df = pd.read_csv(r'E:\爬虫\jjwx\data\piece_links.csv')
        self.piece_links = piece_df['piece_link'].unique().tolist()
        del piece_df

    def start_requests(self):
        for link in self.piece_links:
            url = f'https://www.jjwxc.net/{link}'
            yield scrapy.Request(url, callback=self.get_piece_info, dont_filter=True)

    def get_piece_info(self, response):
        piece_items = PieceItems()
        text = response.text
        piece_items['piece_url'] = response.url
        piece_items['文章类型'] = re.findall(r'itemprop="genre">\r\n(.*)</span>', text)[0].strip()
        piece_items['作品视角'] = re.findall(r'<span>作品视角：</span>\r\n(.*) </li>', text)[0].strip()
        piece_items['作品风格'] = re.findall(r'<li><span>作品风格：</span>(.*)</li>', text)[0].strip()
        piece_items['文章进度'] = re.findall(r'itemprop="updataStatus">.*(完结|暂停|连载).*</span>', text)[0]
        piece_items['全文字数'] = int(re.findall(r'itemprop="wordCount">(\d+)字</span>', text)[0])
        try:
            piece_items['签约状态'] = re.findall(r"签约状态：</span>\r\n.*<b>\r\n.*<font color='red'>(.*)</font>", text)[0]
        except:
            piece_items['签约状态'] = r'未签约'
        piece_items['文章名称'] = re.findall(r'itemprop="articleSection">(.*)</span> </h1>', text)[0]
        piece_items['总书评数'] = int(response.xpath('//*[@id="oneboolt"]/tbody/tr/td/div/span[2]/text()').get())
        piece_items['文章当前被收藏数'] = int(response.xpath('//*[@id="oneboolt"]/tbody/tr/td/div/span[3]/text()').get())
        piece_items['营养液数'] = int(response.xpath('//*[@id="oneboolt"]/tbody/tr/td/div/span[4]/text()').get())
        piece_items['文章积分'] = int(response.xpath('//*[@id="oneboolt"]/tbody/tr/td/div/text()[5]').re_first(r".*文章积分：(.*)").replace(',', ''))

        # 全站霸王排名通过 javascript 加载
        novelid = re.findall(r'.*novelid=(.*)', response.url)[0]
        ranking_url = f'https://s8-static.jjwxc.net/getKingTickets.php?ver=20170519&jsonpcallback=kingticketsortAll&novelid={novelid}&action=ticketsort&type=0'
        yield scrapy.Request(ranking_url, callback=self.get_ranking_other, dont_filter=True,
                             cb_kwargs={'piece_items': piece_items,
                                        'novelid': novelid})

    def get_ranking_other(self, response, piece_items, novelid):
        self.logger.info('正在获取霸王票排行...')
        text = response.text
        try:
            piece_items['霸王票全站排行'] = int(re.findall(r'.*"ranking":"(\d+)".*', text)[0])
            piece_items['前进一名所需地雷数'] = int(re.findall(r'.*"gap":"(\d+)".*', text)[0])
            piece_items['总共地雷数量'] = int(re.findall(r'.*"ticketNum":"(\d+)".*', text)[0])
        except:
            piece_items['霸王票全站排行'] = '暂无'
            piece_items['前进一名所需地雷数'] = 1
            piece_items['总共地雷数量'] = 0

        # 篇章点击量通过 javascript 加载
        click_url = f'https://s8-static.jjwxc.net/getnovelclick.php?novelid={novelid}&jsonpcallback=novelclick'
        yield scrapy.Request(click_url, callback=self.get_total_click_num, dont_filter=True,
                             cb_kwargs={'piece_items': piece_items})

    def get_total_click_num(self, response, piece_items):
        self.logger.info('正在获取总点击量...')
        try:
            novelclick_dict = eval(re.findall(r'novelclick(.*)', response.text)[0])
            piece_items['总点击量'] = sum([int(i) for i in novelclick_dict.values()])
        except:
            novelclick_list = re.findall(r'\d+', response.text)
            piece_items['总点击量'] = sum([int(i) for i in novelclick_list])

        yield piece_items

