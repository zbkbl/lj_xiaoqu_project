# -*- coding: utf-8 -*-

import scrapy
from lj_project.items import ResidenceInfoItem
import datetime
import re

city_dict = {
    'bj': u'北京', 'sh': u'上海', 'xm':u'厦门', 'nj':u'南京', 'cd':u'成都', 'qd':u'青岛',
    'wh': u'武汉', 'jn': u'济南', 'hf': u'合肥','xa': u'西安','gz':u'广州', 'su':u'苏州'
}


class LjXiaoquSpider(scrapy.Spider):
    name = "lj_xiaoqu"
    allowed_domain = [
                      'https://bj.lianjia.com',
                      'https://cd.lianjia.com',
                      'https://jn.lianjia.com',
                      'https://nj.lianjia.com',
                      'https://qd.lianjia.com',
                      'https://sh.lianjia.com',
                      # # 'http://sh.lianjia.com',
                      'https://hf.lianjia.com',
                      'https://wh.lianjia.com',
                      'https://xm.lianjia.com',
                      'https://xa.lianjia.com',
                      'https://gz.lianjia.com',
                      'http://su.lianjia.com'
                      ]

    start_urls = {
        'https://bj.lianjia.com/xiaoqu',
        'https://cd.lianjia.com/xiaoqu',
        'https://jn.lianjia.com/xiaoqu',
        'https://nj.lianjia.com/xiaoqu',
        'https://qd.lianjia.com/xiaoqu',
        'https://hf.lianjia.com/xiaoqu'
        # 'http://sh.lianjia.com/xiaoqu',
        'https://sjz.lianjia.com/xiaoqu',
        'https://wh.lianjia.com/xiaoqu',
        'https://xm.lianjia.com/xiaoqu',
        'https://xa.lianjia.com/xiaoqu'
    }

    # 获取区域链接
    def parse(self, response):
        u = response.url
        URL = u.split(r"/xiaoqu/")[0]
        urls = response.xpath('//div[@class="position"]/dl[2]/dd/div[@data-role="ershoufang"]/div/a/@href').extract()
        for url in urls:
            if "https" not in url:
                new_url = URL + url
                yield scrapy.Request(url=new_url, callback=self.parse_community)

    # 获取小区链接
    def parse_community(self, response):
        item = ResidenceInfoItem()
        select = scrapy.Selector(response)
        li = select.xpath("/html/body/div[4]/div[1]/ul//li")
        for l in li:
            url = l.xpath("a/@href").extract_first()
            item['residence_name'] = l.xpath("div[@class='info']/div/a/text()").extract_first()
            item['district'] = l.xpath("div/div/a[@class='district']/text()").extract_first()
            item['community'] = l.xpath("div/div/a[@class='bizcircle']/text()").extract_first()

            yield scrapy.Request(url, meta={'key': item}, callback=self.parse_residence_info)

        page_box = select.xpath('//div[@class="page-box house-lst-page-box"]').extract_first()
        if page_box is not None:
            totalPage = eval(scrapy.Selector(text=page_box).xpath('//@page-data').extract_first())['totalPage']
            curPage = eval(scrapy.Selector(text=page_box).xpath('//@page-data').extract_first())['curPage']
            if totalPage > curPage:
                yield scrapy.Request(
                    response.url[0:response.url.find('/', 30) + 1] + 'pg' + str(curPage + 1) + '/',
                    callback=self.parse_community
                )

    def parse_residence_info(self, response):
        select = scrapy.Selector(response)
        item = response.meta['key']
        # 小区地址，别名
        name_str = select.xpath('//*[@class="detailDesc"]/text()').extract_first()
        item['address'] = name_str
        # if r'(' in name_str:
        #     address = re.findall(r'\((.*?)\)', name_str)[0]
        #     item['address'] = address
        #     alias = name_str[len(address)+2:]
        #     item['alias'] = alias
        # else:
        #     item['address'] = name_str
        #     item['alias'] = u"无"
        # 小区经纬度
        item['coordinate'] = select.xpath('//*[@class="xiaoquInfoContent"]/span/@xiaoqu').extract_first()
        # 建成时间
        item['build_time'] = select.xpath('//*[@class="xiaoquInfo"]/div[1]/span[2]/text()').extract_first()
        # 物业费
        item['property_price'] = select.xpath('//*[@class="xiaoquInfo"]/div[3]/span[2]/text()').extract_first()
        # 物业公司
        item['property_company'] = select.xpath('//*[@class="xiaoquInfo"]/div[4]/span[2]/text()').extract_first()
        # 开发商
        item['developer'] = select.xpath('//*[@class="xiaoquInfo"]/div[5]/span[2]/text()').extract_first()
        # 楼栋总数
        item['total_buildings'] = select.xpath('//*[@class="xiaoquInfo"]/div[6]/span[2]/text()').extract_first()
        # 总户数
        item['total_houses'] = select.xpath('//*[@class="xiaoquInfo"]/div[7]/span[2]/text()').extract_first()

        # 业务时间
        item['bsn_dt'] = str(datetime.date.today())
        # 抓取时间
        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %X')
        # 入库时间戳
        item['tms'] = datetime.datetime.now().strftime('%Y-%m-%d %X')

        item['webst_nm'] = u'链家'
        # 城市
        for key in city_dict.keys():
            if key in response.url:
                item['city'] = city_dict[key]
        item['url'] = response.url
        yield item