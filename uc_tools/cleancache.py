#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : cleancache.py
# 
# 
# Creation      : 2013-8-20
# Author        : aowj@ucweb.com
# changelog     : modify the cmd ,use CMDExec class;@laijx
###########################################################################################################

from cmdexec import CMDExec

class CleanCache(object):
    """ 用于清除浏览器缓存

    .. tip:: 已经废弃不再更新，建议使用browsermanager进行缓存的清除
    """
    def __init__(self, _browser_pkg, _serial_number):
        """ 构造方法
 
        :param _browser_pkg: 浏览器的包名
        :type _browser_pkg: string

        :param _serial_number: 手机串号
        :type _serial_number: string
        """
        self._browser_pkg = _browser_pkg
        self.serial_number = _serial_number
        self.cmd_exec = CMDExec()    
        self.cmd_exec.setTargetSerial(self.serial_number)  # set first target serialNum
        self.cmd_exec.compatible()  # ensure adb command compatible
    
    def cleanUC(self):
        """ 清除UC浏览器的缓存
        """
        self.cmd_exec.sendShellCommand("rm -r /sdcard/UCDownloads/cache")
        self.cmd_exec.sendShellCommand("rm -r /sdcard/UCDownloads/offline")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/cache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/UCMobile/databases")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/UCMobile/offline")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/UCMobile/userdata/UCProxyCache.db")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/UCMobile/httpCache")

    def cleanFirefox(self):
        """ 清除火狐（Firefox）浏览器的缓存
        """
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/cache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/files")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/app_tmpdir")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/app_plugins")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/app_plugins_private")
    
    def cleanQQ(self):
        """ 清除QQ浏览器的缓存
        """
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/databases")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/cache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/app_appcache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/app_databases")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/files")
    
    def cleanChrome(self):
        """ 清除chrome浏览器的缓存
        """
        # app_chrome,app_textures,cache,databases,files 
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/databases")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/cache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/app_chrome")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/app_textures")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/files")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/app_chrome/Default/Local Storage")
    
    def cleanBaiDu(self):
        """ 清除百度浏览器的缓存
        """
        # app_appcache,app_appcache_sys,app_geolocation,cache,databases,files
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/app_appcache_sys")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/app_databases")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/app_geolocation")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/databases")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/cache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/files")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self._browser_pkg + "/app_appcache")

    def cleanCache(self):
        """ 根据包名进行浏览器缓存的清除
        """
        # if it is UC browser
        if self._browser_pkg.find("com.UCMobile") != -1:
            self.cleanUC()
        # if it is QQ browser
        elif self._browser_pkg.find("com.tencent") != -1:
            self.cleanQQ()
        # if it is chrome
        elif self._browser_pkg.find("com.android.chrome") != -1:
            self.cleanChrome()
        # if it is firefox
        elif self._browser_pkg.find("org.mozilla.firefox") != -1:
            self.cleanFirefox()
        # if it is baidu browser com.baidu.browser.apps + com.baidu.browser.app.BrowserActivity
        elif self._browser_pkg.find("com.baidu") != -1:
            self.cleanBaiDu()
