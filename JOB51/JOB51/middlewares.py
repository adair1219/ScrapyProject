from scrapy import signals
from fake_useragent import UserAgent

class RandomUserAgentMiddlware():
    ## 随机更换 User-Agent
    def __init__(self):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.random)
        request.headers.setdefault('Cookie', None)
