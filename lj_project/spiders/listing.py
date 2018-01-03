# coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider
from lj_project.geturl import GetMissionUrl
import datetime
from scrapy.selector import Selector
from scrapy import Request
from lj_project.Exception import tryex
import re
import time


class LjListingSpider(CrawlSpider):
    name = 'lj_listing'
    starts_urls = []
    allowed_domain = [
        'https://bj.lianjia.com',
        'https://cd.lianjia.com',
        'https://jn.lianjia.com',
        'https://nj.lianjia.com',
        'https://qd.lianjia.com',
        # 'https://sh.lianjia.com',
        # # 'http://sh.lianjia.com',
        'https://hf.lianjia.com',
        'https://wh.lianjia.com',
        'https://xm.lianjia.com',
        'https://xa.lianjia.com',
        'https://gz.lianjia.com',
        'https://cq.lianjia.com',
        # 'http://su.lianjia.com'
    ]
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
        self.mission_urls = self.geturl.get_listing_urls()

    def start_requests(self):
        for item in self.mission_urls:
            yield scrapy.Request(item['url'], meta={'key': item},
                                 callback=self.get_deal_url)

    def get_deal_url(self, response):
        select = scrapy.Selector(response)
        item = response.meta['key']
        deal_url = select.xpath('//*[@id="goodSell"]/div/a/@href').extract_first()
        if deal_url:
            yield scrapy.Request(deal_url, meta={'key': item}, callback=self.get_esf_url)

    def get_esf_url(self, response):
        item = response.meta['key']
        esf_url = Selector(response).xpath('/html/body/div[4]/div[1]/ul/li/a/@href').extract()
        for url in esf_url:
            yield Request(
                url,
                meta={'key': item},
                callback=self.get_esf_info
            )
        page_box = Selector(response).xpath('//*[@class="page-box house-lst-page-box"]').extract_first()
        if page_box is not None:
            totalPage = eval(Selector(response).xpath('//@page-data').extract_first())['totalPage']
            curPage = eval(Selector(response).xpath('//@page-data').extract_first())['curPage']
            if totalPage > curPage:
                yield Request(
                    response.url[0:response.url.find('/', 34) + 1] + 'pg' + str(curPage + 1) + '/',
                    meta={'key': item},
                    callback=self.get_esf_url,
                )

    def get_esf_info(self, response):
        sr = Selector(response)
        item = response.meta['key']
        item['structure']         = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋户型').extract_first()
        item['orientation']       = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋朝向').extract_first()
        item['area']              = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'建筑面积').extract_first()
        item['inner_area']        = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'套内面积').extract_first()
        item['heating_style']     = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'供暖方式').extract_first()
        item['decoration']        = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'装修情况').extract_first()

        rec = re.compile(r'\d+')
        fl = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'所在楼层').extract_first()).split(' ')
    	if len(fl) == 2:
    		item['floor'] = fl[0]
    		item['total_floor'] = rec.findall(fl[1])[0]
        else:
    		item['floor'] = None
    		item['total_floor'] = None

        item['house_type_struct'] = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'户型结构').extract_first()
        item['build_type']        = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'建筑类型').extract_first()
        item['build_struct']      = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'建筑结构').extract_first()
        item['household']         = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'梯户比例').extract_first()
        item['elevator']          = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'配备电梯').extract_first()

        item['ring_num']          = sr.xpath('//*[@class="areaName"]/span[2]/text()[2]').extract_first()
        item['lj_num']            = sr.xpath('//*[@class="houseRecord"]/span[2]/text()').extract_first()

        item['house_age']         = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋年限').extract_first()
        item['property_type']     = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'交易权属').extract_first()
        item['house_type']        = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋用途').extract_first()
        item['house_owner']       = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'产权所属').extract_first()
        item['listing_date']      = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'挂牌时间').extract_first()
        item['total_price']       = sr.xpath('//span[@class="total"]/text()').extract_first()
        item['unit_price']        = sr.xpath('//span[@class="unitPriceValue"]/text()').extract_first()
        item['last_deal']         = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'上次交易').extract_first()
        item['mortgage']          = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../span[2]/text()' % u'抵押信息').extract_first()
        item['house_backup']      = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房本备件').extract_first()

        item['residence_url']               = item['url']
        item['crawl_time']        = time.strftime("%Y-%m-%d %X",time.localtime())
        item['bsn_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
        item['tms'] = time.strftime("%Y-%m-%d %X", time.localtime())
        item['webst_nm'] = u'链家'

        item['url'] = response.url
        yield item