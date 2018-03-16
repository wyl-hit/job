#-*- coding:utf-8 -*-
import sys
import time
from PyQt4 import QtGui, QtCore, QtWebKit


class PageShot(QtGui.QWidget):

    def __init__(self, url_save_path_list, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.url_save_path_list = url_save_path_list
        self.url_save_path = ''

    def shot(self):
        webView = QtWebKit.QWebView(self)
        try:
            self.url_save_path = self.url_save_path_list.pop()
        except IndexError:
            self.close()
        webView.load(QtCore.QUrl(self.url_save_path))
        self.webPage = webView.page()
        self.connect(
            webView, QtCore.SIGNAL("loadFinished(bool)"), self.savePage)

    def savePage(self, finished):
        if finished:
            size = self.webPage.mainFrame().contentsSize()
            self.webPage.setViewportSize(
                QtCore.QSize(size.width() + 16, size.height()))
            img = QtGui.QImage(size, QtGui.QImage.Format_ARGB32)
            painter = QtGui.QPainter(img)
            self.webPage.mainFrame().render(painter)
            painter.end()
            fileName = self.url_save_path[
                :self.url_save_path.rfind('/')] + '/pageblock.jpeg'
            if not img.save(fileName):
                sys.stderr.write('%s  PageShot error to save img: %s\n' %
                                 (time.ctime(), self.url_save_path))
        else:
            sys.stderr.write('%s  PageShot error to load html: %s\n' %
                             (time.ctime(), self.url_save_path))
        self.shot()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # shotter = PageShotter("http://www.adssfwewfdsfdsf.com")
    url_list = [
        '/home/zxy/phishing_check/web_info/protected_web/www.sina.com/7bad3943/70e8a5ca/7072eca3/f8a07b74/2015-06-27 14:55/block.html',
        '/home/zxy/phishing_check/web_info/protected_web/www.sina.cn/7f6048b9/92ceed72/6db719aa/798c6b5f/2015-05-24 17_03/block.html']
    shotter = PageShot(url_list)
    shotter.shot()
    sys.exit(app.exec_())

insert into web_feature(title,url,feature,blockpage,webpage,kword,add_time) values('PayPal: Achetez, envoyez de l\'argent et acceptez les paiements','http://kafconstructions.com/wp-includes/SimplePie/XML/Declaration/auth/cmd=_login-run&dispatch=5885d80a13c0db1f998ca05/4efbdf2c29878a435fe324eec2511727fbf3e9efc15215e3628a3e/','','/web_info/counterfeit_web/kafconstructions.com/40dbc186/74722c15/235bc924/bcc4f5fe/2015-07-10 16_27/blockpage.jpeg','/web_info/counterfeit_web/kafconstructions.com/40dbc186/74722c15/235bc924/bcc4f5fe/2015-07-10 16_27/webpage.jpeg','Rechercher/Contact/argent/Aide/Adresseemail/Ouvriruncompte/Accepterdespaiements/Envoyezdel/Payerenligne/PayersureBay/Motdepasse/Vousavezoublivotremotdepasse/Professionnels/PayPal/Seeallcountries/Demanderdel/Ensavoirplus/AvecPayPal/Gratuitpourvous/Entreproches','2015-07-15 19:37')
