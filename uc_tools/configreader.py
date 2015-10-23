# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : configreader
# 
# Creation      : 2013-12-18
# Author        : huangjj@ucweb.com
###########################################################################

import ConfigParser

class ConfigReader(object):
    """ 帮助读取格式为*.ini 和 *.cfg 格式的配置文件
    """
    
    def __init__(self, log_file_url):
        """ 构造方法

        :param log_file_url: 配置文件的路径
        :type log_file_url: string
        """
        self.__log_file_url = log_file_url
        self.__config = None
        self.readConfig();
    
    def readConfig(self):
    	""" 创建ConfigParser对象并且读取配置

        :returns: ConfigParser对象
        :rtype: ConfigParser
        """
        # if self.__config is not None, return this object
        if self.__config:
            return self.__config

        self.__config = ConfigParser.ConfigParser()
        self.__config.optionxform = str
        cfgfile = open(self.__log_file_url)
        self.__config.readfp(cfgfile)
        return self.__config
    
    def getSections(self):
        """ 获取配置文件的节点

        :returns: 配置文件中所拥有哦的所有节点列表
        :rtype: list
        """
        sections = self.__config.sections()
        return sections
    
    def getItems(self, section_name):
        """ 获取节点下面的所有键值对

        :param section_name: 节点名字
        :type section_name: string

        :returns: 节点下面的键值对，eg:((name, value))
        :rtype: list
        """
        items = self.__config.items(section_name)
        return items 

    def getValue(self, section_name, item_name):
        """ 获取某个节点下对应键的值

        :param section_name: 节点名字
        :type section_name: string

        :param item_name: 键的名字
        :type item_name: string

        :returns: 某个节点下对应键的值
        :rtype: string
        """
    	value = self.__config.get(section_name, item_name)
    	return value
