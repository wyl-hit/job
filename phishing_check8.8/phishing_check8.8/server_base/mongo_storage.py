# -*- coding: utf-8 -*-

'''数据库collection定义'''

from errors import DependencyNotInstalledError

try:
    from mongoengine import Document, EmbeddedDocument, \
        StringField, DateTimeField, EmailField, \
        BooleanField, URLField, IntField, FloatField, \
        ListField, EmbeddedDocumentField, DictField, \
        ObjectIdField
except ImportError:
    raise DependencyNotInstalledError('mongoengine')


class GrayList(Document):  # 灰名单列表
    gray_name = StringField()  # 灰名单名称
    gray_type = StringField()  # 类型：‘手动’，‘域名探测’，‘关键字探测‘
    creat_time = StringField()  # 生成时间
    update_time = StringField()  # 更新时间
    usr_id = IntField()  # 用户ID
    task_id = IntField()  # 任务ID
    url_num = IntField()  # 灰名单中URL数量
    use_count = IntField()  # 使用次数
    gray_list = ListField(StringField())  # URL列表
    child_gray = ListField(ObjectIdField())  # 该灰名单对应所有子名单objectID列表


class OnceChanged(EmbeddedDocument):  # 每次变换后存在的域名结果
    changed_time = StringField()  # 探测时间，格式化字符串
    task_id = IntField()
    host_rule_list = ListField(StringField())
    top_rule_list = ListField(StringField())
    path_rule_list = ListField(StringField())
    all_changed_num = IntField()  # 该被保护网站域名变换的所有域名数量
    exist_changed_num = IntField()  # 该被保护网站域名变换存在的域名数量
    exist_changed_list = ListField(StringField())  # 存在的变换后域名列表
    gray_ID = StringField()  # pathed exist url


class DomainChange(Document):  # 每个被保护网站的域名变换结果
    protected_url = StringField()  # 被保护网站
    # all_changed_list = ListField(StringField()) #所有变换后域名列表
    exist_changed_list = ListField(StringField())  # 该被保护网站域名变换存在的域名数量
    exist_changed_num = IntField()  # 该被保护网站域名变换存在的域名数量
    # 每次探测存在的域名分别按日期存储
    exist_note = ListField(EmbeddedDocumentField(OnceChanged))


class WebTitle(EmbeddedDocument):  # 保存网页随时间变化的信息
    update_time = StringField()  # 更新时间，格式化字符串
    title = StringField()


class WebText(EmbeddedDocument):  # 保存网页随时间变化的信息 or kword
    update_time = StringField()  # 更新时间，格式化字符串
    text = StringField()
    text_hash = StringField()


class DomNode(EmbeddedDocument):  # 网页dom树的一个结点
    num = IntField()  # 编号
    top = IntField()  # 顶部坐标
    left = IntField()  # 左部坐标
    height = IntField()  # 高度
    width = IntField()  # 宽度


class DomTree(EmbeddedDocument):  # 保存网页dom树
    update_time = StringField()  # 更新时间，格式化字符串
    dom_nodes = ListField(EmbeddedDocumentField(DomNode))
    tree_hash = StringField()


class ChildImage(EmbeddedDocument):  # child image feature, may null
    border_coordinate = ListField(IntField())  # 图片边界坐标
    core_coordinate = ListField(IntField())  # 子图像重心坐标
    core_distance = FloatField()  # 分块重心与整幅图像重心间的距离
    core_angle = FloatField()  # 子图重心相对整幅图像顶点的夹角
    core_ratio = FloatField()  # 分块重心与整幅图像重心间的距离与重心间距离相对对角线的比例
    info_entropy = FloatField()  # 子图信息熵特征
    eccentricity = FloatField()  # 子图像的偏心率
    rotundity_nature = FloatField()  # 子图像的圆形性
    invariant_matrix = ListField(FloatField())  # Hu不变矩组 (7元)


class Image(EmbeddedDocument):  # image infomation
    image_type = IntField()  # 图片类型: 0/1/2
    # 图片名 D:/web/wamp/www/white/white_foreign/americanexpress/506tmp.jpeg
    image_name = StringField()
    image_dct = StringField()  # DCT摘要量化(模糊哈希)
    image_site = StringField()  # 图片位置
    child_image = ListField(EmbeddedDocumentField(ChildImage))  # 图片特征 may null


class WebViewFeature(EmbeddedDocument):  # view compare extracting feature
    update_time = StringField()  # 更新时间，格式化字符串
    view_hash = StringField()  # image_list hash value
    image_list = ListField(EmbeddedDocumentField(Image))


class WebBorder(EmbeddedDocument):  # save web width and high
    update_time = StringField()  # 更新时间，格式化字符串
    width = IntField()
    high = IntField()


class GrayWebSave(Document):  # 保存Gray网页信息，变化的信息存在WebInfo中
    web_url = StringField()
    web_title_list = ListField(EmbeddedDocumentField(WebTitle))
    web_text_list = ListField(EmbeddedDocumentField(WebText))
    web_tree_list = ListField(EmbeddedDocumentField(DomTree))
    web_view_list = ListField(EmbeddedDocumentField(WebViewFeature))
    web_border_list = ListField(EmbeddedDocumentField(WebBorder))


class ProtectedWebSave(Document):  # 保存Protected网页信息，变化的信息存在WebInfo中
    web_url = StringField()
    web_title_list = ListField(EmbeddedDocumentField(WebTitle))
    web_text_list = ListField(EmbeddedDocumentField(WebText))
    web_tree_list = ListField(EmbeddedDocumentField(DomTree))
    web_view_list = ListField(EmbeddedDocumentField(WebViewFeature))
    web_border_list = ListField(EmbeddedDocumentField(WebBorder))


class CounterfeitWebSave(Document):  # 保存Phishing网页信息，变化的信息存在WebInfo中
    web_url = StringField()
    web_title_list = ListField(EmbeddedDocumentField(WebTitle))
    web_text_list = ListField(EmbeddedDocumentField(WebText))
    web_tree_list = ListField(EmbeddedDocumentField(DomTree))
    web_view_list = ListField(EmbeddedDocumentField(WebViewFeature))
    web_border_list = ListField(EmbeddedDocumentField(WebBorder))

class MonitorWebSave(Document):  # 保存Phishing网页信息，变化的信息存在WebInfo中
    web_url = StringField()
    web_title_list = ListField(EmbeddedDocumentField(WebTitle))
    web_text_list = ListField(EmbeddedDocumentField(WebText))
    web_tree_list = ListField(EmbeddedDocumentField(DomTree))
    web_view_list = ListField(EmbeddedDocumentField(WebViewFeature))
    web_border_list = ListField(EmbeddedDocumentField(WebBorder))