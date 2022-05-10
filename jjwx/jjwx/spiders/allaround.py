import scrapy
import re
from scrapy_redis.spiders import RedisSpider

from ..items import AllItems

class AllaroundSpider(RedisSpider):
    name = 'allaround'
    redis_key = 'allaround_start_urls'
    # start_urls = ['https://www.jjwxc.net/scorelist.php?scorestep=0']  # 超级

    def parse(self, response):
        start_urls_ = ['https://www.jjwxc.net/scorelist.php?scorestep=0']  # 超级
        start_urls_.extend([f'http://www.jjwxc.net/scorelist.php?scorestep=1&page={i}' for i in range(1, 6 + 1)])  # 十亿
        start_urls_.extend([f'http://www.jjwxc.net/scorelist.php?scorestep=2&page={i}' for i in range(1, 27 + 1)])  # 亿级
        start_urls_.extend([f'http://www.jjwxc.net/scorelist.php?scorestep=3&page={i}' for i in range(1, 50 + 1)])  # 千万级
        for url in start_urls_:
            yield scrapy.Request(url, callback=self.get_author_links, dont_filter=True)

    def get_author_links(self, response):
        author_links = re.findall(r'<a href="(oneauthor.*)">', response.text)
        for link in author_links:
            url = f'https://www.jjwxc.net/{link}'
            yield scrapy.Request(url, self.get_author_info, dont_filter=True)

    def get_author_info(self, response):
        items = AllItems()
        text = response.text

        items['author_url'] = response.url
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

        # 获取该作者下的可用文章链接
        all_piece_links = re.findall(r'<a href=(onebook.php?.*)>\n', text)
        piece_links = list(set([x.strip() for x in all_piece_links if len(x) < 40]))

        # 作者发出的红包数通过 ajax 方法，即需要单独请求一个 网页来获取
        authorid = re.findall(r'.*authorid=(.*)', response.url)[0]
        ajax_url = f'https://my.jjwxc.net/backend/red_envelope.php?action=redtotal&authorid={authorid}'
        yield scrapy.Request(ajax_url, callback=self.get_red_envelope_number,
                             cb_kwargs={'items': items, 'piece_links': piece_links})

    def get_red_envelope_number(self, response, items, piece_links):
        items['a_作者所发送红包数'] = int(re.findall('.*total.*:"(.*)"', response.text)[0])

        for link in piece_links:
            url = f'https://www.jjwxc.net/{link}'
            yield scrapy.Request(url, callback=self.get_piece_info, dont_filter=True,
                                 cb_kwargs={'items': items})

    def get_piece_info(self, response, items):
        text = response.text
        items['piece_url'] = response.url
        items['b_文章类型'] = re.findall(r'itemprop="genre">\r\n(.*)</span>', text)[0].strip()
        items['b_作品视角'] = re.findall(r'<span>作品视角：</span>\r\n(.*) </li>', text)[0].strip()
        items['b_作品风格'] = re.findall(r'<li><span>作品风格：</span>(.*)</li>', text)[0].strip()
        items['b_文章进度'] = re.findall(r'itemprop="updataStatus">.*(完结|暂停|连载).*</span>', text)[0]
        items['b_全文字数'] = int(re.findall(r'itemprop="wordCount">(\d+)字</span>', text)[0])
        try:
            items['b_签约状态'] = re.findall(r"签约状态：</span>\r\n.*<b>\r\n.*<font color='red'>(.*)</font>", text)[0]
        except:
            items['b_签约状态'] = r'未签约'
        items['b_文章名称'] = re.findall(r'itemprop="articleSection">(.*)</span> </h1>', text)[0]
        items['b_总书评数'] = int(response.xpath('//*[@id="oneboolt"]/tbody/tr/td/div/span[2]/text()').get())
        items['b_文章当前被收藏数'] = int(response.xpath('//*[@id="oneboolt"]/tbody/tr/td/div/span[3]/text()').get())
        items['b_营养液数'] = int(response.xpath('//*[@id="oneboolt"]/tbody/tr/td/div/span[4]/text()').get())
        items['b_文章积分'] = int(response.xpath('//*[@id="oneboolt"]/tbody/tr/td/div/text()[5]').re_first(r".*文章积分：(.*)").replace(',', ''))

        # 全站霸王排名通过 javascript 加载
        novelid = re.findall(r'.*novelid=(.*)', response.url)[0]
        ranking_url = f'https://s8-static.jjwxc.net/getKingTickets.php?ver=20170519&jsonpcallback=kingticketsortAll&novelid={novelid}&action=ticketsort&type=0'
        yield scrapy.Request(ranking_url, callback=self.get_ranking_other, dont_filter=True,
                             cb_kwargs={'items': items,
                                        'novelid': novelid})

    def get_ranking_other(self, response, items, novelid):
        self.logger.info('正在获取霸王票排行...')
        text = response.text
        try:
            items['b_霸王票全站排行'] = int(re.findall(r'.*"ranking":"(\d+)".*', text)[0])
            items['b_前进一名所需地雷数'] = int(re.findall(r'.*"gap":"(\d+)".*', text)[0])
            items['b_总共地雷数量'] = int(re.findall(r'.*"ticketNum":"(\d+)".*', text)[0])
        except:
            items['b_霸王票全站排行'] = '暂无'
            items['b_前进一名所需地雷数'] = 1
            items['b_总共地雷数量'] = 0

        # 篇章点击量通过 javascript 加载
        click_url = f'https://s8-static.jjwxc.net/getnovelclick.php?novelid={novelid}&jsonpcallback=novelclick'
        yield scrapy.Request(click_url, callback=self.get_total_click_num, dont_filter=True,
                             cb_kwargs={'items': items})

    def get_total_click_num(self, response, items):
        self.logger.info('正在获取总点击量...')
        try:
            novelclick_dict = eval(re.findall(r'novelclick(.*)', response.text)[0])
            items['b_总点击量'] = sum([int(i) for i in novelclick_dict.values()])
        except:
            novelclick_list = re.findall(r'\d+', response.text)
            items['b_总点击量'] = sum([int(i) for i in novelclick_list])

        yield items





