import scrapy
import re
import time
from scrapy.selector import Selector

import winsound
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from lxml import etree

from ..items import JjwxItem

class JjwxcSpider(scrapy.Spider):
    name = 'jjwxc'
    # allowed_domains = ['jjwxc.net']

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.headless = False  # 开启无头模式
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe", chrome_options=options) 

        # profile = webdriver.FirefoxProfile()
        # profile.set_preference('network.proxy.type', 0)
        # self.browser = webdriver.Firefox(profile)
        
        ## 登录
        self.logger.info('请在30s内完成登录')
        login_url = r'https://www.jjwxc.net/bookbase_slave.php?t=0&booktype=vip&opt=&page=2&endstr=&orderstr=4'
        self.browser.get(login_url)
        time.sleep(30)

    def start_requests(self):
        self.logger.info(f'获取言情、原创、衍生、纯爱下的各个作品库，如VIP, 免费，完结，驻站，经典等...')
        for t in [0, 1, 2, 3]:
            for booktype in ['vip', 'package', '', 'sp', 'scriptures', 'free']:
            # for booktype in ['vip', 'free', 'package']: # 只有vip,free有200页，所以第二次只需要爬取这两个类型
                url = f'https://www.jjwxc.net/bookbase_slave.php?t={t}&booktype={booktype}&page=1'
                yield scrapy.Request(url, callback=self.get_page_num, dont_filter=True, cb_kwargs={'booktype': booktype})

    def get_page_num(self, response, booktype):
        items = JjwxItem()
        wait = WebDriverWait(self.browser, 180)
        page_num = response.xpath("/html/body/div[6]/font[1]/text()").get()
        self.logger.info(f'该类别下共 {page_num} 页-。-')
        base_url = re.findall(r'(.*&page=)', response.url)[0]
        for num in range(1, int(page_num)+1):
        # for num in range(187, int(page_num)+1): # 由于太过频繁访问，被ban了，第二次从101页开始访问
            url = base_url + str(num)
            self.browser.get(url)
            # 防止网卡，没有加载出页面，设置个显示等待
            next_page = wait.until(EC.presence_of_element_located((By.XPATH, r'/html/body/div[8]/span[2]/a')))

            html = self.browser.page_source
            response = etree.HTML(html)

            zpk_len = len(response.xpath('/html/body/div[7]/table/tbody/tr/td[2]/a/text()'))
            for i in range(2, zpk_len+2):
                items['作品库类型'] = booktype
                items['a_作者'] = response.xpath(f'/html/body/div[7]/table/tbody/tr[{i}]/td[1]/a/text()')[0]
                items['a_作者_url'] = response.xpath(f'/html/body/div[7]/table/tbody/tr[{i}]/td[1]/a/@href')[0]
                items['b_作品'] = response.xpath(f'/html/body/div[7]/table/tbody/tr[{i}]/td[2]/a/text()')[0]
                items['b_作品_url'] = response.xpath(f'/html/body/div[7]/table/tbody/tr[{i}]/td[2]/a/@href')[0]
                items['c_类型'] = response.xpath(f'/html/body/div[7]/table/tbody/tr[{i}]/td[3]/text()')[0].strip()
                items['d_风格'] = response.xpath(f'/html/body/div[7]/table/tbody/tr[{i}]/td[4]/text()')[0]
                try:
                    items['e_进度'] = response.xpath(f'/html/body/div[7]/table/tbody/tr[{i}]/td[5]/font/text()')[0] # 字体带颜色
                except:
                    items['e_进度'] = response.xpath(f'/html/body/div[7]/table/tbody/tr[{i}]/td[5]/text()')[0].strip()
                items['f_字数'] = response.xpath(f'/html/body/div[7]/table/tbody/tr[{i}]/td[6]/text()')[0]
                items['g_作品积分'] = response.xpath(f'/html/body/div[7]/table/tbody/tr[{i}]/td[7]/text()')[0]
                items['h_发表时间'] = response.xpath(f'/html/body/div[7]/table/tbody/tr[{i}]/td[8]/text()')[0]
                
                yield items