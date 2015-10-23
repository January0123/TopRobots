# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.browser_manager.ucbrowsermanager
# 
# Creation      : 2013-10-31
# Author        : huangjj@ucweb.com
###########################################################################

import os
import time
import browsermanager
from uc_tools.cmdexec import CMDExec
from uc_tools import fileutils
from uc_tools.pkgmanager import PKGManager

class ChromeBrowserManager(browsermanager.BrowserManager):
    """ Chrome浏览器管理类，封装了启动浏览器、加载URL，关闭浏览器等方法
    """


    def __init__(self, pkg_name, activity="com.google.android.apps.chrome.Main", device=None):
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
        ChromeRemoveWelPage(self).removeWelcomePage()
        
    def cleanCache(self):
        """清除浏览器缓存
        """
        # app_chrome,app_textures,cache,databases,files 
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/databases")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/cache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/app_chrome")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/app_textures")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/files")
        
class ChromeRemoveWelPage(object):
    """ Chrome浏览器新手界面的移除
    """

    def __init__(self, browser_manager):
        """ 构造方法

        :param browser_manager: 浏览器管理类
        :type browser_manager: ChromeBrowserManager
        """
        self.pkg_name = browser_manager.pkg_name
        self.browser_manager = browser_manager
        self.cmd_exec = browser_manager.cmd_exec

    def removeWelcomePage(self):
        """ 进行chrome浏览器的新手界面的跳过
        """
        # the information about file used for flag
        file_name = "com.android.chrome_preferences.xml"
        flag_path = "/data/data/%s/shared_prefs/%s" % (self.pkg_name, file_name)

        # target_path = fileutils.getUCToolsLocation()
        folders = ["./", "temp", "tools"]
        target_path = fileutils.createPath(folders)
       
        # create the folder to save the flag-file
        fileutils.createFolder(target_path)

        self.browser_manager.startActivity(wait_for_completion=True)
        time.sleep(5)
        # pull the file which has the flag for welcome page
        self.cmd_exec.sendShellCommand("chmod 777 %s" %  (flag_path))
        self.cmd_exec.pull(flag_path, target_path)

        # change the flag-content to remove welcome page for chrome
        file_path = target_path + "/" + file_name
    
        self.__insertFlag(file_path)

        # push the file which has the flag for removing welcome page
        self.cmd_exec.push(file_path, flag_path)
        self.browser_manager.killPid()
        time.sleep(5)
        self.browser_manager.killPid()
        # delete the file
        fileutils.delete(file_path)

    def __insertFlag(self,file_path):
        """ 插入非首次启动的标记

        :param file_path: 标志文件所在的路径
        :type file_path: string
        """
        content = "<boolean name=\"first_run_flow\" value=\"true\"/>\n</map>"
        # use the 'w' mode to rewrite the content
        file_handler = open(file_path,"r+")
        file_content = file_handler.read()
        file_content = file_content.replace("</map>",content)
        # change the offset to the begin of content
        file_handler.seek(0,0)
        file_handler.write(file_content)
        file_handler.close()


        