#encoding:utf8
import urllib2
class Base():
    # 初始化
    def __init__(self):
        self.host = 'http://www.baidu.com/'
        self.form = 'wd'
        self.link_xpath = '//h3/a'
        self.next_text = '下一页>'
        self.ready = False
        self.waite = 0
        self.max_num = 4
        self.sleep_time = 1
        
    def fill_form(self,browser,key):
        browser.select_form(nr=0)
        browser.form[self.form] = key
    
    # 解析出相关讯息
    def parse(self,page):
        return [{'title' : (''.join(t.xpath('.//text()')).strip()),
                 'url' : t.get('href')}
                 for t in page.xpath(self.link_xpath)]
                 
    # 下一条URL
    def next(self,clawer,browser):
        clawer.next_url = browser.find_link(text=self.next_text)
        
class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        return fp
    def http_error_302(self, req, fp, code, msg, headers):
        return fp
    


