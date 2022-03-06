import scrapy
import json
import re

from ..items import Job51Item

class Job51Spider(scrapy.Spider):
    name = 'job51'
    # allowed_domains = ['job51.com']
    start_urls = ['https://search.51job.com/list/090200,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE,3,1.html?']

    def parse(self, response):
        item = Job51Item()
        self.logger.info(f'Visit website {response.url}')
        self.logger.info('获取当前页面所有的工作链接')
        json_text = json.loads(re.findall(r".__SEARCH_RE.*ULT__ = (.*?)</script>", response.text)[0])
        self.logger.info('存储部分需要的字段')
        engine_jds = json_text['engine_jds']
        for i in range(len(engine_jds)):
            item['type'] = engine_jds[i]['type']
            item['jt'] = engine_jds[i]['jt']
            item['tags'] = engine_jds[i]['tags']
            item['ad_track'] = engine_jds[i]['ad_track']
            item['jobid'] = engine_jds[i]['jobid']
            item['coid'] = engine_jds[i]['coid']
            item['effect'] = engine_jds[i]['effect']
            item['is_special_job'] = engine_jds[i]['is_special_job']
            item['job_href'] = engine_jds[i]['job_href']
            item['job_name'] = engine_jds[i]['job_name']
            item['job_title'] = engine_jds[i]['job_title']
            item['company_href'] = engine_jds[i]['company_href']
            item['company_name'] = engine_jds[i]['company_name']
            item['providesalary_text'] = engine_jds[i]['providesalary_text']
            item['workarea'] = engine_jds[i]['workarea']
            item['workarea_text'] = engine_jds[i]['workarea_text']
            item['updatedate'] = engine_jds[i]['updatedate']
            item['iscommunicate'] = engine_jds[i]['iscommunicate']
            item['companytype_text'] = engine_jds[i]['companytype_text']
            item['degreefrom'] = engine_jds[i]['degreefrom']
            item['workyear'] = engine_jds[i]['workyear']
            item['issuedate'] = engine_jds[i]['issuedate']
            item['isFromXyz'] = engine_jds[i]['isFromXyz']
            item['isIntern'] = engine_jds[i]['isIntern']
            item['jobwelf'] = engine_jds[i]['jobwelf']
            item['isdiffcity'] = engine_jds[i]['isdiffcity']
            item['attribute_text'] = ','.join(engine_jds[i]['attribute_text'])
            item['companysize_text'] = engine_jds[i]['companysize_text']
            item['companyind_text'] = engine_jds[i]['companyind_text']
            item['adid'] = engine_jds[i]['adid']
            yield item

        self.logger.info(f'当前职位共有{int(json_text["total_page"])}页')
        for j in range(2, int(json_text['total_page'])):
            url = f'https://search.51job.com/list/090200,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE,{j+1},{j}.html?'
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)




