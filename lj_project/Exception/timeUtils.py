# coding:utf-8
from datetime import datetime


def getPriceTime():
    year = datetime.today().year
    month = datetime.today().month
    if month == 1:
        month = 12
        year = int(year)-1
    return str(year) + '/' + str(month)

if __name__=="__main__":
    t = getPriceTime()
    print t