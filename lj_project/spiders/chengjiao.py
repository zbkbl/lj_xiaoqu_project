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


class GetResidencePrice(CrawlSpider):
    name = 'lj_chengjiao'
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
        # 'http://su.lianjia.com'
    ]
    custom_settings = {
            'ITEM_PIPELINES': {
                'lj_project.pipelines.LjProjectPipeline': 300,
            },
            'DOWNLOADER_MIDDLEWARES': {
            'lj_project.filter_url.LjprojectDealMiddleware': 310,

            },
            'DOWNLOAD_DELAY':0.2
    }

    def __init__(self):
        self.geturl = GetMissionUrl()
        self.mission_urls = self.geturl.get_chengjiao_urls()

    def start_requests(self):
        for item in self.mission_urls:
            yield scrapy.Request(item['url'], meta={'key': item},
                                 callback=self.get_deal_url)

    def get_deal_url(self, response):
        select = scrapy.Selector(response)
        item = response.meta['key']
        deal_url = select.xpath('//*[@id="frameDeal"]/a/@href').extract_first()
        if deal_url:
            yield scrapy.Request(deal_url, meta={'key': item}, callback=self.get_deal_list)

    def get_deal_list(self, response):
        select = scrapy.Selector(response)
        item = response.meta['key']
        detail_url = select.xpath('/html/body/div[5]/div[1]/ul/li/a/@href').extract()
        for url in detail_url:
            yield Request(
                url,
                meta={'key': item},
                callback=self.get_deal_info
            )

        page_box = Selector(response).xpath('//*[@class="page-box house-lst-page-box"]').extract_first()
        if page_box is not None:
            totalPage = eval(Selector(response).xpath('//@page-data').extract_first())['totalPage']
            curPage = eval(Selector(response).xpath('//@page-data').extract_first())['curPage']
            if totalPage > curPage:
                next_page_url = response.url[0:33] + response.url.split('/')[4] + '/' + 'pg' + str(curPage + 1) + '/'
                yield Request(
                    next_page_url,
                    meta={'key':item},
                    callback=self.get_deal_url
                )

    def get_deal_info(self, response):
        item = response.meta['key']

        sr = Selector(response)

        item['structure']         = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋户型').extract_first())
        item['orientation']       = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋朝向').extract_first())
        item['area']              = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'建筑面积').extract_first())
        item['inner_area']        = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'套内面积').extract_first())
        item['heating_style']     = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'供暖方式').extract_first())
        item['decoration']        = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'装修情况').extract_first())

        rec = re.compile(r'\d+')
        fl = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'所在楼层').extract_first()).split(' ')
    	if len(fl) == 2:
    		item['floor'] = fl[0]
    		item['total_floor'] = rec.findall(fl[1])[0]
        else:
    		item['floor'] = None
    		item['total_floor'] = None

        item['house_type_struct'] = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'户型结构').extract_first())
        item['build_type']        = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'建筑类型').extract_first())
        item['build_struct']      = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'建筑结构').extract_first())
        item['household']         = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'梯户比例').extract_first())
        item['elevator']          = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'配备电梯').extract_first())

        item['house_age']         = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋年限').extract_first())
        item['property_type']     = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'交易权属').extract_first())
        item['house_type']        = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋用途').extract_first())
        item['house_owner']       = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房权所属').extract_first())
        item['listing_date']      = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'挂牌时间').extract_first())
        item['listing_price']     = tryex.strip(sr.xpath('//div[@class="msg"]/span[1]/label/text()').extract_first())
        item['total_price']       = tryex.strip(sr.xpath('//span[@class="dealTotalPrice"]/i/text()').extract_first())

        transaction_date = tryex.strip(sr.xpath('//*[@class="house-title"]/div/span/text()').extract_first())
        if transaction_date:
             s = transaction_date.split(' ')[0]
             item['transaction_date'] = s.replace('.','-')

        else:
            item['transaction_date'] = None

        item['last_deal']         = tryex.strip(sr.xpath('//*[@id="chengjiao_record"]/ul/li[2]/p/text()').extract_first())
        item['deal_cycle']        = tryex.strip(sr.xpath('//*[@class="msg"]/span[2]/label/text()').extract_first())
        item['look_times']        = tryex.strip(sr.xpath('//*[@class="msg"]/span[4]/label/text()').extract_first())
        item['unit_price'] = sr.xpath('//div[@class="price"]/b/text()').extract_first()
        if item['unit_price'] is None:
            item['unit_price'] = sr.xpath('//div[@class="unitPrice"]/span/text()').extract_first()
        item['crawl_time']        = time.strftime("%Y-%m-%d %X",time.localtime())
        item['residence_url']     = item['url']
        item['url']               = response.url
        item['webst_nm']          = u'链家'
        item['bsn_dt']            = time.strftime("%Y-%m-%d %X",time.localtime())
        item['tms']               = time.strftime("%Y-%m-%d %X",time.localtime())
        yield item