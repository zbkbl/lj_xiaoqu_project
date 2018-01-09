# coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider
from lj_project.geturl import GetMissionUrl
from lj_project.Exception import timeUtils
import datetime
from lj_project.Exception.emailSender import emailSender


class GetResidencePrice(CrawlSpider):
    name = 'lj_xiaoqu_price'
    starts_urls = []
    custom_settings = {
            'ITEM_PIPELINES': {
                'lj_project.pipelines.LjProjectPipeline': 300,
            },
            'DOWNLOADER_MIDDLEWARES': {
                'lj_project.filter_url.LjprojectListingMiddleware': 310,
            },
            'DOWNLOAD_DELAY':0.2
    }

    def __init__(self):
        self.geturl = GetMissionUrl()
        self.mission_urls = self.geturl.get_lj_urls()

    def start_requests(self):
        for item in self.mission_urls:
            yield scrapy.Request(item['url'], meta={'key': item},
                                 callback=self.get_residence_price)

    def get_residence_price(self, response):
        select = scrapy.Selector(response)
        item = response.meta['key']
        avg_price = select.xpath('//*[@class="xiaoquUnitPrice"]/text()').extract_first()
        if avg_price is None:
            avg_price = select.xpath('//*[@id="zoneView"]/div[2]/div[2]/div/p[2]/span[1]/text()').extract_first()
        if avg_price is not None:
            item['avg_price'] = avg_price.strip()
        else:
            item['avg_price'] = None
        item['avg_time'] = timeUtils.getPriceTime()
        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %X')

        yield item

    @staticmethod
    def close(spider, reason):
        emailSenderClient = emailSender()
        toSendEmailLst = ['liuyang@zhongjiaxin.com']
        finishTime = datetime.datetime.now().strftime('%Y-%m-%d %X')
        subject = u"爬虫结束状态汇报"
        body = u"爬虫结束状态汇报：\n\
                爬虫名称：" + spider.name + u"\n\
                结束原因：" + reason + u"\n\
                结束时间：" + finishTime
        emailSenderClient.sendEmail(toSendEmailLst, subject, body, spider)
