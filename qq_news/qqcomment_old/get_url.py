# -*-coding:utf-8-*-
'''
Created on 2015年9月18日

@author: yx
'''
import pymongo
import time
import datetime
import sys
import chardet
reload(sys)
sys.setdefaultencoding('utf-8')
def get_url():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['qqnews']
    #db.authenticate("root","111111")
    a = 40
    two_day = (datetime.datetime.now() + datetime.timedelta(days=-a)).strftime("%Y-%m-%d %H:%M")
    cursor = db.TitleItem.find({"title_time": {"$gt": two_day}})
    update_time = (datetime.datetime.now() + datetime.timedelta(days=-a)).strftime("%Y-%m-%d %H:%M")
    try:
        f = open('url.txt', 'w')
        for i in cursor:
            f.write(i['title_url'] + '\t' + update_time + '\t' + str(i['num']) + '\n')
        f.close()
    except Exception, e:
        print str(e)
    client.close() 
get_url()