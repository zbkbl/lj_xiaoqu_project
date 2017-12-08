# coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider
from lj_project.geturl import GetMissionUrl
import datetime


class GetResidencePrice(CrawlSpider):
    name = 'lj_xiaoqu_price'
    starts_urls = []
    custom_settings = {
            'ITEM_PIPELINES': {
                'lj_project.pipelines.LjProjectPipeline': 300,
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
        item['avg_price'] = select.xpath('//*[@class="xiaoquUnitPrice"]/text()').extract_first()
        item['avg_time'] = u'2017/11'
        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %X')

        yield item