# coding: utf-8
import MySQLdb
import MySQLdb.cursors
from lj_project.items import ResidencePriceItem


class GetMissionUrl(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = '3385458'
        self.db = 'test'

        self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db, charset='utf8')
        self.cursor = self.conn.cursor()
        self.url_list = []

    def get_lj_urls(self):
        try:
            self.cursor.execute("select id,city,district,community,residence_name,url from t_web_lj_xiaoqu;")
            rs = self.cursor.fetchall()
            for line in rs:
                # print line
                item = ResidencePriceItem()
                item['id'] = line[0]
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


        # for i in self.url_list:
        #     print i
        # print len(self.url_list)
        return self.url_list

    def get_lj_deal_urls(self):
        try:
            self.cursor.execute("select url from t_web_lj_deal_copy where unit_price is NULL;")
            rs = self.cursor.fetchall()
            for line in rs:
                self.url_list.append(line[0])
        except Exception, e:
            print e
        return self.url_list
        # for i in self.url_list:
        #     print i
        # print len(self.url_list)

    def get_crawled_urls(self):
        try:
            self.cursor.execute("select url from t_web_lj_xiaoqu where city='西安'")
            rs = self.cursor.fetchall()
            for line in rs:
                self.url_list.append(line[0])
        except Exception, e:
            print e
        return self.url_list

if __name__ == '__main__':
    test = GetMissionUrl()
    test.get_crawled_urls()
    print len(test.url_list)