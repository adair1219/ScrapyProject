import time
from scrapy import Spider, Request
import json
import re
import winsound
from selenium import webdriver
from selenium.common import exceptions
from lxml import etree
from ..items import BossItem
import pandas as pd

class ZhipinSpider(Spider):
    name = 'zhipin'
    # allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/wapi/zpgeek/common/data/citysites.json']
    handle_httpstatus_list = [302]

    def __init__(self):
        ## 想要爬取的城市
        self.city_name = r"成都"
        self.job_name = r"数据分析师"
        self.csv_path = r"数据分析师.csv"
        ck = "acw_tc=0bdd34c216343712024382713e01abc00f6f67f77d51a68d89c16d552bb32d; __zp_stoken__=a693dfH1SSnpGBXMlfgJzfHlfISkZdCUiY2IjdXtSCzUeNnduS2c8EHkvSzwhS3Y0TxwHMxNrJS57CjUAIDl5OTIDeks1Ok1JEl8aTxAmYgF2e0NYalVKeztqfkAUfVx%2FDSU1GxxDTw1LOjQ%3D"
        self.cks_dict = {i.split("=")[0] : i.split("=")[1] for i in ck.split(";")}
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-CN,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Connection': 'keep-alive',
            "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": '?0',
            "sec-ch-ua-platform": "Windows",
            "Upgrade-Insecure-Requests": 1,
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chrome_options.headless = True  # 开启无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe", chrome_options=chrome_options)
        self.browser.implicitly_wait(10)
    
    def parse(self, response):
        ### 获取城市id
        citysites = json.loads(response.body)
        city_dict = citysites["zpData"]
        for i in range(26):
            if city_dict[i]["name"] == self.city_name:
                city_code = city_dict[i]["code"]
                city_url = city_dict[i]["url"]
        url = f"https://www.zhipin.com{city_url}?ka=city-sites-{city_code}"
        yield Request(url=url, callback=self.get_zhuye, headers=self.headers, dont_filter=True)

    def get_zhuye(self, response):
        ### 获取具体行业的招聘信息，获取两个参数
        ## 1.ka 2.行业代码
        print(f"爬取--{self.job_name}--的招聘信息")
        job_list = []
        item = BossItem()
        job_code = response.xpath(r'//*[@id="main"]/div/div[1]').re_first(r'.*<a ka="search_.*" href="/(.*?)/">{}</a>'.format(self.job_name))
        search_job = re.search(r'.*-p(\d+)', job_code).group(1)
        url = f"https://www.zhipin.com/{job_code}/?ka=search_{search_job}"
        count = 1
        try:
            page_next = True
            while page_next:
                self.browser.get(url)
                if count==1:
                    jobs = self.browser.find_elements_by_xpath(r'//*[@id="main"]/div/div[3]/ul/li/div/div[1]/div[1]/div/div[1]/span[1]/a')
                    urls_job = [job.get_attribute("href") for job in jobs]
                    next_s = self.browser.find_elements_by_xpath(r'//*[@id="main"]/div/div[3]/div[3]/a')
                    next_ = next_s[-1].get_attribute("class")
                else:
                    jobs = self.browser.find_elements_by_xpath(r'//*[@id="main"]/div/div[2]/ul/li/div/div[1]/div[1]/div/div[1]/span[1]/a')
                    urls_job = [job.get_attribute("href") for job in jobs]
                    next_s = self.browser.find_elements_by_xpath(r'//*[@id="main"]/div/div[2]/div[2]/a')
                    next_ = next_s[-1].get_attribute("class")
                job_list.extend(urls_job)
                if next_ == "next disabled":
                    break
                next_page_url = next_s[-1].get_attribute("href")
                url = next_page_url
                count+=1
        except:
            jobs = self.browser.find_elements_by_xpath(r'//*[@id="main"]/div/div[3]/ul/li/div/div[1]/div[1]/div/div[1]/span[1]/a')
            urls_job = [job.get_attribute("href") for job in jobs]
            job_list.extend(urls_job)
            print("完毕")
        
        print(f"一共有{len(job_list)}个岗位")
        print(f"总共有{count}页")

        boss_item = {
            "url": job_list,
            "a_status": [],
            "b_title": [],
            "c_salary": [],
            "d_fuli": [],
            "e_city": [],
            "f_rq": [],
            "g_name": [],
            "h_info": [],
            "i_jobDes": [],
            # "j_comName": [],
            # "k_address": [],
        }
        for job_detail_url in job_list:
            self.browser.get(job_detail_url)
            html = self.browser.page_source
            response = etree.HTML(html)
            boss_item["a_status"].extend(response.xpath(r'//*[@id="main"]/div[1]/div/div/div[2]/div[1]/span/text()'))
            boss_item["b_title"].extend(response.xpath(r'//*[@id="main"]/div[1]/div/div/div[2]/div[2]/h1/text()'))
            boss_item["c_salary"].extend(response.xpath(r'//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span/text()'))
            boss_item["d_fuli"].extend([','.join(response.xpath(r'//*[@id="main"]/div[1]/div/div/div[3]/div[2]/span/text()'))])
            boss_item["e_city"].extend(response.xpath(r'//*[@id="main"]/div[1]/div/div/div[2]/p/a/text()'))
            boss_item["f_rq"].extend([','.join(response.xpath(r'//*[@id="main"]/div[1]/div/div/div[2]/p/text()'))])
            boss_item["g_name"].extend(response.xpath(r'//*[@id="main"]/div[3]/div/div[2]/div[1]/h2/text()[1]'))
            boss_item["h_info"].extend([','.join(response.xpath(r'//*[@id="main"]/div[3]/div/div[2]/div[1]/p/text()'))])
            boss_item["i_jobDes"].extend([','.join([des.strip() for des in response.xpath(r'//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div/text()')])])
            # boss_item["j_comName"].extend(response.xpath(r'//*[@id="main"]/div[3]/div/div[2]/div[2]/div[5]/div[1]/text()'))
            # boss_item["k_address"].extend(response.xpath(r'//*[@id="main"]/div[3]/div/div[2]/div[2]/div[6]/div/div[1]/text()'))
            
        pd.DataFrame(boss_item).to_csv(self.csv_path)
        self.browser.quit()

            


