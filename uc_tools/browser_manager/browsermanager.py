# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.browsermanager
# 
# Creation      : 2013-10-31
# Author        : huangjj@ucweb.com
###########################################################################

import time
from uc_tools import pkgmanager

class BrowserManager(pkgmanager.PKGManager):
    """ 默认的浏览器管理类，封装了启动浏览器、加载URL，关闭浏览器等方法
    """
    def __init__(self, pkg_name=None, activity=None, device=None):
        """ 构造方法
 
        :param pkg_name: 浏览器的包名
        :type pkg_name: string

        :param activity: 浏览器的Activity名
        :type activity: string

        :param device: 设备串号
        :type device: string
        """
        pkgmanager.PKGManager.__init__(self,pkg_name, activity, device)  
        self.browser_dict = {
                             "com.tencent.mtt"   : ".SplashActivity",
                             "com.android.chrome": "com.google.android.apps.chrome.Main",
                             "com.UCMobile"      : "com.UCMobile.main.UCMobile",
                             "com.oupeng.mini.android" : "com.opera.mini.android.Browser",
                             "mobi.mgeek.TunnyBrowser" : ".BrowserActivity",
                             }  
        
    def removeWelcomePage(self):
        """ 移除新手教育界面
        """
        try:
            parent = super(BrowserManager, self)
            parent.startActivity()
            time.sleep(5)
            parent.killPid()
        except Exception, e:
            print "browser remover welcome page error :"+str(e)
    
    def cleanCache(self):
        """清除浏览器缓存
        """
        pass
    
    def getPKGList(self):
        """ 获取浏览器列表
        """
        all_pkg_list = super(BrowserManager, self).getPKGList() 
        all_browser_pkg_list = []
        
        for key in self.browser_dict.keys():
            for pkg_name in all_pkg_list:
                if key in pkg_name:
                    all_browser_pkg_list.append(pkg_name)   
        return all_browser_pkg_list  
        
    def loadUrl(self, url):
        """ 加载url

        :param url: 需要加载的url
        :type url: string
        """
        parent = super(BrowserManager, self)
        parent.startActivity(data=url)
            
        