# -*- coding: utf-8 -*-

import scrapy
from lj_project.items import ResidenceInfoItem
import time
from scrapy.spiders import CrawlSpider
import datetime
from lj_project.Exception.emailSender import emailSender
city_dict = {
    'sh.lianjia': u'上海', 'su.lianjia':u'苏州'
}
url_dict = {
    'sh.lianjia': "http://sh.lianjia.com", 'su.lianjia':"http://su.lianjia.com"
}


class ShXiaoquSpider(CrawlSpider):
    name = "sh_xiaoqu_spider"
    allowed_domain = ["http://sh.lianjia.com",
                      'http://su.lianjia.com'
                      ]

    start_urls = ["http://sh.lianjia.com/xiaoqu",
                  "http://su.lianjia.com/xiaoqu"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES_BASE': {
            'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
            'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
            'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 500,
            'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
            'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
            'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
            'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 750,
            'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 800,
            'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,
            'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 900,
        },
        'DOWNLOADER_MIDDLEWARES': {
           'lj_project.filter_url.LjprojectSpiderMiddleware': 310,
            # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 'fangproject.useragent_middlewares.RandomUserAgent': 400,
        },
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {
        'lj_project.pipelines.LjProjectPipeline' : 300,
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse, dont_filter=True)

    # 获取区域
    def parse(self, response):
        URL = self.get_domain(response.url)
        select = scrapy.Selector(response)
        urls = select.xpath('//*[@id="filter-options"]/dl[1]/dd/div/a/@href').extract()
        for url in urls[1:]:
            new_url = URL + url
            yield scrapy.Request(url=new_url, callback=self.parse_community)

    def parse_community(self, response):
        select = scrapy.Selector(response)
        URL = self.get_domain(response.url)
        urls = select.xpath('//*[@id="filter-options"]/dl[1]/dd/div[2]/a/@href').extract()
        for url in urls[1:]:
            new_url = URL + url
            yield scrapy.Request(url=new_url, callback=self.parse_residence)

    def parse_residence(self, response):
        select = scrapy.Selector(response)
        URL = self.get_domain(response.url)
        res = select.xpath('//*[@id="house-lst"]/li')
        for li in res:
            url = li.xpath('div[2]/h2/a/@href').extract_first()
            district = li.xpath('div[2]/div[1]/div[2]/div/a[1]/text()').extract_first()
            community = li.xpath('div[2]/div[1]/div[2]/div/a[2]/text()').extract_first()
            item = ResidenceInfoItem()
            item['url'] = URL + url
            item['district'] = district
            item['community'] = community
            yield scrapy.Request(url=item['url'], meta={'item': item}, callback=self.parse_Info)
        next = select.xpath('//div[@class="page-box house-lst-page-box"]/a[@gahref="results_next_page"]/@href').extract_first()
        if next:
            new_url = URL + next
            yield scrapy.Request(url=new_url, callback=self.parse_residence)

    def parse_Info(self, response):
        item = response.meta['item']
        select = scrapy.Selector(response)
        residence_name = select.xpath('/html/body/div[4]/div[1]/section/div[1]/div[1]/span/h1/text()').extract_first()
        address = select.xpath('/html/body/div[4]/div[1]/section/div[1]/div[1]/span/span[2]/text()').extract_first()
        # 经纬度
        coordinate = select.xpath('//*[@id="actshowMap_xiaoqu"]/@xiaoqu').extract_first()
        if coordinate:
            coor = coordinate.split(',')
            item['coordinate'] = coor[0] + ','+ coor[1].strip() + ']'

        bd_time = select.xpath('//*[@id="zoneView"]/div[2]/div[3]/ol/li[2]/span/span/text()').extract_first()
        build_time = bd_time.strip().replace("~","-")

        property_price = select.xpath('//*[@id="zoneView"]/div[2]/div[3]/ol/li[3]/span/text()').extract_first().strip()

        property_company = select.xpath('//*[@id="zoneView"]/div[2]/div[3]/ol/li[4]/span/text()').extract_first().strip()

        developer = select.xpath('//*[@id="zoneView"]/div[2]/div[3]/ol/li[5]/span/text()').extract_first().strip()

        floor_sum = None

        house_sum = None

        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %X')
        for key in city_dict.keys():
            if key in response.url:
                item['city'] = city_dict[key]
        item['residence_name'] = residence_name
        item['address'] = address
        item['build_time'] = build_time
        item['property_price'] = property_price
        item['property_company'] = property_company
        item['developer'] = developer
        item['total_houses'] = floor_sum
        item['total_buildings'] = house_sum
        item['bsn_dt'] = str(datetime.date.today())
        item['webst_nm'] = u'链家'
        item['tms'] = time.strftime("%Y-%m-%d %X", time.localtime())
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

    def get_domain(self, url):
        for k,v in url_dict.items():
            if k in url:
                return v