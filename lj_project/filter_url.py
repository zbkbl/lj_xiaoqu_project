# coding:utf-8
from lj_project.geturl import GetMissionUrl
from scrapy.exceptions import IgnoreRequest


class LjprojectSpiderMiddleware(object):

    def __init__(self):
        test = GetMissionUrl()
        self.urls = test.get_crawled_urls()

    def process_request(self, request, spider):
        if request.url in self.urls:
            spider.logger.info(request.url + "has been crawled !!")
            raise IgnoreRequest
        else:
            return None


class LjprojectDealMiddleware(object):

    def __init__(self):
        test = GetMissionUrl()
        self.urlList = test.get_crawled_deal_urls()

    def process_request(self, request, spider):
        if request.url in self.urlList:
            spider.logger.info(request.url + "has been crawled !!")
            raise IgnoreRequest
        else:
            return None
