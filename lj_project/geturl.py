# coding: utf-8
import MySQLdb
import MySQLdb.cursors
from lj_project.items import ResidencePriceItem
from lj_project.items import DealItem, EsfItem


class GetMissionUrl(object):
    def __init__(self):
        self.host = '10.0.8.198'
        self.user = 'dashuju'
        self.password = '8FTeR5dA!'
        self.db = 'crawler'

        self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db, charset='utf8')
        self.cursor = self.conn.cursor()
        self.url_list = []

    def get_lj_urls(self):
        """
        获取小区均价种子
        :return:
        """
        try:
            self.cursor.execute("select id,city,district,community,residence_name,url from t_web_lj_xiaoqu;")
            rs = self.cursor.fetchall()
            for line in rs:
                # print line
                item = ResidencePriceItem()
                item['residence_id'] = line[0]
                item['city'] = line[1]
                item['district'] = line[2]
                item['community'] = line[3]
                item['name'] = line[4]
                item['url'] = line[5]
                self.url_list.append(item)
        except Exception, e:
            print e
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        return self.url_list

    def get_chengjiao_urls(self):
        """
        成交任务种子获取
        :return:
        """
        try:
            self.cursor.execute("select id,city,district,community,residence_name,url from t_web_lj_xiaoqu where id>67439")
            rs = self.cursor.fetchall()
            for line in rs:
                # print line
                item = DealItem()
                item['residence_id'] = line[0]
                item['city'] = line[1]
                item['district'] = line[2]
                item['community'] = line[3]
                item['residence_name'] = line[4]
                item['url'] = line[5]
                self.url_list.append(item)
        except Exception, e:
            print e
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        return self.url_list

    def get_listing_urls(self):
        """
        在售任务种子获取
        :return:
        """
        try:
            self.cursor.execute("select id,city,district,community,residence_name,url from t_web_lj_xiaoqu")
            rs = self.cursor.fetchall()
            for line in rs:
                # print line
                item = EsfItem()
                item['residence_id'] = line[0]
                item['city'] = line[1]
                item['district'] = line[2]
                item['community'] = line[3]
                item['residence_name'] = line[4]
                item['url'] = line[5]
                self.url_list.append(item)
        except Exception, e:
            print e
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        return self.url_list

    def get_listing_sh_urls(self):
        """
        上海，苏州在售任务种子获取
        :return:
        """
        try:
            self.cursor.execute("select id,city,district,community,residence_name,url from t_web_lj_xiaoqu\
                                where city in ('上海','苏州')")
            rs = self.cursor.fetchall()
            for line in rs:
                # print line
                item = EsfItem()
                item['residence_id'] = line[0]
                item['city'] = line[1]
                item['district'] = line[2]
                item['community'] = line[3]
                item['residence_name'] = line[4]
                item['url'] = line[5]
                self.url_list.append(item)
        except Exception, e:
            print e
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        return self.url_list

    def get_lj_deal_urls(self):
        try:
            self.cursor.execute("select url from t_web_lj_deal_copy where unit_price is NULL;")
            rs = self.cursor.fetchall()
            for line in rs:
                self.url_list.append(line[0])
        except Exception, e:
            print e
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        return self.url_list

    def get_crawled_deal_urls(self):
        """
        获取已抓取过的成交链接
        :return:
        """
        try:
            self.cursor.execute("select url from t_web_lj_deal_copy")
            rs = self.cursor.fetchall()
            for line in rs:
                self.url_list.append(line[0])
        except Exception, e:
            print e
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        return self.url_list

    def get_crawled_listing_urls(self):
        """
        获取已抓取过的挂牌连接
        :return:
        """
        try:
            self.cursor.execute("select url from t_web_lj_esf")
            rs = self.cursor.fetchall()
            for line in rs:
                self.url_list.append(line[0])
        except Exception, e:
            print e
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        return self.url_list

    def get_crawled_urls(self):
        try:
            self.cursor.execute("select url from t_web_lj_xiaoqu")
            rs = self.cursor.fetchall()
            for line in rs:
                self.url_list.append(line[0])
        except Exception, e:
            print e
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        return self.url_list

if __name__ == '__main__':
    test = GetMissionUrl()
    test.get_crawled_deal_urls()
    print len(test.url_list)