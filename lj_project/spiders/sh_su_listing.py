# coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider
from lj_project.geturl import GetMissionUrl
from scrapy.selector import Selector
from scrapy import Request
from lj_project.Exception import tryex
import re
import time

url_dict = {
    'sh.lianjia': "http://sh.lianjia.com", 'su.lianjia':"http://su.lianjia.com"
}


class ShListing(CrawlSpider):
    name = 'lj_sh_listing'
    allowed_domain = [
        'http://sh.lianjia.com',
        'http://su.lianjia.com'
    ]

    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'lj_project.pipelines.LjProjectPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'lj_project.filter_url.LjprojectListingMiddleware': 310,

        },
        'DOWNLOAD_DELAY': 0.2
    }

    def __init__(self):
        self.geturl = GetMissionUrl()
        self.mission_urls = self.geturl.get_listing_sh_urls()

    def start_requests(self):
        for item in self.mission_urls:
            yield scrapy.Request(item['url'], meta={'key': item},
                                 callback=self.get_deal_url)

    def get_deal_url(self, response):
        select = scrapy.Selector(response)
        domain = self.get_domain(response.url)
        item = response.meta['key']
        deal_url = select.xpath('//*[@id="yz_ershoufang"]/div[1]/a/@href').extract_first()
        if deal_url:
            new_url = domain + deal_url
            yield scrapy.Request(new_url, meta={'key': item}, callback=self.get_esf_url)

    def get_esf_url(self, response):
        item = response.meta['key']
        domain = self.get_domain(response.url)
        select = Selector(response)
        esf_url = select.xpath('//*[@id="js-ershoufangList"]/div[2]/div[3]/div[1]/ul/li/a/@href').extract()
        for url in esf_url:
            new_url = domain + url
            yield Request(
                new_url,
                meta={'key': item},
                callback=self.get_esf_info
            )

        next = select.xpath('//*[@id="js-ershoufangList"]/div[2]/div[3]/div[1]/div[2]/a[@gahref="results_next_page"]/@href').extract_first()
        if next:
            next_page = domain + next
            yield Request(
                next_page, meta={'key':item},
                callback=self.get_esf_url
            )

    def get_esf_info(self, response):
        sr = Selector(response)
        item = response.meta['key']
        html = response.body.decode('utf-8', 'ignore')

        list_ziduan = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[2]/ul/li/span[1]/text()').extract()
        list_neirong = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[2]/ul/li/span[2]/text()').extract()

        details = dict(zip(list_ziduan, list_neirong))
        for k, v in details.items():
            if k == u'房屋户型':
                item['structure'] = v
            elif k == u'配备电梯':
                item['elevator'] = v
            elif k == u'建筑面积':
                item['area'] = v.replace(u'平',u'㎡')
            elif k== u'供暖方式':
                item['heating_style'] = v

        list_title = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[3]/ul/li/span[1]/text()').extract()
        list_desc = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[3]/ul/li/span[2]/text()').extract()
        de = dict(zip(list_title, list_desc))
        for k, v in de.items():
            if k == u'所在楼层':
                item['floor'] = v.split('/')[0]
                item['total_floor'] = re.findall(r'\d+', v)[0]
            elif k == u'装修情况':
                item['decoration'] = v
            elif k == u'房屋朝向':
                item['orientation'] = v.strip()

        item['inner_area']        = None

        item['house_type_struct'] = None

        # 交易属性相关字段
        list_tran = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[2]/div[2]/ul/li/span[1]/text()').extract()
        list_trandesc = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[2]/div[2]/ul/li/span[2]/text()').extract()
        trand = dict(zip(list_tran, list_trandesc))
        for k, v in trand.items():
            if k == u'上次交易':
                item['last_deal'] = v.strip()
            elif k == u'房本年限':
                item['house_age'] = v
            elif k == u'房屋朝向':
                item['orientation'] = v

        #房屋类型
        house_type = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[2]/div[3]/ul/li[2]/span[2]/text()').extract_first()
        item['house_type'] = house_type.strip()
        item['build_type']        = None
        item['build_struct']      = None
        item['household']         = None

        item['ring_num']          = None
        lj_num            = sr.xpath('/html/body/section/div[2]/aside/ul[2]/li[4]/span[2]/text()').extract()
        item['lj_num'] = lj_num[1]
        item['property_type']     = None
        item['house_owner']       = None
        item['listing_date']      = None
        item['total_price']       = sr.xpath('/html/body/section/div[2]/aside/div[1]/div[1]/span[1]/text()').extract_first()
        item['unit_price']        = sr.xpath('/html/body/section/div[2]/aside/div[1]/div[2]/p[1]/span/text()').extract_first()
        item['mortgage']          = None
        item['house_backup']      = None

        item['residence_url']               = item['url']
        item['crawl_time']        = time.strftime("%Y-%m-%d %X",time.localtime())
        item['bsn_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
        item['tms'] = time.strftime("%Y-%m-%d %X", time.localtime())
        item['webst_nm'] = u'链家'

        item['url'] = response.url
        yield item


    def get_domain(self,url):
        for k,v in url_dict.items():
            if k in url:
                return v