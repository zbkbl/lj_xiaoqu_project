# coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider
from lj_project.items import DealItem
import datetime
from scrapy.selector import Selector
from scrapy import Request
from lj_project.Exception import tryex
import re
import time
import datetime
from lj_project.Exception.emailSender import emailSender

url_dict = {
    'sh.lianjia': "http://sh.lianjia.com", 'su.lianjia':"http://su.lianjia.com"
}


class ShChengjiao(CrawlSpider):
    name = 'lj_sh_chengjiao'
    allowed_domain = [
        'http://sh.lianjia.com',
        'http://su.lianjia.com'
    ]

    start_urls = ["http://sh.lianjia.com/chengjiao",
                  "http://su.lianjia.com/chengjiao"]

    custom_settings = {
            'ITEM_PIPELINES': {
                # 'lj_project.pipelines.ShPipeline': 250,
                'lj_project.pipelines.LjProjectPipeline': 300,
            },
            'DOWNLOADER_MIDDLEWARES': {
            'lj_project.filter_url.LjprojectDealMiddleware': 310,

            },
            'DOWNLOAD_DELAY': 0.2
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.get_district_list, dont_filter=True)

    def get_district_list(self, response):
        """
        获取行政区
        :param response:
        :return:
        """
        select = scrapy.Selector(response)
        domain = self.get_domain(response.url)
        deal_url = select.xpath('//*[@id="plateList"]/div/a/@href').extract()
        chengjiao_list = deal_url[1:]
        for u in chengjiao_list:
            url = domain + u
            yield scrapy.Request(url, callback=self.get_community_list)

    def get_community_list(self, response):
        """
        获取商圈
        :param response:
        :return:
        """
        select = scrapy.Selector(response)
        domain = self.get_domain(response.url)
        deal_url = select.xpath('//*[@id="plateList"]/div[2]/div/a/@href').extract()
        community_list = deal_url[1:]
        for u in community_list:
            url = domain + u
            yield Request(
                url, callback=self.get_url_list
            )

    def get_url_list(self, response):
        """
        获取案例链接
        :param response:
        :return:
        """
        select = scrapy.Selector(response)
        domain = self.get_domain(response.url)
        house_url = select.xpath('//*[@id="js-ershoufangList"]/div[2]/div[4]/div/ul/li/a/@href').extract()
        for u in house_url:
            url = domain + u
            yield Request(url, callback=self.get_deal_info)

        next_page = select.xpath('//*[@id="js-ershoufangList"]/div[2]/div[4]/div/div/a[@gahref="results_next_page"]/@href').extract_first()
        if next_page:
            nextPage = domain + next_page
            yield Request(nextPage, callback=self.get_url_list)


    def get_deal_info(self, response):
        item = DealItem()
        domain = self.get_domain(response.url)
        html = response.body.decode('utf-8','ignore')
        div = re.findall('<table[\s\S]*</table>',html)[0]
        # print html
        # f = open('ceshi.txt','w')
        # f.write(html.encode('utf-8'))
        # f.close()
        sr = Selector(response)
        title = sr.xpath('/html/body/div[4]/div/div[1]/div[1]/div[1]/h1/text()').extract_first()
        title_list = title.split(" ")
        item['structure']         = tryex.strip(title_list[1])
        item['residence_name']    = tryex.strip(title_list[0])
        orientation       = re.findall(u"朝向：</span>(.*?)</td>",div,re.S)
        if orientation:
            item['orientation'] = orientation[0].strip()
        item['area']              = tryex.strip(title_list[2].replace(u"平米",u"㎡"))
        item['inner_area']        = None
        item['heating_style']     = None
        decoration        = re.findall(u"装修：</span>(.*?)</td>",div,re.S)
        if decoration:
            item['decoration'] = decoration[0].strip()

        rec = re.compile(r'\d+')
        floor_string = re.findall(u"楼层：</span>(.*?)</td>",div,re.S)
        if floor_string:
            fs = floor_string[0].split('/')
            item['floor'] = fs[0].strip()
            item['total_floor'] = rec.findall(floor_string[0].strip())[0]
        else:
    		item['floor'] = None
    		item['total_floor'] = None

        item['house_type_struct'] = None
        item['build_type']        = None
        item['build_struct']      = None
        item['household']         = None
        item['elevator']          = None

        item['house_age']         = sr.xpath('//span[@class="taxfree-ex"]/span/text()').extract_first()
        item['property_type']     = None
        item['house_type']        = None
        item['house_owner']       = None
        item['listing_date']      = None
        listing_price     = re.findall(u'<p>(.*?)<span class="unit">万</span></p>',html)
        if listing_price:
            item['listing_price'] = listing_price[0].strip()
        item['total_price']       = None

        transaction_date = re.findall(u'<div class="cell first">(.*?)链家网签约',html,re.S)
        if transaction_date:
             s = transaction_date[0].strip()
             td = re.findall("<p>(.*?)</p>",s)[0]
             item['transaction_date'] = td.replace('.','-').strip()

        else:
            item['transaction_date'] = None

        item['last_deal']         = None
        item['deal_cycle']        = None
        item['look_times']        = None
        unit_price      = re.findall(u"挂牌单价：</span>(.*?)</td>",div,re.S)
        if unit_price:
            up = unit_price[0].split(u'元')
            item['unit_price'] = up[0].strip()
        item['crawl_time']        = time.strftime("%Y-%m-%d %X",time.localtime())

        key_url = re.findall(u'<span class="title">小区：</span>(.*?) target',html, re.S)
        if key_url:
            u = key_url[0].strip()
            r_url = re.findall(r'"(.*?)"',u)[0]
            if r_url:
                item['residence_url'] = domain + r_url

        item['url']               = response.url
        item['webst_nm']          = u'链家'
        item['bsn_dt']            = time.strftime("%Y-%m-%d %X",time.localtime())
        item['tms']               = time.strftime("%Y-%m-%d %X",time.localtime())
        item['residence_id'] = None
        item['city'] = None
        item['district'] = None
        item['community'] = None


        yield item

    @staticmethod
    def close(spider, reason):
        emailSenderClient = emailSender()
        toSendEmailLst = ['542463713@qq.com']
        finishTime = datetime.datetime.now().strftime('%Y-%m-%d %X')
        subject = u"爬虫结束状态汇报"
        body = u"爬虫结束状态汇报：\n\
                爬虫名称：" + spider.name + u"\n\
                结束原因：" + reason + u"\n\
                结束时间：" + finishTime
        emailSenderClient.sendEmail(toSendEmailLst, subject, body)

    def get_domain(self,url):
        for k,v in url_dict.items():
            if k in url:
                return v