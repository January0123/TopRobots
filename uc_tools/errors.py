# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File   : error
# 
# Creation      : 2013-8-24
# Author : zhangrong@ucweb.com
###########################################################################

r"""
定义了基类中常用的异常类
"""
 
class MsgException(Exception):
    """ 可以设置异常信息的通用的异常类
    """
    def __init__(self, msg=""):
        self.msg = msg

class WaitForResponseTimedOutError(Exception):
    """ 执行一个命令并且太久没有响应的时候，返回这个异常类
    """

class DeviceUnresponsiveError(Exception):
    """ 设备对命令执行没有响应的时候，返回这个异常类
    """

class InstrumentationError(Exception):
    """ 执行 ``instrumentation`` 失败的时候。返回这个异常类
    """

class AbortError(MsgException):
    """ 该异常表明产生了一个致命的错误并且程序必须退出
    """
    
class ParseError(MsgException):
    """ 当数据解析错误的时候跑出该异常
    """
        

 
