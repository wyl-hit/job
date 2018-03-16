# -*- coding: UTF-8 -*-
'''
define decorator
'''

#import functools


def autoInitClass(OldClass):
    """
    装饰器
    自动初始化父类方法
    注：父类无初始化属性，切基类需要继承自object类
    """
    superClass = OldClass.mro()[1]

    class NewClass(OldClass):

        def __init__(*args):
            self = args[0]
            superClass.__init__(self)
            apply(OldClass.__init__, args)
    return NewClass


'''def freePMEM(func):
    """
    装饰器
    调用entry之前调用freeParent方法
    """
    @functools.wraps(func)
    def freeFunc(self, *args, **kwargs):
        self.freeParent()
        func(self, *args, **kwargs)
    return freeFunc'''
