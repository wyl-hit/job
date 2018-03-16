# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')


class CommentPipeline(object):

    def __init__(self):
        try:
            self.conn = MySQLdb.Connect(
                host='10.10.16.21',
                user='user1',
                passwd='password1',
                db='cluster',
                port=3306
            )
            self.cur = self.conn.cursor()
            self.conn.set_character_set('utf8')
            self.cur.execute('SET NAMES utf8;')
            self.cur.execute('SET CHARACTER SET utf8;')
            self.cur.execute('SET character_set_connection=utf8;')
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def handle_ip(self, ip, source):
        ip = ip.replace("省", "")
        new_ip = ip.replace("市", "")
        if source.find("qq") != -1:
            new_ip = new_ip.replace(":", "")
            new_ip = new_ip.replace("中国", "")
        return new_ip

    def close_spider(self, spider):
        try:
            self.cur.close()
            self.conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return self.urllist

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        try:
            if collection_name == 'TitleItem':
                #self.db[collection_name].update({'_id': item['_id']}, dict(item), upsert = True)
                pass
            elif collection_name == 'CommentItem':
                try:
                self.cur.execute("insert into reply(title,source,comment_id,content,user_id,support_count,ip_location) \
                    values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\") \
                    ON DUPLICATE KEY UPDATE comment_id = \"%s\";" % (

                    None, item['title_id'], item['_id'], item['comments'], item[
                        'user'], 0, "", item['_id']
                ))
                self.conn.commit()
            except MySQLdb.Error, e:
                print [comments['comments']]
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            else:
                self.db['TitleItem'].update({'_id': item['_id']}, {"$set": {'num': item['num']}})
        except Exception, e:
            pass
            #print str(e)
        return item

    def process_item(self, item, spider):

        if 'comments' in item and len(item['comments']) > 1:
            item['ip_location'] = self.handle_ip(
                item['ip_location'], item['title_id'])

            try:
                self.cur.execute("insert into reply(title,source,comment_id,content,user_id,support_count,ip_location) \
                    values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\") \
                    ON DUPLICATE KEY UPDATE content = \"%s\";" % (

                    item['title'], item['title_id'], item['comment_id'], item['comments'], item[
                        'user_id'], item['support_count'], item['ip_location'], item['comments']
                ))
                self.conn.commit()
            except MySQLdb.Error, e:
                print [comments['comments']]
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        elif 'urllist' in item:
            try:
                f = open('url_item', 'a')
                for i in item['urllist']:
                    f.write(i + '\n')
                f.close()
            except Exception, e:
                print str(e)
            self.urllist += item['urllist']
        else:
            try:
                # self.cur.execute(
                  #  "insert into bbs_title(id,title) values(\"%s\",\"%s\") \
                  #  ON DUPLICATE KEY UPDATE title=\"%s\";" % (
                  #      item['title_id'],
                  #      item['title_content'],
                  #      item['title_content']
                  #  )
               # )
                # self.conn.commit()
                return '2333'
            except MySQLdb.Error, e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
