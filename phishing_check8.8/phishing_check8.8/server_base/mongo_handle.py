# -*- coding: utf-8 -*-
'''
mongo操作
create time:2015.4.17

author: xinyi
'''

import sys
import time
import traceback
from errors import DependencyNotInstalledError, MongoError
from extra_opration import hash_md5
try:
    from mongoengine import connect, DoesNotExist, ValidationError, errors
except ImportError:
    raise DependencyNotInstalledError('mongoengine')
try:
    from mongo_storage import GrayList, DomainChange, OnceChanged, \
        DomTree, ProtectedWebSave, GrayWebSave, CounterfeitWebSave, \
        DomNode, WebText, WebTitle, WebViewFeature, Image, \
        ChildImage, WebBorder, MonitorWebSave
except ImportError:
    raise DependencyNotInstalledError('mongo_storage')

reload(sys)
sys.setdefaultencoding("utf-8")


class Mongo_Operate():

    def __init__(self, mongo_db='phishing_check', mongo_host='127.0.0.1',
                 mongo_port=27017, mongo_username='root', mongo_password=''):
        try:
            connect(mongo_db, host=mongo_host, port=mongo_port,
                    username=mongo_username, password=mongo_password)
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
        sys.stdout.write('%s  connect mongo win, ip: %s\n' %
                         (time.ctime(), mongo_host))
        self.gray_max_url = 10000  # 每个灰名单最大URL数量

    def deal_error(self, e):
        '''
        focus deal mongo error, print error info
        '''
        sys.stderr.write('%s  %s\n' % (time.ctime(), MongoError(e)))

    def objectID_get_gray(self, objectID):
        '''
        use objectID get gray_list
        '''
        try:  # 若指定objectID不存在，则新创建document
            Gray = getattr(GrayList, 'objects').get(id=objectID)
        except (DoesNotExist, ValidationError):
            Gray = GrayList(url_num=0)
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False
        return Gray

    def create_gray(self, gray_name='', gray_type='manual', usr_id=0, task_id=0):
        '''创建一个新的灰名单文档
        输入：灰名单文档名称、类型、用户id、任务id
        输出：灰名单objectID列表，仅有一条新创建的记录'''
        try:
            Gray = GrayList(url_num=0)
            current_time = time.strftime(
                '%Y-%m-%d %H:%M', time.localtime(time.time()))
            Gray.creat_time = current_time
            Gray.update_time = current_time
            if gray_type != '':
                Gray.gray_name = gray_name
            else:
                Gray.gray_name = current_time  # 探测时用时间替代
            Gray.gray_type = gray_type
            Gray.usr_id = int(usr_id)
            Gray.task_id = task_id
            Gray.use_count = 0
            Gray.child_gray = []
            Gray.save()
            return Gray.id
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def add_gray_url(self, add_url='', objectID=''):
        '''储存一条URL到garyID指定的可疑灰名单，若不指定objectID则创建新名单
        输入：objectID（已知document的objectID,若没指定新创建）
              add_url（待添加URL）
        输出：目标document列表
        '''
        try:
            if add_url is '':
                return False
            Gray = self.objectID_get_gray(objectID)
            if Gray.child_gray != []:
                add_Gray = getattr(GrayList, 'objects').get(
                    id=Gray.child_gray[-1])
            else:
                add_Gray = Gray
            # 当前灰名单中超过10w条URL时，新建并转存下一个灰名单
            if add_Gray.url_num / self.gray_max_url >= 1:
                add_Gray.save()
                if add_Gray.id != objectID and add_Gray.id not in Gray.child_gray:
                    Gray.child_gray.append(add_Gray.id)
                    Gray.url_num += self.gray_max_url
                add_Gray = GrayList(url_num=0)
            add_Gray.gray_list.append(add_url)
            add_Gray.url_num += 1
            add_Gray.save()
            if add_Gray.id != objectID and add_Gray.id not in Gray.child_gray:
                Gray.child_gray.append(add_Gray.id)
                Gray.url_num += add_Gray.url_num
            Gray.save()
            return True
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def add_gray_list(self, add_list=[], objectID=''):
        '''储存一个URL列表到garyID指定的可疑灰名单，若不指定objectID_list则创建新名单
        输入：objectID（已知document的objectID,若不指定或不存在新创建）
              add_list（待添加URL列表）
        输出：True or False
        '''
        try:
            if add_list == []:
                return False
            Gray = self.objectID_get_gray(objectID)
            if Gray.child_gray != []:
                add_Gray = getattr(GrayList, 'objects').get(
                    id=Gray.child_gray[-1])
            else:
                add_Gray = Gray
            for add_url in add_list:
                # 当前灰名单中超过10w条URL时，新建并转存下一个灰名单
                if add_Gray.url_num / self.gray_max_url >= 1:
                    add_Gray.save()
                    if add_Gray.id != objectID and add_Gray.id not in Gray.child_gray:
                        Gray.child_gray.append(add_Gray.id)
                        Gray.url_num += self.gray_max_url
                    add_Gray = GrayList(url_num=0)
                add_Gray.gray_list.append(add_url)
                add_Gray.url_num += 1
            add_Gray.save()
            if add_Gray.id != objectID and add_Gray.id not in Gray.child_gray:
                Gray.child_gray.append(add_Gray.id)
                Gray.url_num += add_Gray.url_num
            Gray.save()
            return True
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def expand_gray_list(self, objectID):
        '''
        objectID is str or list, 对objectID进行拓展，
        把其中每个灰名单的子名单也加入expand_objectID_list中
        '''
        try:
            expand_objectID_list = []
            if isinstance(objectID, unicode):
                objectID = [objectID]
            for garyID in objectID:
                try:
                    Gray = getattr(GrayList, 'objects').get(id=garyID)
                except (DoesNotExist, ValidationError), e:
                    sys.stderr.write(
                        '%s  %s  expand_gray_list, objectID: %s\n' %
                        (time.ctime(), MongoError(e), garyID))
                    continue
                expand_objectID_list.append(str(Gray.id))
                for child_id in Gray.child_gray:
                    expand_objectID_list.append(str(child_id))
            return expand_objectID_list
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def get_gray_num(self, garyID):
        '''
        获取指定灰名单的url数量
        '''
        try:
            try:
                Gray = getattr(GrayList, 'objects').get(id=garyID)
            except (DoesNotExist, ValidationError), e:
                sys.stderr.write(
                    '%s  %s  get_gray_num, objectID: %s\n' %
                    (time.ctime(), MongoError(e), garyID))
                return False
            return Gray.url_num
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def get_gray_list_num(self, gary_list):
        '''
        获取指定灰名单list的url数量
        '''
        url_num = 0
        try:
            for garyID in gary_list:
                try:
                    Gray = getattr(GrayList, 'objects').get(id=garyID)
                except (DoesNotExist, ValidationError), e:
                    sys.stderr.write(
                        '%s  %s  get_gray_list_num, objectID: %s\n' %
                        (time.ctime(), MongoError(e), garyID))
                    return False
                url_num += Gray.url_num
            return url_num
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def get_gray_list(self, objectID_list=[], read_objectID=None, read_url=None):
        '''用迭代器，返回已储存可疑灰名单中一条URL，并可继续之前读取的位置继续读
        输入：待读取的objectID列表、之前读取间断的objectID和在该ID对应灰名单中gray_list中的位置
        输出：迭代器'''
        try:
            if read_objectID in objectID_list:
                objectID_site = objectID_list.index(read_objectID)
                objectID_list = objectID_list[objectID_site:]
            first_sign = 0  # 本次读取，第一次调用该迭代器标志
            for garyID in objectID_list:
                try:
                    Gray = getattr(GrayList, 'objects').get(id=garyID)
                except (DoesNotExist, ValidationError), e:
                    sys.stderr.write(
                        '%s  %s  get_gray_list, objectID: %s\n' %
                        (time.ctime(), MongoError(e), garyID))
                    continue
                if first_sign is 0 and read_url is not None and read_url in Gray.gray_list:
                    url_site = Gray.gray_list.index(read_url)
                    goal_gray_list = Gray.gray_list[url_site:]
                    first_sign = 1
                else:
                    goal_gray_list = Gray.gray_list
                for gray_url in goal_gray_list:
                    yield gray_url
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)

    def get_once_gray(self, objectID='', read_url=None):
        '''用迭代器，返回已储存可疑灰名单中一条URL，并可继续之前读取的位置继续读
        输入：待读取的objectID、之前在该ID对应灰名单中读取间断的位置
        输出：迭代器'''
        try:
            try:
                Gray = getattr(GrayList, 'objects').get(id=objectID)
            except (DoesNotExist, ValidationError), e:
                sys.stderr.write(
                    '%s  %s  get_once_gray, objectID: %s\n' %
                    (time.ctime(), MongoError(e), objectID))
                # iterator def, can't return, only raise error
                raise StopIteration
            if read_url is not None and read_url in Gray.gray_list:
                url_site = Gray.gray_list.index(read_url)
                goal_gray_list = Gray.gray_list[url_site:]
            else:
                goal_gray_list = Gray.gray_list
            for gray_url in goal_gray_list:
                yield gray_url
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)

    def add_changed_domain(self, protected, new_exist_domain,
                           exist_change_domain, task_id, host_rule_list,
                           top_rule_list, path_rule_list, all_changed_num):
        '''
        将经过域名变换后生存的域名保存在知识库中，包括所有生成的域名和存在的域名
        '''
        try:
            try:  # 若指定protected previous save，则新创建document
                domain_change = getattr(DomainChange, 'objects').get(
                    protected_url=protected)
            except (DoesNotExist, ValidationError):
                domain_change = DomainChange(
                    protected_url=protected, exist_changed_num=0)
            # domain_change.changed_list.extend(all_change_domain)
            # domain_change.changed_num += len(all_change_domain)
            domain_change.exist_changed_list.extend(new_exist_domain)
            domain_change.exist_changed_num += len(new_exist_domain)
            once_changed = OnceChanged()
            update_time = time.strftime(
                '%Y-%m-%d %H:%M', time.localtime(time.time()))
            once_changed.changed_time = update_time
            once_changed.task_id = task_id
            if len(domain_change.exist_note) != 0:
                for last_changed in domain_change.exist_note[::-1]:
                    if len(last_changed.exist_changed_list) == 0:
                        continue
                    if last_changed.exist_changed_list == exist_change_domain:
                        domain_change.exist_note.append(once_changed)
                        domain_change.save()
                        return True
                    else:
                        break
            once_changed.exist_changed_list = exist_change_domain
            once_changed.exist_changed_num = len(exist_change_domain)
            once_changed.host_rule_list = host_rule_list
            once_changed.top_rule_list = top_rule_list
            once_changed.path_rule_list = path_rule_list
            once_changed.all_changed_num = all_changed_num
            domain_change.exist_note.append(once_changed)
            domain_change.save()
            return True
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def add_changed_grays(self, protected, task_id, objectID):
        '''
        domian: path joined, exist url save
        '''
        try:
            try:  # 若指定objectID不存在，save failure
                domain_change = getattr(DomainChange, 'objects').get(
                    protected_url=protected)
            except (DoesNotExist, ValidationError), e:
                sys.stderr.write(
                    '%s  %s  add_changed_grays, objectID: %s\n' %
                    (time.ctime(), MongoError(e), objectID))
                return False
            k = 0
            for once_changed in domain_change.exist_note[::-1]:
                k += 1
                if once_changed.task_id == task_id:
                    if once_changed.gray_ID is not None:
                        return False
                    break
            once_changed.gray_ID = objectID
            k = len(domain_change.exist_note) - k
            domain_change.exist_note[k] = once_changed
            domain_change.save()
            return True
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def url_get_websave(self, url, url_type, get_type):
        '''
        if url previous saved web, return
        else create new document in mongo
        url_type: include: gray, protected, counterfeit, monitor
            correspond three collection
        get_type: include: get, add.
            add: if not exist, create new record
            get: if not exist, raise error
        '''
        try:
            if url_type == 'gray':
                web_save = getattr(GrayWebSave, 'objects').get(web_url=url)
            elif url_type == 'protected':
                web_save = getattr(
                    ProtectedWebSave, 'objects').get(web_url=url)
            elif url_type == 'counterfeit':
                web_save = getattr(
                    CounterfeitWebSave, 'objects').get(web_url=url)
            elif url_type == 'monitor':
                web_save = getattr(
                    MonitorWebSave, 'objects').get(web_url=url)
            else:
                '''sys.stderr.write(
                    '%s  url_type error, url_get_websave, url: %s, url_type: %s, get_type: %s\n' %
                    (time.ctime(), url, url_type, get_type))'''
                return False
        except (DoesNotExist, ValidationError), e:
            if get_type == 'add':
                if url_type == 'gray':
                    web_save = GrayWebSave(web_url=url)
                elif url_type == 'protected':
                    web_save = ProtectedWebSave(web_url=url)
                elif url_type == 'counterfeit':
                    web_save = CounterfeitWebSave(web_url=url)
                elif url_type == 'monitor':
                    web_save = MonitorWebSave(web_url=url)
            else:
                '''sys.stderr.write(
                    '%s  url not exist, url_get_websave, %s, url: %s, url_type: %s, get_type: %s\n' %
                    (time.ctime(), MongoError(e), url, url_type, get_type))'''
                return False
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False
        except:
            sys.stderr.write(
                '%s  url_get_websave maybe MultipleObjectsReturned, url: %s, url_type: %s, get_type: %s\n' %
                (time.ctime(), url, url_type, get_type))
            traceback.print_exc()
            return False
        return web_save

    def add_web_tree(self, url, url_type, new_tree):
        '''
        保存筛选后的dom树
        '''
        try:
            web_save = self.url_get_websave(url, url_type, get_type='add')
            if web_save is False:
                return False
            new_tree_hash = hash_md5(str(new_tree))
            try:
                dom_tree = web_save.web_tree_list[-1]
                if dom_tree.tree_hash != new_tree_hash:
                    dom_tree = DomTree()
                else:
                    return False
            except:  # 当第一次保存该网页的时候list不存在
                dom_tree = DomTree()
            node_num = 0
            for node in new_tree:
                dom_node = DomNode()
                dom_node.num = node_num
                dom_node.top = node[0]
                dom_node.left = node[1]
                dom_node.height = node[2]
                dom_node.width = node[3]
                dom_tree.dom_nodes.append(dom_node)
                node_num += 1
            dom_tree.update_time = time.strftime(
                '%Y-%m-%d %H:%M', time.localtime(time.time()))
            dom_tree.tree_hash = new_tree_hash
            web_save.web_tree_list.append(dom_tree)
            web_save.save()
            return True
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def get_web_tree(self, url, url_type):
        '''
        获取指定URL的最新dom树
        '''
        try:
            web_save = self.url_get_websave(url, url_type, get_type='get')
            if web_save is False:
                return False
            if web_save.web_tree_list == []:
                return []
            saved_dom_nodes = web_save.web_tree_list[-1].dom_nodes
            dom_tree = []
            for node in saved_dom_nodes:
                dom_tree.append(
                    [node.num, node.top, node.left, node.height, node.width])
            return dom_tree
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def add_web_title(self, url, url_type, new_title):
        '''
        保存网页title
        '''
        try:
            web_save = self.url_get_websave(url, url_type, get_type='add')
            if web_save is False:
                return False
            try:
                web_title = web_save.web_title_list[-1]
                # 不能将unicode对象和str对象进行比较，需将str对象转换
                if web_title.title != new_title.decode('utf-8'):
                    web_title = WebTitle(title=new_title)
                else:
                    return False
            except:  # 当第一次保存该网页的时候list不存在, list[-1] error
                web_title = WebTitle(title=new_title)
            web_title.update_time = time.strftime(
                '%Y-%m-%d %H:%M', time.localtime(time.time()))
            web_save.web_title_list.append(web_title)
            web_save.save()
            return True
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def get_web_title(self, url, url_type):
        '''
        获取指定URL的最新title
        '''
        try:
            web_save = self.url_get_websave(url, url_type, get_type='get')
            if web_save is False:
                return False
            if web_save.web_title_list == []:
                return ''
            return web_save.web_title_list[-1].title
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def add_web_text(self, url, url_type, new_text):
        '''
        保存网页text or kword
        '''
        try:
            web_save = self.url_get_websave(url, url_type, get_type='add')
            if web_save is False:
                return False
            new_text_hash = hash_md5(str(new_text))
            try:
                web_text = web_save.web_text_list[-1]
                # 当网页dom树和网页文本改变的时候才重新保存
                if web_text.text_hash != new_text_hash:
                    web_text = WebText(text=new_text)
                else:
                    return False
            except:  # 当第一次保存该网页的时候web_info不存在, list[-1] error
                web_text = WebText(text=new_text)
            web_text.text_hash = new_text_hash
            web_text.update_time = time.strftime(
                '%Y-%m-%d %H:%M', time.localtime(time.time()))
            web_save.web_text_list.append(web_text)
            web_save.save()
            return True
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def get_web_text(self, url, url_type):
        '''
        获取指定URL的最新text or kword
        '''
        try:
            web_save = self.url_get_websave(url, url_type, get_type='get')
            if web_save is False:
                return False
            if web_save.web_text_list == []:
                return ''
            return web_save.web_text_list[-1].text
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def add_web_view(self, url, url_type, new_view):
        '''
        保存视觉特征
        '''
        try:
            web_save = self.url_get_websave(url, url_type, get_type='add')
            if web_save is False:
                return False
            new_view_hash = hash_md5(str(new_view))
            try:
                view_feature = web_save.web_view_list[-1]
                # 当网页视觉特征的hash值改变的时候才重新保存
                if view_feature.view_hash == new_view_hash:
                    return False
            except:  # 当第一次保存该网页的时候web_info不存在, list[-1] error
                view_feature = WebViewFeature()
            view_feature.update_time = time.strftime(
                '%Y-%m-%d %H:%M', time.localtime(time.time()))
            view_feature.view_hash = new_view_hash
            for once_image in new_view:
                image = Image()
                image.image_type = once_image[0]
                image.image_name = once_image[1]
                image.image_dct = once_image[2]
                image.image_site = once_image[3]
                for new_cheild_image in once_image[4]:
                    child_image = ChildImage()
                    child_image.border_coordinate = new_cheild_image[0]
                    child_image.core_coordinate = new_cheild_image[1]
                    child_image.core_distance = new_cheild_image[2]
                    child_image.core_angle = new_cheild_image[3]
                    child_image.core_ratio = new_cheild_image[4]
                    child_image.info_entropy = new_cheild_image[5]
                    child_image.eccentricity = new_cheild_image[6]
                    child_image.rotundity_nature = new_cheild_image[7]
                    child_image.invariant_matrix = new_cheild_image[8]
                    image.child_image.append(child_image)
                view_feature.image_list.append(image)
            web_save.web_view_list.append(view_feature)
            web_save.save()
            return True
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def get_web_view(self, url, url_type):
        '''
        获取指定URL的最新视觉特征
        '''
        try:
            web_save = self.url_get_websave(url, url_type, get_type='get')
            if web_save is False:
                return False
            view_feature = []
            if web_save.web_view_list == []:
                return []
            for once_image in web_save.web_view_list[-1].image_list:
                current_image = []
                current_image.append(once_image.image_type)
                current_image.append(once_image.image_name)
                current_image.append(once_image.image_dct)
                current_image.append(once_image.image_site)
                current_image.append([])
                for once_cheild_image in once_image.child_image:
                    current_cheild_image = []
                    current_cheild_image.append(
                        once_cheild_image.border_coordinate)
                    current_cheild_image.append(
                        once_cheild_image.core_coordinate)
                    current_cheild_image.append(
                        once_cheild_image.core_distance)
                    current_cheild_image.append(once_cheild_image.core_angle)
                    current_cheild_image.append(once_cheild_image.core_ratio)
                    current_cheild_image.append(once_cheild_image.info_entropy)
                    current_cheild_image.append(once_cheild_image.eccentricity)
                    current_cheild_image.append(
                        once_cheild_image.rotundity_nature)
                    current_cheild_image.append(
                        once_cheild_image.invariant_matrix)
                    current_image[4].append(current_cheild_image)
                view_feature.append(current_image)
            return view_feature
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def add_web_border(self, url, url_type, nwe_border_list):
        '''
        add web width and high, as web border    new_width, new_high
        '''
        new_width = nwe_border_list[0]
        new_high = nwe_border_list[1]
        try:
            web_save = self.url_get_websave(url, url_type, get_type='add')
            if web_save is False:
                return False
            try:
                web_border = web_save.web_border_list[-1]
                if web_border.width != new_width and web_border.high != new_high:
                    web_border = WebBorder(width=new_width, high=new_high)
                else:
                    return False
            except:  # 当第一次保存该网页的时候list不存在, list[-1] error
                web_border = WebBorder(width=new_width, high=new_high)
            web_border.update_time = time.strftime(
                '%Y-%m-%d %H:%M', time.localtime(time.time()))
            web_save.web_border_list.append(web_border)
            web_save.save()
            return True
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def get_web_border(self, url, url_type):
        '''
        获取指定URL的最新width and high
        '''
        try:
            web_save = self.url_get_websave(url, url_type, get_type='get')
            if web_save is False:
                return False
            if web_save.web_border_list == []:
                return []
            border = web_save.web_border_list[-1]
            return [border.width, border.high]
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False

    def transfer_web_save(self, url, source_type, goal_type):
        try:
            source_web_save = self.url_get_websave(
                url, source_type, get_type='get')
            if source_web_save is False:
                return False
            source_tree = self.get_web_tree(url, source_type)
            source_title = self.get_web_title(url, source_type)
            source_text = self.get_web_text(url, source_type)
            source_view = self.get_web_view(url, source_type)
            source_border = self.get_web_border(url, source_type)
            self.add_web_tree(url, goal_type, source_tree)
            self.add_web_title(url, goal_type, source_title)
            self.add_web_text(url, goal_type, source_text)
            self.add_web_view(url, goal_type, source_view)
            self.add_web_border(url, goal_type, source_border)
            return True
        except errors, e:
            traceback.print_exc()
            self.deal_error(e)
            return False


if __name__ == "__main__":
    test = Mongo_Operate(mongo_db='phishing_check', mongo_host='192.168.65.148',
                         mongo_port=27017, mongo_username='root', mongo_password='')

    #test.transfer_web_save('http://bfssr.cc/', 'gray', 'monitor')

    objectID = test.create_gray(
        gray_name='test', gray_type='manual', usr_id=1)
    print objectID
    gray_url_list = [
        'http://www.eastmoney.com/',
        'http://finance.china.com.cn/',
        'http://bfssr.cc/',
        'http://cpuzt.cc/',
        'http://www.138.gg/',
        'http://www.bjstkc.com/'
    ]
    test.add_gray_list(gray_url_list, objectID)

    '''with open('three_part', 'r') as f:
        urls = f.readlines()
    k = 0
    url_list = []
    for url in urls:
        url = url[:-1]
        print url
        url_list.append(url)
        k += 1
        if k == 500:
            break
    objectID = test.create_gray(
        gray_name='test', gray_type='manual', usr_id=1)
    print objectID
    test.add_gray_list(url_list, objectID)'''

    '''
    with open('phishing_gw', 'r') as f:
        read_info = f.readlines()
    phishing_info_list = []
    for info in read_info:
        phishing_info_list.append(info[:-1].split('#'))
    objectID = test.create_gray(
        gray_name='test', gray_type='manual', usr_id=1)
    print objectID
    url_list = []
    for phishing_info in phishing_info_list:
        print phishing_info
        counterfeit_url = phishing_info[3]
        url_list.append(counterfeit_url)
    test.add_gray_list(url_list, objectID)
    '''
    '''
    objectID_list = ['558e89c1351ff524a3cbe84d']
    print objectID_list
    objectID_list = test.expand_gray_list(objectID_list)
    print objectID_list
    gary_list = test.get_gray_list(
        objectID_list)  # 自行添加objectID
    while 1:
        try:
            gray_url = gary_list.next()
            print gray_url
        except StopIteration:
            break
    '''
    # 视觉特征存取测试
    '''url = 'http://www.zhijinwang.cn'
    image = [[2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/0tmp.jpeg', '669e661a98e783bb7e647c647e46652065006758fc467c467e7ea3f3c8adb772', '01101100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/1tmp.jpeg', '00000000000000000000000000000000000000004a95b52ab52a429500008502', '11111100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/4tmp.jpeg',
                                                                                                                                                                                                                                                                                                                                                                                                                                    'e300630cabaaaaaaaaaaaaaaaaaaaaaaffffffffffffffffffffffffffffffff', '01111100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/7tmp.jpeg', '00002a0055055595459cc69ca55ab552b55255a555a555a952a12a0055a955a9', '10111100', [[[1, 8, 117, 12], [56, 13], 49.0, 76.93068210371783, 0.23347102124769356, 4.8450984097341925, 0.9797060176239845, 0.84955188258642, [0.004270272521263887, 1.7375440332876605e-05, 8.409505124229687e-11, -7.028340855752252e-23]]]]]
    image = [[2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/0tmp.jpeg', '669e661a98e783bb7e647c647e46652065006758fc467c467e7ea3f3c8adb772', '01101100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/1tmp.jpeg', '00000000000000000000000000000000000000004a95b52ab52a429500008502', '11111100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/4tmp.jpeg', 'e300630cabaaaaaaaaaaaaaaaaaaaaaaffffffffffffffffffffffffffffffff', '01111100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/7tmp.jpeg', '00002a0055055595459cc69ca55ab552b55255a555a555a952a12a0055a955a9', '10111100', [[[1, 8, 117, 12], [56, 13], 49.0, 76.93068210371783, 0.23347102124769356, 4.8450984097341925, 0.9797060176239845, 0.84955188258642, [0.004270272521263887, 1.7375440332876605e-05, 8.409505124229687e-11, -7.028340855752252e-23]]]], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/8tmp.jpeg', '80ff80ffffff80ff80ffffffc0ffffff00ff80ffffff80ffffff00ff80ffffff', '11101100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/9tmp.jpeg', '556555755575556555d1554555455545555555155595559555f555f555755537', '00101100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/10tmp.jpeg', '55755575156155414dd55dd55555556555555555555555555555551555555555', '01011100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/11tmp.jpeg', '5555555555555555555555555555555555555555555555555555555555555555', '01011100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/12tmp.jpeg', '0000000000000000000000000000000000000000000000005555555555555555', '11101100', [[[1, 8, 117, 12], [56, 13], 49.0, 76.93068210371783, 0.23347102124769356, 4.8450984097341925, 0.9797060176239845, 0.84955188258642, [0.004270272521263887, 1.7375440332876605e-05, 8.409505124229687e-11, -7.028340855752252e-23]]]], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/13tmp.jpeg', '6d4b4900000000000000000000000000000000000000000000006f323f907fc0', '11101100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/14tmp.jpeg', '005500543fa0ffe45f55ffff0000550005000500000055555555555500001500', '11011100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/15tmp.jpeg', '55555555555555555555555555555555551554555455541554955495549d54dd', '01011100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/16tmp.jpeg', '555556d776d536ddb6c3b6c3b6c1b645165d364d565555555555555555555555', '10011100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/17tmp.jpeg', '555555555555555555555654d650d250d25cd25cd25c525056535a5356575555', '10011100', [[[1, 8, 117, 12], [56, 13], 49.0, 76.93068210371783, 0.23347102124769356, 4.8450984097341925, 0.9797060176239845, 0.84955188258642, [0.004270272521263887, 1.7375440332876605e-05, 8.409505124229687e-11, -7.028340855752252e-23]]]], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/18tmp.jpeg', '5555555555555555555555555555555555555555555555555555555555555555', '10011100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/19tmp.jpeg', '761776d7555554555555555555555555555555555555555554555e45fe04fe44', '10011100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/20tmp.jpeg', 'eec4ee44fe447e457e047e445555545555555555555555555555555555555555', '10011100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/21tmp.jpeg', '555575946d106f74ef766f306f306fb06db06fb06d906db06f306b31d777d767', '10011100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/22tmp.jpeg', '1e071e171e551e571e5755555555555555555555555555555555555555555555', '10001100', [[[1, 8, 117, 12], [56, 13], 49.0, 76.93068210371783, 0.23347102124769356, 4.8450984097341925, 0.9797060176239845, 0.84955188258642, [0.004270272521263887, 1.7375440332876605e-05, 8.409505124229687e-11, -7.028340855752252e-23]]]], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/23tmp.jpeg', '55555555555555555555554955485548fc48b448f648f44955d4574855555555', '10001100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/25tmp.jpeg', '5555555555555c55e4474e7c4efcce5ccc7d6647f047f05755555455c67564fc', '10001100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/27tmp.jpeg', '55555555555555555455545154715c15dc719c73dc73dc73dc7ddc7ddc7f5555', '10001100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/28tmp.jpeg', '75777475f077f0f170f170f170f1f0f5f0f5f0f155d555d555d5777777775577', '10001100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/29tmp.jpeg', '55555415040054545c54ccc5ce5dce41ce5dfed55cd7fedf7657775577775555', '10001100', [[[1, 8, 117, 12], [56, 13], 49.0, 76.93068210371783, 0.23347102124769356, 4.8450984097341925, 0.9797060176239845, 0.84955188258642, [0.004270272521263887, 1.7375440332876605e-05, 8.409505124229687e-11, -7.028340855752252e-23]]]], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/30tmp.jpeg', '555555555555545504005415c49cdc55dc5ddc1ddc7d7e7766f7fedf76777777', '10001100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/31tmp.jpeg', '76775c1ddc1ddcfddcfddcdd543754375c357677777777777777555555555555', '10001100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/32tmp.jpeg', '5555475555555755575555555555545557555755555556555555555557555555', '11001100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/33tmp.jpeg', '9b240d061c0f1c0f2d0e2d0a2d8a2d0216050d0b07c986d126d1c6598759a751', '11001100', []], [2, u'/home/zxy/phishing_check/web/www.zhijinwang.cn/1354f992/e5c194b7/d141cb0b/6c599193/2015-05-18 16_15/34tmp.jpeg', '5555555555555555555555555755575557554755475557555755575557555555', '11001100', [[[1, 8, 117, 12], [56, 13], 49.0, 76.93068210371783, 0.23347102124769356, 4.8450984097341925, 0.9797060176239845, 0.84955188258642, [0.004270272521263887, 1.7375440332876605e-05, 8.409505124229687e-11, -7.028340855752252e-23]]]]]

    test.add_view_feature(url, image)
    print test.get_web_view(url)'''

    # 域名存活情况统计测试
    '''original_domain = 'www.icbc.com.cn'
    new_exist_domain = []
    exist_change_domain = ['www.1cbc.com.cn', 'www.icbcb.com.cn',
                           'www.icbcb.com.com', 'www.icbcc.com.com', 'www.icbcc.com.cn']
    task_id = 3
    host_rule_list = ['io(\\d+)=io(0--4)', 'alde=elde', 'tle=tlenet', 'haker=(a--f)aker,hak(h--k)',
                      'bit=bits']
    top_rule_list = ['\.com=.cn,.tk,.net,.org']
    path_rule_list = [
        '/bank.asp', '/icbc.asp', '/login.asp', '/icbcb.asp', '/iicbc.asp']
    all_change_num = 792
    test.add_changed_domain(
        original_domain, new_exist_domain, exist_change_domain,
        task_id, host_rule_list, top_rule_list,
        path_rule_list, all_change_num)
    test.add_changed_grays(original_domain, 3, '5576c686351ff51339945d28')'''

    # 可疑灰名单写测试
    '''url_list = ['http://www.sina.cn/pay/icbc/',
                'http://www.sina.cn',
                'http://www.icbc.com/',
                'http://www.fx168.com/',
                ]

    objectID1 = test.create_gray(
        gray_name='web_save', gray_type='manual', usr_id=1)
    print objectID1
    test.add_gray_list(url_list, objectID1)'''

    # 可疑灰名单读测试
    '''objectID_list = ['5558235c351ff523f42f2720']
    print objectID_list
    objectID_list = test.expand_gray_list(objectID_list)
    print objectID_list
    gary_list = test.get_gray_list(
        objectID_list)  # 自行添加objectID
    while 1:
        try:
            gray_url = gary_list.next()
            print gray_url
        except StopIteration:
            break

    print '————————————————————————————————————————————————————'
    '''
    '''gary_list = test.get_once_gray('553486d800999b0da83263fd')  # 自行添加objectID
    for i in range(100):
        try:
            gray_url = gary_list.next()
            print gray_url
        except StopIteration:
            break'''

    # 网页保存写测试
    goal_url = 'http://www.inet.com/'
    tree = [[1, 1, 28, 164, 47, 375], [
        1, 1, 86, 175, 34, 353], [1, 1, 0, 0, 377, 528]]
    #title = '百度 * hahaa'
    #text = " QT防卡死循环重启介绍检测引擎在进行比对分析时，遇到QT模块卡死或者其他未知原因造成检测引擎卡死时，需要及时的发现并重启检测引擎，继续上次未执行完的任务。解决方案:每个引擎行在一个守护子进程中，引擎在启动时创建一个以检测进程pid命名的一个文件，假如说同时开多个title引擎，他们均写在同一个目录下，目录是固定的每个引擎在开始检测一个新的可疑URL时，在检测前将这个URL以更新的方式写入到进程对应的pid文件中，每个pid文件只存放当前引擎检测的一条URL记录。测引擎每完成一次URL检测，在任务数据库存储的URL中找到这条URL记录，并进行标记，表示已经进行过检测。服务守护进程在一个线程中定期循环检查这个目录下的所有pid文件，如果发现某个文件在前后两次检查中没有更新，则判定该引擎已经卡死，根据该文件名（pid），杀死对应的引擎进程，并重启引擎，以引擎上次卡死前文件中存放的URL作为重启引擎的断点任务，并跳过这个造成卡死的URL，从卡死URL后的第一条重新开始检测。检测引擎在全部检测完成后向pid文件中写入over，服务守护进程定期查询这个目录下的所有文件时，发现over，则杀死引擎进程并删除这个文件，此时不再重启引擎。引擎检测完成后，服务守护进程查看任务URL中未正常检测的URL(即未被标记)，启动一个引擎对这些URL进行一次检测，直到文件中写入over，完成这次检测后，对仍未进程正常检测的URL进行特殊标记。"
    test.add_web_tree(goal_url, 'gray', tree)
    #test.add_web_title(goal_url, 'gray', title)
    #test.add_web_text(goal_url, 'gray', text)
    print test.get_web_tree(goal_url, 'gray')
    # print test.get_web_title(goal_url, 'gray')
    # print test.get_web_text(goal_url, 'gray')
    print 'program over'
