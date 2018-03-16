#encoding:utf8
import engine_base 
import re
import urllib2
import urllib

class Baidu(engine_base.Base):
    def __init__(self):
        engine_base.Base.__init__(self)
        self.ready = True
        self.opener = urllib2.build_opener(engine_base.RedirectHandler)
        self.url_change_re = re.compile(r'<a\shref="([\s\S]*?)">',re.S)
        
    def parse(self,page):
        result_list = []
        for t in page.xpath(self.link_xpath):
            title = (''.join(t.xpath('.//text()'))).strip()
            url = t.get('href')
            if url.find(r'http://www.baidu.com/link?url=') != -1:
                resopnse = self.opener.open(url).read()
                url = self.url_change_re.search(resopnse).group(1)
            result_list.append({'title':title,'url':url})
        return result_list

class S360(engine_base.Base):
    def __init__(self):
        engine_base.Base.__init__(self)
        self.ready = True
        self.host = 'http://www.so.com/'
        self.form = 'q'
        self.link_xpath = '//h3[@class!="vrt"]/a'
        self.next_text = '下一页>'

class Soso(engine_base.Base):
    def __init__(self):
        engine_base.Base.__init__(self)
        self.ready = True
        self.host = 'http://www.soso.com/'
        self.form = 'query'
        self.link_xpath = '//h3[@class!="vrt"]/a'
        self.next_text = '下一页>'

class Bing(engine_base.Base):
    def __init__(self):
        engine_base.Base.__init__(self)
        self.ready = True
        self.host = 'http://www.bing.com/'
        self.form = 'q'
        self.link_xpath = '//h3/a'
        self.next_text = '下一页'

class Aol(engine_base.Base):
    def __init__(self):
        engine_base.Base.__init__(self)
        self.ready = True
        self.host = 'http://www.aol.com/'
        self.form = 'q'
        self.link_xpath = '//h3[@class!="abt left" and @class!="abtdynamic left"]/a'
        self.next_text = 'Next'

class Google(engine_base.Base):
    def __init__(self):
        engine_base.Base.__init__(self)
        self.ready = True
        self.host = 'https://www.google.com.hk'
        self.form = 'q'
        self.link_xpath = '//h3[@class="r"]/a'
        self.next_text = '下一页'
        self.url_change_re = re.compile(r'url\?q=(.*?)&',re.S)
        self.waite = 2
        self.max_num = 2
    def parse(self,page):
        result_list =  [{'title' : (''.join(t.xpath('.//text()')).strip()),
                 'url' : t.get('href') }
                 for t in page.xpath(self.link_xpath)]
        for result in result_list:
            #print result['url']
            s = self.url_change_re.search(result['url'])
            if s:
                result['url']=s.group(1)
            else:
                result['url']=self.host + result['url']
        return result_list

class AltaVista(engine_base.Base):
    def __init__(self):
        engine_base.Base.__init__(self)
        self.ready = True
        self.host = 'https://search.yahoo.com'
        self.form = 'p'
        self.link_xpath = '//h3/a'
        self.next_text = 'Next'
        self.waite = 1
        self.max_num = 3
        
    def parse(self,page):
        result_list = []
        for t in page.xpath(self.link_xpath):
            title = (''.join(t.xpath('.//text()'))).strip()
            url = t.get('href')
            s = re.search(r'http[s]*\%3a.*',url)
            if s:
                url = s.group().replace('%3a',':')
            s = re.search(r'/url\?q=(.*?)\&',url)
            if s:
                url = s.group(1)
            if not re.match('http',url):
                url = self.host + url
            result_list.append({'title':title,'url':url})
        return result_list