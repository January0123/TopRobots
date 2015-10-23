# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.connectionoperator
# 
# Creation      : 2013-11-1
# Author        : huangjj@ucweb.com
###########################################################################

import urllib, urllib2

def requestByPost(url, values, read_content=True):
    """ 发送一个Post请求

    :param url: 请求URL
    :type url: string

    :param values: 需要发送的参数
    :type values: dict

    :param read_content: 决定着返回的是response对象还是读取出来的内容
    :type read_content: bool

    :returns: 如果 ``read_content`` 的值为 ``True``，返回调用 ``response.read()`` 方法读取出来的问题,否则直接返回response对象，这个时候需要开发者在外面调用close方法关闭请求
    :rtype: string 或者 object
    """
    result = ""
    try:
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response =  urllib2.urlopen(req)

        if read_content:
            result = response.read()
            response.close()
            return result
        else:
            return response
    except Exception,e :
        raise e
        print "Exception is: "+str(e)
    
def requestByGet(url, data=None, read_content=True):
    """ 发送一个Get请求

    :param url: 请求URL
    :type url: string

    :param values: 需要发送的参数
    :type values: dict

    :param read_content: 决定着返回的是response对象还是读取出来的内容
    :type read_content: bool

    :returns: 如果 ``read_content`` 的值为 ``True``，返回调用 ``response.read()`` 方法读取出来的问题,否则直接返回response对象，这个时候需要开发者在外面调用close方法关闭请求
    :rtype: string 或者 object
    """
    try:
        result = ""
        full_url = url
        if data:
            url_values = urllib.urlencode(data) 
            full_url = url + '?' + url_values   
        response = urllib2.urlopen(full_url)
        if read_content:
            result = response.read()
            response.close()
            return result
        else:
            return response
    except Exception, e:
        raise e
        print "Exception is: "+str(e)
   