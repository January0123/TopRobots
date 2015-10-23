# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.browser_manager.ucbrowsermanager
# 
# Creation      : 2014-4-14
# Author        : laijx@ucweb.com
###########################################################################

import browsermanager
 
class Browser360Manager(browsermanager.BrowserManager):
    """ 360浏览器管理类，封装了启动浏览器、加载URL，关闭浏览器等方法
    """
    def __init__(self, pkg_name, activity=None, device=None):
        """ 构造方法

        :param pkg_name: 浏览器的包名
        :type pkg_name: string

        :param activity: 浏览器的Activity名
        :type activity: string

        :param device: 设备串号
        :type device: string
        """
        browsermanager.BrowserManager.__init__(self, pkg_name, activity, device)
    
        
    def removeWelcomePage(self):
        """ 移除新手教育界面
        """
        parent = super(Browser360Manager, self)
        parent.startActivity()
        
    def cleanCache(self):
        """ 清除浏览器缓存
        """
        # app_chrome,app_textures,cache,databases,files 
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/databases")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/cache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/app_appcache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/app_database")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/app_geolocation")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/app_icons")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/app_bookmark")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/files")