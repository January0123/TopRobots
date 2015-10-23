# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.browser_manager.ucbrowsermanager
# 
# Creation      : 2013-10-31
# Author        : huangjj@ucweb.com
###########################################################################

import time
import os
import browsermanager
from uc_tools import runcommand

class QQBrowserManager(browsermanager.BrowserManager):
    '''
    some operations about QQBrowser
    '''


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
        self.cwd = os.path.split(os.path.realpath(__file__))[0]
          
    def removeWelcomePage(self):
        """
        移除QQ浏览器首页
        """
        parent = super(QQBrowserManager, self)
        parent.removeWelcomePage()
 

    def cleanCache(self):
        """清除浏览器缓存
        """
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/databases")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/cache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/app_appcache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/app_databases")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/files")