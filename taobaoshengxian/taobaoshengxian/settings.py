# -*- coding: utf-8 -*-

# Scrapy settings for taobaoshengxian project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'taobaoshengxian'

SPIDER_MODULES = ['taobaoshengxian.spiders']
NEWSPIDER_MODULE = 'taobaoshengxian.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'taobaoshengxian (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 7
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
  'cookie': 'UM_distinctid=16dbeea145a249-03b8c1cd4f8885-396a4507-e1000-16dbeea145b20a; cna=yqElFh6EZFkCAWXOp2wwqcaQ; t=f6d34393e31b2270dc6cbe6c621c5c5f; thw=cn; lgc=tb096159174; tracknick=tb096159174; tg=0; enc=Y2ScmL8fx6m4E4%2F6ZdkPFbFlS03%2BkY4953viXOo2IIsDXnBrs7gJaOsPEraUMOlCvR967cAPAkqBLMvSyM1q9Q%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; miid=1535081682143655975; uc3=lg2=W5iHLLyFOGW7aA%3D%3D&vt3=F8dByuaz8N3yjbhqRds%3D&id2=Vy0Rob%2BmKWjVSA%3D%3D&nk2=F5RFif9lohi4U3Q%3D; uc4=id4=0%40VXqfuEpak5oQgWGiQpxPe%2FA%2FHSEz&nk4=0%40FY4O4HSk06fGssP00BG68YnCG7rh%2Fg%3D%3D; _cc_=WqG3DMC9EA%3D%3D; mt=ci=-1_0; hng=CN%7Czh-CN%7CCNY%7C156; cookie2=5b3bfe857939017ed6ade6e40ce94c97; v=0; _tb_token_=ae75093eee0a; CNZZDATA1256793290=1754150059-1570883198-%7C1574232196; uc1=cookie14=UoTbmVILHHRlkQ%3D%3D; l=dBSThko7q2sPO0s2BOCChurza779AIRvSuPzaNbMi_5Q56dMR8_OkL3QTFp6DjWfTGLB47_ypV99-etkmEy06Pt-g3fPVxDc.; isg=BPj4FRg00Y-Hdj1-YcDX4oXWyaZKyXfThjaLeTJpYTPNTZg32nGVezVvAAXYKBTD; JSESSIONID=621340D0000583D447158AB2918E3BC3',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'taobaoshengxian.middlewares.RandomProxyMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'taobaoshengxian.middlewares.TaobaoshengxianDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'taobaoshengxian.pipelines.TaobaoshengxianPipeline': 300,
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
