# -*- coding: utf-8 -*-
import copy
from lj_project.items import ResidenceInfoItem,ResidencePriceItem,DealItem,EsfItem
import MySQLdb
import MySQLdb.cursors
from lj_project.Exception.readUtils import MysqlConfig
import datetime
from lj_project.Exception.emailSender import emailSender
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LjProjectPipeline(object):

    def __init__(self):
        mysqlConfig = MysqlConfig.getMysqlConfig()
        self.host = mysqlConfig['host']
        self.user = mysqlConfig['user']
        self.password = mysqlConfig['password']
        self.db = mysqlConfig['db']

        self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db, charset='utf8')
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
        if isinstance(item, DealItem):
            self._insert_deal_item(self.cursor, asynitem, spider)
        if isinstance(item, EsfItem):
            self._insert_listing_item(self.cursor, asynitem, spider)

        return item

    def _insert_residence_info(self, cursor, item, spider):
        """
        插入小区信息
        :param cursor:
        :param item:
        :param spider:
        :return:
        """
        try:
            # print cursor
            cursor.execute("insert into t_web_lj_xiaoqu (city,district,community,residence_name,address,\
                          coordinate,build_time,property_price,property_company,developer,total_buildings,\
                          total_houses,bsn_dt,tms,url,webst_nm,crawl_time) values\
                            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (item['city'],item['district'],item['community'],item['residence_name'],item['address'],
                            item['coordinate'],item['build_time'],item['property_price'],item['property_company'],
                            item['developer'],item['total_buildings'],item['total_houses'],item['bsn_dt'],
                            item['tms'],item['url'],item['webst_nm'],item['crawl_time']))
            self.conn.commit()
            spider.logger.info("================= data insert successful !!! =======================")
        except Exception, e:
            spider.logger.error(e)
            emailSenderClient = emailSender()
            toSendEmailLst = ['542463713@qq.com']
            finishTime = datetime.datetime.now().strftime('%Y-%m-%d %X')
            subject = u"爬虫异常状态汇报"
            body = u"爬虫异常状态汇报：\n\
                        爬虫名称：" + spider.name + u"\n\
                        异常信息：" + e.message + u"\n\
                        异常发生时间：" + finishTime
            emailSenderClient.sendEmail(toSendEmailLst, subject, body)

    def _insert_residence_price(self, cursor, item, spider):
        """
        插入小区均价
        :param cursor:
        :param item:
        :param spider:
        :return:
        """
        try:

            cursor.execute("insert into t_web_lj_xiaoqu_price (city,district, community, name, url, avg_time,\
             avg_price, crawl_time,residence_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(item['city'], item['district'], item['community'],\
                                                                      item['name'],item['url'],item['avg_time'],
                                                                      item['avg_price'],item['crawl_time'],int(item['residence_id'])))
            spider.logger.info("======data insert successful !!!======")
            self.conn.commit()
        except Exception, e:
            spider.logger.error(e)

    def _insert_deal_item(self, cursor, item, spider):
        """
        插入成交房源
        :param cursor:
        :param item:
        :param spider:
        :return:
        """
        try:
            cursor.execute("insert into t_web_lj_deal_copy (structure,orientation,area,inner_area,heating_style,\
                                       decoration, floor,total_floor,house_type_struct,build_type,build_struct,household,\
                                       elevator,house_age,property_type,house_type,house_owner,listing_price,listing_date,\
                                       total_price,transaction_date,last_deal,deal_cycle,look_times,bsn_dt,tms,url,webst_nm,\
                                       crawl_time,residence_url,residence_id,unit_price,city,district,community,residence_name\
                                       ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (item['structure'], item['orientation'], item['area'], item['inner_area'], item['heating_style'],
                            item['decoration'], item['floor'], item['total_floor'], item['house_type_struct'],
                            item['build_type'], item['build_struct'], item['household'], item['elevator'],
                            item['house_age'], item['property_type'], item['house_type'], item['house_owner'],
                            item['listing_price'],item['listing_date'],item['total_price'],item['transaction_date'],
                            item['last_deal'],item['deal_cycle'],item['look_times'],item['bsn_dt'],item['tms'],
                            item['url'],item['webst_nm'],item['crawl_time'],item['residence_url'],item['residence_id'],
                            item['unit_price'],item['city'],item['district'],item['community'],item['residence_name']))
            self.conn.commit()
            spider.logger.info("================= data insert successful !!! =======================")
        except Exception, e:
            spider.logger.error(e)
            spider.logger.error(e)
            emailSenderClient = emailSender()
            toSendEmailLst = ['542463713@qq.com']
            finishTime = datetime.datetime.now().strftime('%Y-%m-%d %X')
            subject = u"爬虫异常状态汇报"
            body = u"爬虫异常状态汇报：\n\
                                    爬虫名称：" + spider.name + u"\n\
                                    异常信息：" + e.message + u"\n\
                                    异常发生时间：" + finishTime
            emailSenderClient.sendEmail(toSendEmailLst, subject, body)

    def _insert_listing_item(self, cursor, item, spider):
        """
        插入在售房源
        :param cursor:
        :param item:
        :param spider:
        :return:
        """
        try:
            cursor.execute("insert into t_web_lj_esf (structure,orientation,area,inner_area,heating_style,\
                                       decoration, floor,total_floor,house_type_struct,build_type,build_struct,household,\
                                       elevator,ring_num,lj_num,house_age,property_type,house_type,house_owner,\
                                       listing_date,total_price,unit_price,last_deal,mortgage,house_backup,bsn_dt,tms,url,\
                                       webst_nm,crawl_time,residence_url,residence_id,city,district,community,residence_name\
                                       ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (item['structure'], item['orientation'], item['area'], item['inner_area'], item['heating_style'],
                            item['decoration'], item['floor'], item['total_floor'], item['house_type_struct'],
                            item['build_type'], item['build_struct'], item['household'], item['elevator'],
                            item['ring_num'], item['lj_num'], item['house_age'], item['property_type'],
                            item['house_type'],item['house_owner'],item['listing_date'],item['total_price'],
                            item['unit_price'],item['last_deal'],item['mortgage'],item['house_backup'],item['bsn_dt'],
                            item['tms'],item['url'],item['webst_nm'],item['crawl_time'],item['residence_url'],item['residence_id'],
                            item['city'],item['district'],item['community'],item['residence_name']))
            self.conn.commit()
            spider.logger.info("================= data insert successful !!! =======================")
        except Exception, e:
            spider.logger.error(e)
            spider.logger.error(e)
            emailSenderClient = emailSender()
            toSendEmailLst = ['542463713@qq.com']
            finishTime = datetime.datetime.now().strftime('%Y-%m-%d %X')
            subject = u"爬虫异常状态汇报"
            body = u"爬虫异常状态汇报：\n\
                                    爬虫名称：" + spider.name + u"\n\
                                    异常信息：" + e.message + u"\n\
                                    异常发生时间：" + finishTime
            emailSenderClient.sendEmail(toSendEmailLst, subject, body)


class ShPipeline(object):

    def __init__(self):
        mysqlConfig = MysqlConfig.getMysqlConfig()
        self.host = mysqlConfig['host']
        self.user = mysqlConfig['user']
        self.password = mysqlConfig['password']
        self.db = mysqlConfig['db']

        self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db, charset='utf8')
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        self._query_sh_chengjiao_item(self.cursor, item, spider)

    def _query_sh_chengjiao_item(self, cursor, item, spider):
        try:
            cursor.execute("select id,city,district,community,residence_name from t_web_lj_xiaoqu where url=%s " % item['residence_url'])
            rs = self.cursor.fetchall()
            print rs
            for line in rs:
                item['residence_id'] = line[0]
                item['city'] = line[1]
                item['district'] = line[2]
                item['community'] = line[3]
                item['residence_name'] = line[4]
                spider.logger.info("================ insert residence info successful ================")
                yield item
        except Exception, e:
            spider.logger.error(e)
            spider.logger.error(e)
            emailSenderClient = emailSender()
            toSendEmailLst = ['542463713@qq.com']
            finishTime = datetime.datetime.now().strftime('%Y-%m-%d %X')
            subject = u"爬虫异常状态汇报"
            body = u"爬虫异常状态汇报：\n\
                                    爬虫名称：" + spider.name + u"\n\
                                    异常信息：" + e.message + u"\n\
                                    异常发生时间：" + finishTime
            emailSenderClient.sendEmail(toSendEmailLst, subject, body,spider)
