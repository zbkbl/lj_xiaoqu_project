# -*- coding: utf-8 -*-
import copy
from lj_project.items import ResidenceInfoItem,ResidencePriceItem
import MySQLdb
import MySQLdb.cursors
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LjProjectPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='3385458', db='test', charset="utf8")
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        asynitem = copy.deepcopy(item)
        if isinstance(item, ResidenceInfoItem):
            self._insert_residence_info(self.cursor, asynitem, spider)
        if isinstance(item, ResidencePriceItem):
            self._insert_residence_price(self.cursor, asynitem, spider)

        return item

    def _insert_residence_info(self, cursor, item, spider):
        try:
            # print cursor
            cursor.execute("insert into t_web_lj_xiaoqu (city,district,community,residence_name,address,\
                           coordinate, build_time,property_price,property_company,developer,total_buildings,total_houses,\
                           bsn_dt,tms,url,webst_nm,crawl_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (item['city'],item['district'],item['community'],item['residence_name'],item['address'],
                            item['coordinate'],item['build_time'],item['property_price'],item['property_company'],
                            item['developer'],item['total_buildings'],item['total_houses'],item['bsn_dt'],
                            item['tms'],item['url'],item['webst_nm'],item['crawl_time']))
            self.conn.commit()
            spider.logger.info("================= data insert successfult !!! =======================")
        except Exception, e:
            print e

    def _insert_residence_price(self, cursor, item, spider):
        try:
            cursor.execute("insert into t_web_lj_xiaoqu_price (city,district, community, name, url, avg_time,\
             avg_price, crawl_time) values(%s,%s,%s,%s,%s,%s,%s,%s)",(item['city'], item['district'], item['community'],\
                                                                      item['name'],item['url'],item['avg_time'],
                                                                      item['avg_price'],item['crawl_time']))
            spider.logger.info("======data insert successfult !!!======")
            self.conn.commit()
        except Exception, e:
            print e