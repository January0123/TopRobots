# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.browser_manager.ucbrowsermanager
# 
# Creation      : 2013-10-31
# Author        : huangjj@ucweb.com
###########################################################################

from uc_tools.cmdexec import CMDExec
from uc_tools.processmanager import ProcessManager
from uc_tools.pkgmanager import PKGManager
from uc_tools.configreader import ConfigReader
from uc_tools import runcommand
from uc_tools import fileutils
from uc_tools.devicemanager import DeviceManager
import browsermanager
import os
import time
import sys

 
class UCBrowserManager(browsermanager.BrowserManager):
    """ UC 浏览器管理类
    """

    def __init__(self, pkg_name, activity=None, build_date=None, device=None):
        """ 构造方法

        :param pkg_name: 浏览器的包名
        :type pkg_name: string

        :param activity: 浏览器的Activity名
        :type activity: string

        :param build_date: uc浏览器打包流水号
        :type build_date: string

        :param device: 设备串号
        :type device: string
        """
        self.cwd = os.path.split(os.path.realpath(__file__))[0]
        browsermanager.BrowserManager.__init__(self, pkg_name, activity, device)
        self.build_date = build_date
        self.ucflagscopy = UCFlagsCopy(self,
                                  build_date=self.build_date)    
        
    def removeWelcomePage(self):
        """ 移除新手教育界面
        """
        self.ucflagscopy.copyUCFlagFile()
        
    def cleanCache(self):
        """清除浏览器缓存
        """
        self.cmd_exec.sendShellCommand("rm -r /sdcard/UCDownloads/cache")
        self.cmd_exec.sendShellCommand("rm -r /sdcard/UCDownloads/offline")
        self.cmd_exec.sendShellCommand("rm -r /sdcard/UCDownloads/flash")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/UCMobile/databases")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/UCMobile/offline")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/UCMobile/userdata/UCProxyCache.db")

        # clean form
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/UCMobile/userdata/Form")
        # clean cache about page
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/cache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/UCMobile/httpCache")
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/databases")

        # clean cookie
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/UCMobile/Cookie")
        # clean something about html5
        self.cmd_exec.sendShellCommand("rm -r /data/data/" + self.pkg_name + "/UCMobile/localstorage")

    def changeUCSetting(self, setting_dict):
        """ 修改UC浏览器配置

        :param setting_dict: 浏览器的配置项，格式如下： {section:{key, value}}
        :type setting_dict: dict
        """
        setting_file = "setting.dat"
        path = "/data/data/" + self.pkg_name + "/UCMobile/userdata"
        file_path = path +"/" + setting_file
        is_exist = self.cmd_exec.doesFileExist(file_path)

        if not is_exist:
            setting_file = "setting1.dat"
            file_path = path +"/" + setting_file
        m8code_path = self.__getM8codePath()
        print m8code_path
        self.cmd_exec.sendShellCommand("chmod -R 777 /data/data/" + self.pkg_name)

        os.chdir(self.cwd)
        filename = self.device+".dat"
        decode_file = "decode_"+filename
        # print "decode_file : " + decode_file
        # print self.cwd  + os.sep
        self.cmd_exec.pull(file_path, self.cwd + os.sep + filename)
        runcommand.runCommand("python " + m8code_path + " d  "+filename)
        # read the config file and change the setting value
        config = ConfigReader(decode_file).readConfig()

        for section, setting_items in setting_dict.items():
            print section
            for key, value in setting_items.items():
                print key + ":" + value
                config.set(section, key, value)
        config.write(open(decode_file,"w"))
        #remove the temp file and push them into the mobile
        runcommand.runCommand("rm "+filename)
        runcommand.runCommand("python " + m8code_path + " e "+decode_file)
        self.cmd_exec.push("encode_"+decode_file, file_path)
        self.cmd_exec.sendShellCommand("chmod -R 777 /data/data/" + self.pkg_name)
        runcommand.runCommand("rm "+decode_file)
        runcommand.runCommand("rm encode_"+decode_file)
        os.chdir(sys.path[0])

    def hardwareACManager(self, is_open=1):
        """ 打开浏览器硬加速开关

        :param is_open: 是否打开硬加速开关
        :type is_open: int
        """
        # 是否在设置界面设置过AC
        flag_has_change_hwac = "f4058016078ea7c5e7d329cf3a8w41dewqq"
        # 是否开启HWAC
        flag_file_name = "f4c5058b3111e016078ea7e7d329cf3a"

        path = "/data/data/" + self.pkg_name + "/ucflags"
        self.cmd_exec.sendShellCommand("chmod 777 " + path + "/" + flag_file_name)
        
        # 是否在设置界面设置过AC
        self.cmd_exec.sendShellCommand("chmod -R 777 " + path)
        is_exist = self.cmd_exec.doesFileExist(path + "/" + flag_has_change_hwac)

        if not is_exist:
            self.cmd_exec.sendShellCommand("touch " + path + "/" + flag_has_change_hwac)

        # 是否开启HWAC
        if is_open == 1:
            is_exist = self.cmd_exec.doesFileExist(path + "/" + flag_file_name)
            
            if not is_exist:
                self.cmd_exec.sendShellCommand("touch " + path + "/" + flag_file_name)
            self.ucflagscopy.changeFileOwner()
        else:
            is_exist = self.cmd_exec.doesFileExist(path + "/" + flag_file_name)

            if is_exist:
                self.cmd_exec.sendShellCommand("rm " + path + "/" + flag_file_name)

        


    def __getM8codePath(self): 
        """ 获取M8加解密的路径
        """
        path = fileutils.getUCToolsLocation()
        m8code_path = path + os.sep + "m8code.py"
        print m8code_path
        return m8code_path

    
class UCFlagsCopy(object):
    """ 进行UC浏览器新手界面的移除
    """
    
    def __init__(self, browser_manager, build_date=None):
        """ 构造方法

        :param pkg_name: 浏览器的包名
        :type pkg_name: string

        :param device: 设备串号
        :type device: string

        :param build_date: 浏览器的打包流水号
        :type build_date: string
        """
        self.browser_manager = browser_manager
        self.__pkg_name = browser_manager.pkg_name 
        # self.__activity = browser_manager.activity   
        self.__device = browser_manager.device

        self.__need_start_activity = True
        self.__last_ver = build_date
        self.cmd_exec = browser_manager.cmd_exec
        
    def __copyFileToStorage(self):
        """ 复制标记文件到手机中
        """
        change_file_mod_cmd = "chmod -R 777 /data/data/" + self.__pkg_name
        self.cmd_exec.sendShellCommand(change_file_mod_cmd)
        src = "./ucflags"
        dest = "/data/data/"+ self.__pkg_name
        self.cmd_exec.push(src, dest)

        src = "/data/data/" + self.__pkg_name + "/ucflags"
        is_success = self.cmd_exec.doesFileExist(src)
        
        if(is_success):
            self.cmd_exec.sendShellCommand(change_file_mod_cmd)
            return is_success
        else:
            return is_success


    def changeFileOwner(self):
        """ 修改标志文件的所属用户
        """
        path = "/data/data/" + self.__pkg_name
        ls_cmd = "ls -l " + path + "/UCMobile/userdata/history.ini"
        result = self.cmd_exec.sendShellCommand(ls_cmd)
        result_infos = result.split()
        owner = result_infos[1]

        # change
        change_mod_cmd = "chown " + owner + ":" + owner + " "
        start_flag_cmd = change_mod_cmd + path + "/StartedFlagFile" 
        last_ver_cmd = change_mod_cmd + path + "/lastVer"
        self.cmd_exec.sendShellCommand(start_flag_cmd)
        self.cmd_exec.sendShellCommand(last_ver_cmd)

        # change the owner and group of the file
        ucflags_list_result = self.cmd_exec.sendShellCommand("ls " + path + "/ucflags")
        ucflags_list = ucflags_list_result.split("\r\n")

        for ucflags in ucflags_list:
            flags_cmd = change_mod_cmd + path + "/ucflags/" + ucflags
            self.cmd_exec.sendShellCommand(flags_cmd)
    
    def copyUCFlagFile(self):
        """ 创建并且复制标志文件到手机中
        """
        if not self.__last_ver:
            self.browser_manager.startActivity()
            time.sleep(5)
            # get screen size and click to exit the education-page for pad
            device_info_manager = DeviceManager(self.__device).getDeviceInfoManager()
            win_size = device_info_manager.getWindowSize()
            width = int(int(win_size[0]) * 0.73)
            height = int(int(win_size[1]) * 0.78)
            self.cmd_exec.sendShellCommand("input tap %s %s" % (width, height))
            time.sleep(2)
            query_lastver_cmd = "cat /data/data/" + self.__pkg_name +"/lastVer"
            self.__last_ver = self.cmd_exec.sendShellCommand(query_lastver_cmd)
        else:
            self.__need_start_activity =  False

        create = UCFlagsCreate(self.__last_ver)
        create.createAllUCFlags()
        is_success = self.__copyFileToStorage()

        if self.__need_start_activity :
            self.browser_manager.killPid()
        self.changeFileOwner()
        return is_success

    def getLastVer(self):
        """ 获取UC浏览器打包流水号
        """
        return self.__last_ver
    
class UCFlagsCreate :
    """ UC浏览器新手界面标志文件的创建
    """

    def __init__(self, build=None):
        """ 构造方法

        :param build: 浏览器APK打包流水号
        :type build: string
        """
        self.__build_date = build
    
    
    def __createRootFile(self):
        """ 创建用于存放UC浏览器标志文件的目录
        """
        path = './ucflags'
        exist = os.path.exists(path)
        
        if(not exist) :
            os.makedirs(path)


    def __createStartedFlags(self):
        """ 创建UC浏览器标志文件
        """
        startedFilePath = "./ucflags/StartedFlagFile"
        startedFileExist = os.path.exists(startedFilePath)
        
        if(not startedFileExist) :
            f=open(startedFilePath, "w")
            f.close()

        #create or overwrite lastVer  
        if self.__build_date != None :
            lastVerFilePath="./ucflags/lastVer"
            f = open(lastVerFilePath, "w")
            f.write(str(self.__build_date))
            f.close()
        
    def __createUCFlags(self):
        """ 创建UC浏览器标志文件
        """
        __array = ["0E096B97155C31EEFCCE603C55B00DE8",  #add because of the version 9.2
                   "316124FE28ACAB5BB39D04A63981A3F5",
                   "5A1AAA4199E5FE1DE1DAFF346BFACE13",
                   "6B5952CE1D3338AE1CF832C8FDFDEA75",
                   "97C9E90F260438961B830448F5945D39",
                   "B145796D298BF0653682FA2D3109EF7B",
                   "E22B69B8916227BEB262B29C0458F581",
                   "E55D880ADDA31547F994DF4D05F21CF7",
                   "F6583C12299E85D4C9E9B6650DE7A6BD",
                   "1624333369FA459C97C33B8550CFDA3D",  #add because of the version 9.3
                   "212C982D31A0AE9D56B4489CEBD32464",
                   "F56B56A4027BD5AADA5B9474B6F792E8",
                   "flag_addon_clipboard_enabled"
                   "7CA8650BAD6327DA1D068C8AFDEA0088", # add because of the version 9.4
                   "800722D4B130F1A898BE5773097027AE",
                   "C49C83EB60BC52E7FEF67D702E7DBD2D",
                   "F87087627D1935D04F3ECAD6379C010F",
                   "c65e05bd699d150affd3ab7daa40ef87", # add because of the version 9.6
                   "f4c5058b3111e016078ea7e7d329cf3a"]
        path = "./ucflags/ucflags"
        exist = os.path.exists(path)
        
        # check if the folder which in path, if not, create it
        if(not exist) :
            os.makedirs(path)
            
        #check whether the file in the array is exists, if they don't exists, create them.
        for filename in __array:
            filePath = path + "/" + filename
            ex = os.path.exists(filePath)

            if(not ex):
                f=open(filePath, "w")
                f.close()
    
    
    def createAllUCFlags(self):
        """ 调用前面的方法进行标志文件的创建
        """
        self.__createRootFile()
        self.__createStartedFlags()
        self.__createUCFlags()
