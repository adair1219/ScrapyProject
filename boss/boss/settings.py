# Scrapy settings for boss project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'boss'

SPIDER_MODULES = ['boss.spiders']
NEWSPIDER_MODULE = 'boss.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'boss (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
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
  'Cookie': 'wt2=D5uIxZ3p1cYF-8-7h28BJGlN_1-I00kKxZfsdxNEF1tkbM993vjLRmR9XU7S6p8NlZvm7y8rHzALPOVX7E6oKAw~~; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1634118450,1634118477,1634118498,1634124544; lastCity=101270100; acw_tc=0bcb2f1816341794659708763e5d57e063ce754e4f21311e8750c0dfdba636; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1634179950; __zp_stoken__=6b6cdAF5kA3kZWzF%2Bcy5BcComVhZCSkpaGkgyVH87d3M6LloGCEwYd3l2EEFRLmldWn9%2BTxhkXTFxE3UEMVBZSFoMLV1qdWkBRAlQSxRGUR4fGDpdByZLIHZ%2BGRg8NjoWGEZMZxdEN004XXQ%3D; __c=1634124544; __a=79579767.1630238364.1634118287.1634124544.148.3.119.148; __zp_seo_uuid__=3af7d06c-aa81-4caf-bd87-4141df377452; __l=r=https%3A%2F%2Fwww.baidu.com%2Fs%3Ftn%3D59044660_hao_pg%26ie%3Dutf-8%26wd%3Dboss%2520%25E6%258B%259B%25E8%2581%2598%25E7%2588%25AC%25E5%258F%2596&l=%2Fzhaopin%2Fb4fd16db74e74ddc33x729u_%2F&s=1; geek_zp_token=V1QNogFeH83FlpVtRvzBkZISu37jPfwyk~',
  "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'boss.middlewares.BossSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'boss.middlewares.BossDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'boss.pipelines.BossPipeline': 300,
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
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
