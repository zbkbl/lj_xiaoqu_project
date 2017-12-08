# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ResidencePriceItem(scrapy.Item):
    id = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    community = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    avg_time = scrapy.Field()
    avg_price = scrapy.Field()
    crawl_time = scrapy.Field()
    residence_id = scrapy.Field()


class ResidenceInfoItem(scrapy.Item):
    city = scrapy.Field()
    district = scrapy.Field()
    community = scrapy.Field()
    residence_name = scrapy.Field()
    # 别名
    alias = scrapy.Field()
    address = scrapy.Field()
    # 经纬度
    coordinate = scrapy.Field()
    build_time = scrapy.Field()
    property_price = scrapy.Field()
    property_company = scrapy.Field()
    developer = scrapy.Field()
    total_buildings = scrapy.Field()
    total_houses = scrapy.Field()
    bsn_dt = scrapy.Field()
    tms = scrapy.Field()
    url = scrapy.Field()
    webst_nm = scrapy.Field()
    crawl_time = scrapy.Field()
