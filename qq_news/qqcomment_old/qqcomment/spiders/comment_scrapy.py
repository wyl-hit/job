# -*-coding:utf-8-*-
'''
Created on 2015年8月29日

@author: wyl
'''
import scrapy
import re
import urllib
import time
from qqcomment.items import CommentItem
from qqcomment.items import TitleItem
from qqcomment.items import UpdateItem
import chardet
import logging
import requests 
from random import choice
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

class get_comment(scrapy.Spider):
    name = "comment_scrapy"

    def __init__(self):
        self.start_urls = ['http://www.qq.com/', 'http://news.qq.com/']
        self.before_list = {}
        self.user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]

    def parse(self, response):
        try:
            f = open('url.txt', 'r')
            for i in f.readlines():
                url_info = i.strip().split('\t')
                logging.info('get old ' + url_info[0]) 
                self.before_list[url_info[0]] = None
                request = scrapy.Request(url_info[0], callback=self.comment_qq)
                request.meta['update_time'] = url_info[1]
                request.meta['comment_num'] = url_info[2]
                yield request
            f.close()
            f = open('url.txt', 'w')
            f.write('')
            f.close()
        except Exception, e:
            print str(e)
        # parse and get index page news url
        '''if response.url == 'http://www.qq.com/':
                                    try:
                                        url_list = []
                                        url_list = response.xpath('//div[@class="txtArea"]/h3/a/@href  | //div[@class="contentLeft"]/ul/li/a/@href | //div[contains(@class, "contentRight")]/ul/li/a/@href').extract()
                                        url_list += response.xpath('//*[contains(@id, "newsContent")]/ul/li/a/@href | //*[contains(@id, "newsContent")]/div/h3/a/@href').extract()
                                        url_list += response.xpath('//div[@class="ft"]/ul/li/a/@href | //div[@class="ft"]/h3/a/@href ').extract()
                                    except Exception, e:
                                        logging.debug(str(e)) 
                                    for i in url_list: 
                                        target_url = i
                                        if i not in self.before_list:
                                            if i.find("http") == -1:
                                                target_url = 'http:' + i
                                            if target_url.find('v.qq.com') != -1 or target_url.find('le.qq.com') != -1 or target_url.find('kid.qq.com') != -1 or  target_url.find('class.qq.com') != -1 or  target_url.find('dajia.qq.com') != -1 or  target_url.find('chuangshi.qq.com') != -1:
                                                continue
                                            logging.info(target_url)
                                            request = scrapy.Request(target_url, callback=self.comment_qq)
                                            request.meta['update_time'] = None
                                            request.meta['comment_num'] = None
                                            yield request
                                elif response.url == 'http://news.qq.com/':
                                    try:
                                        url_list = []
                                        url_list = response.xpath('//div[@class="slist"]//li/a/@href').extract()
                                        url_list += response.xpath('//div[contains(@class, "pList")]/div/div//h3/a/@href | //div[contains(@class, "pList")]/div//em/a/@href').extract()
                                    except Exception, e:
                                        logging.debug(str(e)) 
                                    for i in url_list: 
                                        target_url = i
                                        if i not in self.before_list:
                                            if i.find("http") == -1:
                                                target_url = 'http:' + i
                                            if target_url.find('v.qq.com') != -1:
                                                continue
                                            logging.info(target_url)
                                            request = scrapy.Request(target_url, callback=self.comment_qq)
                                            request.meta['update_time'] = None
                                            request.meta['comment_num'] = None
                                            yield request
                                    # parse and get block list page url
                                    try:
                                        block_url_list = []
                                        tmp1 = response.xpath('//ul[@id="siteNavPart1"]/li/a/@href').extract()
                                        #tmp2 = response.xpath('//ul[@id="siteNavPart2"]/li/a/@href').extract()
                                        tmp3 = response.xpath('//ul[@id="channelNavPart"]/li/a/@href').extract()
                                        block_url_list = tmp1[2:] 
                                        block_url_list.append(tmp3[2])  # http://news.qq.com/world_index.shtml
                                        block_url_list.append(tmp3[3])  #http://society.qq.com/
                                        block_url_list.append(tmp3[6])  #http://mil.qq.com/mil_index.htm
                                    except Exception, e:
                                        logging.debug(str(e)) 
                                    for block_url in block_url_list: 
                                        target_url = block_url
                                        if target_url.find('v.qq.com') != -1:
                                                continue
                                        if block_url.find("http") == -1:
                                            target_url = 'http:' + block_url
                                        request = scrapy.Request(target_url, callback=self.get_block_list)
                                        yield request'''
                        


    def get_block_list(self, response):
        url_list = []
        try:
            url_list = response.xpath('//div[contains(@class, "pList")]/div/div//h3/a/@href | //div[contains(@class, "pList")]/div/div/em/a/@href').extract()
        except Exception, e:
            logging.debug(str(e)) 
        for url in url_list:
            target_url = url
            if url not in self.before_list:
                if target_url.find('v.qq.com') != -1 or target_url.find('le.qq.com') != -1 or target_url.find('kid.qq.com') != -1 or  target_url.find('class.qq.com') != -1 or  target_url.find('dajia.qq.com') != -1 or  target_url.find('chuangshi.qq.com') != -1:
                        continue
                if url.find("http:") == -1:
                        target_url = 'http:' + url
                request = scrapy.Request(target_url, callback=self.comment_qq)
                request.meta['update_time'] = None
                request.meta['comment_num'] = None
                yield request

    # qq
    def comment_qq(self, response):
        web_url = response.url
        if response.url.find('notfound') != -1:
            tmp = response.url.split('uri=')
            if len(tmp) > 1:
                web_url = tmp[1]
            logging.info("-" *20 + response.url)
        #http://kuaibao.qq.com/s/20171208A0FBGI00
        #http://new.qq.com/omn/20171205C0ZFKR00 20171206A0H7O000  20171206A0DRT5
        if response.url.find('omn') != -1 or response.url.find('kuaibao.qq.com') != -1:
            news_id = response.url.split('/')[-1].split('.')[0]
            if len(news_id) <16:
                news_id += '0'*(16-len(news_id))
            ajax_url = 'http://openapi.inews.qq.com/getQQNewsNormalContent?id=' + news_id +'&chlid=news_rss&refer=mobilewwwqqcom&otype=jsonp&callback=getNewsContentOnlyOutput'
            headers = {'user-agent': choice(self.user_agent_list)}
            news_data = requests.get(ajax_url, headers=headers)
            pubtime = re.findall(r'pubtime":"(.*?[^"])"', news_data.text, re.S)
            created_time = ''
            cmt_id = ''
            title_id = ''
            num = 0
            if pubtime:
                created_time = pubtime[0]
            if response.meta['update_time']:
                update_time = response.meta['update_time']
            else:
                update_time = created_time    
            cid = re.findall(r'cid":"(\d*?)",', news_data.text, re.S) 
            if cid:
                cmt_id = cid[0]
                title_id = cmt_id
                if not response.meta['update_time']:
                    url = 'http://coral.qq.com/article/' + cmt_id +'/comment?commentid=0&reqnum=10&tag=&callback=mainComment'
                    request = scrapy.Request(url, callback=self.commentitem_qq)
                    request.meta['title_id'] = title_id
                    request.meta['update_time'] = update_time
                    yield request
            try:
                title = ''.join(re.findall(r'title":"(.*?[^"])"', news_data.text, re.S)).decode('unicode_escape')
                text_p = ''.join(re.findall(r'value":"(.*?[^"])"', news_data.text, re.S)).decode('unicode_escape')
            except UnicodeDecodeError, e:
                title = ''.join(re.findall(r'title":"(.*?[^"])"', news_data.text, re.S))
                text_p = ''.join(re.findall(r'value":"(.*?[^"])"', news_data.text, re.S))
            ajax_url = 'http://coral.qq.com/article/batchcommentnum?targetid=' + cmt_id + '&callback=_cbSum&_=' + str(long(time.time()))
            headers = {'user-agent': choice(self.user_agent_list)}
            r = requests.get(ajax_url, headers=headers)
            comment_num = re.findall(r'commentnum":"(\d*?)"' ,r.text, re.S)
            if comment_num:
                num = comment_num[0]
                if response.meta['update_time'] and response.meta['comment_num']:
                    if int(response.meta['comment_num']) +5 < int(num):
                        url = 'http://coral.qq.com/article/' + cmt_id +'/comment?commentid=0&reqnum=10&tag=&callback=mainComment'
                        request = scrapy.Request(url, callback=self.commentitem_qq)
                        request.meta['title_id'] = title_id
                        request.meta['update_time'] = update_time
                        yield request
                    else:
                        logging.info('+'*20 + response.url)
            else:
                logging.info("++++++++++" + title  + created_time + title_id + response.url)
                return

        # update_time 没有的话用文章时间
        else:
            created_time = response.xpath('//span[@class="a_time"]/text() | //span[@class="article-time"]/text()' ).extract_first()
            if created_time == None:
                pubtime = re.findall(r'pubtime:(.*?[^,]),', response.body, re.S)
                if pubtime:
                    pubtime_s = pubtime[0].decode(chardet.detect(pubtime[0])['encoding']).encode('utf-8')
                    created_time = pubtime_s.replace(u'年' ,'-').replace(u'月' ,'-').replace(u'日' ,' ')
                else:
                    logging.info('**********' + response.url)
                    return
            if response.meta['update_time']:
                update_time = response.meta['update_time']
            else:
                update_time = created_time
            # 获得文章id
            listp = re.findall(r'cmt_id\s*?=\s*?(\d*?);', response.body, re.S)
            # http://tech.qq.com/a/20171205/025754.htm#p=6
            if len(listp) == 0:
                listp = re.findall(r'aid\s*?:\s*?"(\d*?)",', response.body, re.S)
            cmt_id = listp[0]
            title_id = cmt_id
            if not response.meta['update_time']:
                url = 'http://coral.qq.com/article/' + cmt_id +'/comment?commentid=0&reqnum=10&tag=&callback=mainComment'
                request = scrapy.Request(url, callback=self.commentitem_qq)
                request.meta['title_id'] = title_id
                request.meta['update_time'] = update_time
                yield request
            # 获得文章详细信息
            if response.xpath('//div[@class="qq_article"]/div[1]/h1/text() | //div[@class="LEFT"]/h1/text()').extract_first():
                title = response.xpath('//div[@class="qq_article"]/div[1]/h1/text() | //div[@class="LEFT"]/h1/text() | //*[@id="C-Main-Article-QQ"]/div[1]/h1/text()').extract_first().strip()
            else:
                if response.xpath('//p[@class="title"]/text()').extract_first():
                    title = response.xpath('//p[@class="title"]/text()').extract_first().strip()
                else:
                    title = response.xpath('//title/text()').extract_first().strip() 
            text_list = response.xpath('//*[@id="Cnt-Main-Article-QQ"]/p/text()').extract()
            #http://tech.qq.com/a/20171205/025754.htm#p=5 
            num = response.xpath('//*[@id="cmtNum"]/text() | //*[@id="endShareBtn-cmt-num"]/text()').extract_first()
            if num==0 or num==u'0' or num == None:
                payload = {'targetid':cmt_id, 'callback': '_cbSum', '_': str(long(time.time()))}
                ajax_url = 'http://coral.qq.com/article/batchcommentnum?targetid=' + cmt_id + '&callback=_cbSum&_=' + str(long(time.time()))
                headers = {'user-agent': choice(self.user_agent_list)}
                r = requests.get(ajax_url, headers=headers)
                comment_num = re.findall(r'commentnum":"(\d*?)"' ,r.text, re.S)
                if comment_num:
                    num = comment_num[0]
            if response.meta['comment_num']:       
                if int(response.meta['comment_num'])  < int(num):
                    print '***' + response.meta['comment_num'] + '***' + num
                    url = 'http://coral.qq.com/article/' + cmt_id +'/comment?commentid=0&reqnum=10&tag=&callback=mainComment'
                    request = scrapy.Request(url, callback=self.commentitem_qq)
                    request.meta['title_id'] = title_id
                    request.meta['update_time'] = update_time
                    yield request
            else:
                logging.info('+'*20 + response.url)
            text_p = ''
            for i in text_list:
                text_p += i
        titleitem = TitleItem()
        titleitem['_id'] = title_id
        titleitem['title_content'] = title
        titleitem['title_url'] = web_url
        titleitem['title_time'] = created_time
        titleitem['title_text'] = text_p
        titleitem['update_time'] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        titleitem['num'] = num
        yield titleitem  
        
        
    def commentitem_qq(self, response):
        import json 
        update_time = response.meta['update_time']
        title_id = response.meta['title_id']
        json_c = json.loads(
            re.findall(r'mainComment\((.*)\)', response.body, re.S)[0]
        )
        commentid = json_c['data']['last']
        if not commentid:
            return 
        url = 'http://coral.qq.com/article/' + title_id +\
            '/comment?commentid=' + commentid +\
            '&reqnum=10&tag=&callback=mainComment' 
        for each_item in json_c['data']['commentid']:
            comments = CommentItem()
            comments['_id'] = each_item['id']
            comments['title_id'] = title_id
            comments['comments'] = each_item['content']
            comments['time'] = time.strftime("%Y-%m-%d %H:%M", time.localtime(each_item['time']))
            if comments['time'] <= update_time:
                updataitem = UpdateItem()
                updataitem['_id'] = title_id
                updataitem['num'] = json_c['data']['total']
                yield updataitem
                print 'update ' + title_id + ' ' + str(updataitem['num'])
                return
            comments['user'] = each_item['userid']
            if cmp(each_item['parent'], '0') == 0:
                comments['pid'] = None
            else:
                comments['pid'] = each_item['parent']
            yield comments
        if json_c['data']['hasnext']:
            request = scrapy.Request(url, callback=self.commentitem_qq)
            request.meta['title_id'] = title_id
            request.meta['update_time'] = update_time
            yield request 
        else:
            updataitem = UpdateItem()
            updataitem['_id'] = title_id
            updataitem['num'] = json_c['data']['total']
            yield updataitem
            print 'get ' + title_id + ' ' + str(updataitem['num'])
            return
