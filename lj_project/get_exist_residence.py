# encoding=utf8
import MySQLdb
import MySQLdb.cursors

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class GetUrls(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = '3385458'
        self.db = 'test'

        self.conn = MySQLdb.connect(host=self.host, user=self.user,
                                    passwd=self.password, db=self.db,
                                    charset="utf8")
        self.cursor = self.conn.cursor()

    def get_lj_residence_urls(self):
        """
        获取已经存在的小区url，用于去重,增加新增小区
        :return:
        """
        url_set = set()
        try:
            self.cursor.execute("select url from t_web_lj_xiaoqu")
            rs = self.cursor.fetchall()
            for line in rs:
                url_set.add(line[0])
        except Exception, e:
            print e
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        return url_set


if __name__=="__main__":
    cls = GetUrls()
    a = cls.get_lj_residence_urls()
    print a