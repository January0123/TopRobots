# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.convert
# 
# Creation      : 2013-11-1
# Author        : huangjj@ucweb.com
###########################################################################
import base64
import struct
import hashlib


def md5Encode(content):
    """ 给字符串进行MD5加密

    :param content: 需要加密的内容
    :type content: string
    """
    md5 = hashlib.md5()
    md5.update(content)
    result = md5.hexdigest()
    return result

def base64Encode(content):
    """ 给字符串进行base64加密

    :param content: 需要加密的内容
    :type content: string
    """
    result = base64.encodestring(content) 
    return result

def base64Decode(content):
    """ 给字符串进行base64解密

    :param content: 需要解密的内容
    :type content: string
    """
    result = base64.decodestring(content)
    return result
    