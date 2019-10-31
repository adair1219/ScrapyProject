# -*- coding: utf-8 -*-

# Scrapy settings for cd58 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


BOT_NAME = 'cd58'

SPIDER_MODULES = ['cd58.spiders']
NEWSPIDER_MODULE = 'cd58.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cd58 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
import random

DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  ':authority': 'cd.58.com',
  ':method': 'GET',
  ':scheme': 'https',
  'accept-encoding': 'gzip, deflate, br',
  'accept-language': 'zh-CN,zh;q=0.9',
  'cache-control': 'max-age=0',
  # 'cookie': 'commontopbar_new_city_info=102%7C%E6%88%90%E9%83%BD%7Ccd; commontopbar_ipcity=cd%7C%E6%88%90%E9%83%BD%7C0; f=n; id58=e87rZl2OtBtQ9Sm0CHupAg==; 58tj_uuid=888ecf43-b2c9-44f9-8bcf-9d7eaebb0409; als=0; xxzl_deviceid=IaJ14fuv%2B23Nmw%2F%2FBVg21oATZBQEu92OeXrlkWYxK7NW41OpgkCOxkPxL3tb6yID; wmda_uuid=9b165c4543df1caff4b0365721cbbe14; wmda_new_uuid=1; wmda_visited_projects=%3B1731916484865; gr_user_id=bc602b89-0ebd-4152-a48f-cf2443be5aa4; myfeet_tooltip=end; Hm_lvt_b4a22b2e0b326c2da73c447b956d6746=1570087936; __utma=253535702.133325547.1569674343.1569674343.1570092501.2; __utmz=253535702.1570092501.2.2.utmcsr=sh.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/zplvyoujiudian/36585961941412x.shtml; city=cd; 58home=cd; commontopbar_new_city_info=102%7C%E6%88%90%E9%83%BD%7Ccd; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1570087996,1570094268,1570110899,1570155164; wmda_session_id_1731916484865=1570165072303-592f6dc2-b062-1951; new_uv=31; utm_source=; spm=; init_refer=; gr_session_id_b4113ecf7096b7d6=b7bd01a7-f698-40af-b378-e39de16db802; gr_session_id_b4113ecf7096b7d6_b7bd01a7-f698-40af-b378-e39de16db802=true; new_session=0; sessionid=1e2af397-59f4-4a5a-aba9-48fef5d199b3; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1570158008,1570165075,1570165285,1570165623; Hm_lpvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1570165623; ppStore_fingerprint=EA47A9ABA8F41E4F05F4DF46FED33C7B124302E3B32DAC55%EF%BC%BF1570165624149',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'cd58.middlewares.ProxyMiddleware': 543,
   'cd58.middlewares.RandomUserAgentMiddlware': 333,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'cd58.middlewares.Cd58DownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'cd58.pipelines.Cd58Pipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

HTTPERROR_ALLOWED_CODES = [301]

# # # 分布式爬虫功能设置
# DUPEFILTER_CLASS = 'scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter' # 去重调用, 避免重复调用, 原理使用 redis 数据库的集合特性，集合的唯一性
# SCHEDULER = 'scrapy_redis_bloomfilter.scheduler.Scheduler' # 开启调度引擎
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
# SCHEDULER_PERSIST = True # 是否在关闭时保留原来的记录

# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379


