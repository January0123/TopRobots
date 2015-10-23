# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.browsermanagerfactory
# 
# Creation      : 2013-10-31
# Author        : huangjj@ucweb.com
###########################################################################

from uc_tools.browser_manager import browsermanager
from uc_tools.browser_manager import ucbrowsermanager
from uc_tools.browser_manager import chromebrowsermanager
from uc_tools.browser_manager import firefoxbrowsermanager
from uc_tools.browser_manager import baidubrowsermanager
from uc_tools.browser_manager import qqbrowsermanager
from uc_tools.browser_manager import browser360manager

 
class BrowserManagerFactory(object):
    """ 获取手机管理类的工厂类

    下面是一个简单的使用方法::

        from uc_tools.browsermanagerfactory import BrowserManagerFactory

        pkg_name = "com.android.chrome" 
        activity_name = "com.google.android.apps.chrome.Main"
        browser_manager_factory = BrowserManagerFactory()   # 初始化浏览器管理对象工厂类
        browser_manager = browser_manager_factory.getBrowserManager(pkg_name)   # 根据包名获取相应的浏览器管理对象
        browser_manager.setActivity(activity_name)  # 设置浏览器管理类中浏览器的activity名字
        browser_manager.cleanCache()    #  清楚缓存
        browser_manager.startActivity() # 启动浏览器

    .. tip:: 当前支持的具体的浏览器管理类有UC浏览器、QQ浏览器、chrome浏览器，firefox浏览器，百度浏览器，360浏览器，其他浏览器返回默认的浏览器管理类
    """
     
    def __init__(self, device=None):
        """ 构造方法

        :param device: 手机串号
        :type device: string
        """
        # self.cmd_exec = cmdexec.CMDExec()
        # if device:
        #     self.cmd_exec.setTargetSerial(device)
        #: 设备串号
        self.device = device
        
    def getBrowserManager(self, pkg_name):
        """ 根据包名获取相应的浏览器管理对象，如果匹配失败，则返回默认的浏览器管理对象

        :param pkg_name: 浏览器包名
        :type pkg_name: string

        :returns: 根据包名返回相应的浏览器管理对象
        :rtype: browsermanager
        """
        if ("UC" in pkg_name) or ("uc" in pkg_name):
            return ucbrowsermanager.UCBrowserManager(pkg_name, device=self.device)
        elif "tencent" in pkg_name:
            return qqbrowsermanager.QQBrowserManager(pkg_name, device=self.device)
        elif "chrome" in pkg_name:
            return chromebrowsermanager.ChromeBrowserManager(pkg_name, device=self.device)
        elif "firefox" in pkg_name:
            return firefoxbrowsermanager.FirefoxBrowserManager(pkg_name, device=self.device)
        elif "baidu" in pkg_name:
            return baidubrowsermanager.BaiduBrowserManager(pkg_name, device=self.device)
        elif "qihoo" in pkg_name:
            return browser360manager.Browser360Manager(pkg_name, device=self.device)
        else:
            return browsermanager.BrowserManager(pkg_name, device=self.device)