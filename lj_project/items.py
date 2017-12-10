# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ResidencePriceItem(scrapy.Item):
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

class DealItem(scrapy.Item):
    structure = scrapy.Field()
    orientation = scrapy.Field()
    area = scrapy.Field()
    inner_area = scrapy.Field()
    heating_style = scrapy.Field()
    decoration = scrapy.Field()
    floor = scrapy.Field()
    total_floor = scrapy.Field()
    house_type_struct = scrapy.Field()
    build_type = scrapy.Field()
    build_struct = scrapy.Field()
    household = scrapy.Field()
    elevator = scrapy.Field()

    house_age = scrapy.Field()
    property_type = scrapy.Field()
    house_type = scrapy.Field()
    house_owner = scrapy.Field()
    listing_date = scrapy.Field()
    listing_price = scrapy.Field()
    total_price = scrapy.Field()
    transaction_date = scrapy.Field()
    last_deal = scrapy.Field()
    deal_cycle = scrapy.Field()
    look_times = scrapy.Field()

    bsn_dt = scrapy.Field()
    tms = scrapy.Field()
    url = scrapy.Field()
    webst_nm = scrapy.Field()
    crawl_time = scrapy.Field()
    residence_url = scrapy.Field()

    residence_id = scrapy.Field()
    unit_price = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    community = scrapy.Field()
    residence_name = scrapy.Field()


class EsfItem(scrapy.Item):

    structure         = scrapy.Field()
    orientation       = scrapy.Field()
    area              = scrapy.Field()
    inner_area        = scrapy.Field()
    heating_style     = scrapy.Field()
    decoration        = scrapy.Field()
    floor             = scrapy.Field()
    total_floor       = scrapy.Field()
    house_type_struct = scrapy.Field()
    build_type        = scrapy.Field()
    build_struct      = scrapy.Field()
    household         = scrapy.Field()
    elevator          = scrapy.Field()

    ring_num          = scrapy.Field()
    lj_num            = scrapy.Field()

    house_age         = scrapy.Field()
    property_type     = scrapy.Field()
    house_type        = scrapy.Field()
    house_owner       = scrapy.Field()
    listing_date      = scrapy.Field()
    total_price       = scrapy.Field()
    unit_price        = scrapy.Field()
    last_deal         = scrapy.Field()
    mortgage          = scrapy.Field()
    house_backup      = scrapy.Field()

    bsn_dt            = scrapy.Field()
    tms               = scrapy.Field()
    url               = scrapy.Field()
    webst_nm          = scrapy.Field()
    crawl_time        = scrapy.Field()
    residence_url     = scrapy.Field()
    residence_id      = scrapy.Field()
    city              = scrapy.Field()
    district          = scrapy.Field()
    community         = scrapy.Field()
    residence_name    =scrapy.Field()