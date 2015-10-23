# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2014 UC Mobile Limited. All Rights Reserved
# File     : runtest
# 
# Creation : 2014-7-16
# Author   : yelq@ucweb.com
###########################################################################

# System imports
from uc_tools import runcommand
from uc_tools.configreader import ConfigReader
from uc_tools.cmdexec import CMDExec
from uc_tools.task import image_diff
from shutil import copy
from uc_log4py.logger import LogFactory
import os
import time

#platform
plat = os.name

class RunTest(object):
    
    def __init__(self,result_log,serial=None,config =ConfigReader("config.cfg")):
        #: 设备串号
        self.serial = serial
        self.cmdexec =  CMDExec(self.serial)
        if(self.serial==None):
            self.adb_cmd = "adb"
        else:
            self.adb_cmd = "adb -s " + self.serial
        self.enable_u3 = config.getValue("config","enable_u3")
        self.diff_value =  config.getValue("config","diff_value")
        pkgName_ = config.getValue("config","pkg_")
        self.pkgs_ = pkgName_.split(",")
        self.server_addr = config.getValue("config","server_addr")
        self.dir = os.getcwd()
        log_factory = LogFactory(result_log,log_config_url="uc_log4py/log4py.cfg")
        self.__logger = log_factory.getLogger("RunTest")
        self.runUrl = ""
        self.runTime = ""

        if plat=="posix":
            self.pic_path =  os.path.join(self.dir,'client/pics/')
        elif plat == "nt":
            self.pic_path =  os.path.join(self.dir,'client\\pics\\')
        self.result_url =  config.getValue("config","result_url")
        
    def getLogger(self):
        return self.__logger
        
    def pullPic(self,pkg_):
#         self.__logger.debug("debug for pull pic")
#         self.__logger.info("info for pull pic")
#         self.__logger.warn("warn for pull pic")
#         self.__logger.error("error for pull pic ")
        picFile = ""
        #u3 特有的截图方法
        if(self.enable_u3 == "1"):
            print "u3 get pic,picFile=",pkg_
            try:
            #pull 图片
                self.cmdexec.pull("/sdcard/UCDownloads/PageShot/","./client/old/")
                #删除手机上的图片
                self.cmdexec.sendShellCommand("  rm -r /sdcard/UCDownloads/PageShot/")
                #创建原文件夹
                self.cmdexec.sendShellCommand("  mkdir /sdcard/UCDownloads/PageShot")
                picFile = self.getAndReName(pkg_)
                if(picFile == ""):
                    #DEL
                    print "picFile is None,pkg_ = ",pkg_
                    #del_pics = 'del /Q "'+self.pic_path+'"'
                    #os.system(del_pics)
                    self.__logger.info("Pic is None, RunUrlTest Again ")
                    self.runUrlTest(self.runTime, self.runUrl)
                
            except:
                print "get pic error"
                #获取不到图片再次测试
                self.__logger.error("********get pic error********")
                self.__logger.info("RunUrlTest Again ")
                #del_pics = 'del /Q "'+self.pic_path+'"'
                #os.system(del_pics)
                self.runUrlTest(self.runTime, self.runUrl)
                
            finally:
                return picFile
        else:
            #使用非U3内核的浏览器截图功能的代码
            print u"请实现代码"
        return PicFile
                
            
    def getAndReName(self,pkg_):
        if plat == "posix":
            old_path = os.path.join(self.dir,'client/old/')
        elif plat == "nt":
            old_path = os.path.join(self.dir,'client\\old\\')
        files = os.listdir(old_path)
        newFile = ""
        for f in files:
            newFile =os.path.join(self.pic_path, f)
            nowFile = os.path.join(old_path,f)
            #os.rename(nowFile, newFile)
            copy(nowFile, newFile)
            #DEL
            if plat == "posix":
                del_pics = 'rm -rf  ' +old_path+ '*.*'
            elif plat == "nt":
                del_pics = 'del /Q "'+self.pic_path+'"'
            os.system(del_pics)   
        return newFile
    
    def imageDiff(self,p1,p2):
        diff_value = 0.01
        try:
            diff  = image_diff (p1,p2)
            diff_value = diff.compareimage()
        except:
            print "image diff error"
        finally:
            return diff_value
        
    def diffResult(self,pics):
        re = ""
        if (len(pics)==2):
            if(pics[0]!="" and pics[1]!=""):
                print "image diff"
                diff = self.imageDiff(pics[0],pics[1])
                diff_value = float(self.diff_value)
                print "diff = ",diff
                print "diff_value = ",diff_value
                if diff < diff_value :
                    re = "p1 & p2 are different , diffValue = "+str(diff)
                    #upload
                    nohttp_url = self.runUrl.split("/")[2]
                    print "nohttp_url = ",nohttp_url
                    print upload_dir
                    os.system("python client/upload.py "+ upload_dir + " "+ nohttp_url)
                else :
                    re = "p1 & p2 are same , diffValue = "+str(diff)
                    #DEL
                    #del_pics = 'del /Q "'+self.pic_path+'"'
                    #os.system(del_pics)
            else:
                re = "error:p1 or p2  is None"
        else:
            re =  "error:p1 or p2  is None,pics len = "+str(len(pics))
        return re
        
    def runUrlTest(self,t,url):
        pics = []
        i = 1
        for p in self.pkgs_:
            pic = ""
            #pkgName = "com.UCMobile."+p
            pkgName=p
            if "UCMobile" in p:
                cmd_url =  ' am start -a android.intent.action.VIEW -n ' + pkgName + '/com.UCMobile.main.UCMobile -d \"' + url + '"'
            elif "chrome" in p:
                cmd_url =  ' am start -a android.intent.action.VIEW -n ' + pkgName + '/com.google.android.apps.chrome.Main -d \"' + url + '"'
            elif "tensent" in p:
                cmd_url =  ' am start -a android.intent.action.VIEW -n ' + pkgName + '/com.tencent.mtt.SplashActivity -d \"' + url + '"'
            print "Pkg"+str(i)+" "+cmd_url
            i = i + 1
            self.cmdexec.sendShellCommand(cmd_url)
            time.sleep(5)
            self.cmdexec.sendShellCommand(cmd_url)
            time.sleep(5)
            #截屏
            name=url.split("/")[-1]
            cmd_screen= '/system/bin/screencap -p /sdcard/UCDownloads/pageShot/' + name+"_"+pkgName+"_1.png"
            print cmd_screen
            self.cmdexec.sendShellCommand(cmd_screen)
            time.sleep(t)
            if "UCMobile" in p:
                kill_pkg ='am start -n' + pkgName +'/com.UCMobile.main.UCMobile -e click quit'
            else:
                kill_pkg = " am force-stop " + pkgName
            self.cmdexec.sendShellCommand(kill_pkg)
            pic = self.pullPic(p)
            pics.append(pic)
        return pics
        
    
    def handleProcess(self,upload_dir,url_list = os.path.join(os.getcwd(),"urls.txt")):
        
        #删除手机上的图片
        self.cmdexec.sendShellCommand("  rm -r /sdcard/UCDownloads/PageShot/")
        #创建原文件夹
        self.cmdexec.sendShellCommand("  mkdir /sdcard/UCDownloads/PageShot")
        #DEL
        #del_pics = 'del /Q "'+self.pic_path+'"'
        #os.system(del_pics)
        
        pics = []
        result = ""
        
        ofile = open(url_list,'r')
        for line in ofile:
            urls = line.strip('\n')
            urls = urls.strip('\r')
            url = urls.split()[0]
            print urls
            print url
            t = int(urls.split()[1])
            self.runTime = t
            self.runUrl = url
            self.__logger.info("RunTest URL = "+self.runUrl+" Runtime = "+str(self.runTime))
            pics = self.runUrlTest(t, self.runUrl)
            for p1 in pics:
                print "pics===================" ,p1
            #if (len(pics)==2 and pics[0]!="" and pics[1]!=""):
            #    result = self.diffResult(pics)
            #    self.__logger.info("RunTest Result = "+result)
            #else:
                #失败再来一次
                #DEL
                #del_pics = 'del /Q "'+self.pic_path+'"'
                #os.system(del_pics)
                #self.__logger.info("RunTest pics[]!=2 or pics is none  Run Again")
                #pics = self.runUrlTest(t, self.runUrl)
                #result = self.diffResult(pics)
               # self.__logger.info("RunTest Result = "+result)
                
            self.__logger.info("=================================================================================")
                
        ofile.close()
        
        
if __name__ == '__main__':
    #device id
    date_str = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()));
    upload_dir = date_str
    log_path  = "./logs/"+upload_dir+".log"
    run = RunTest(log_path)
    logger = run.getLogger()
    logger.info("RunTest Result URL = "+run.result_url+"?re="+upload_dir)
    #服务器上的文件夹名称
    print run.result_url+"?re="+upload_dir
    run.handleProcess(upload_dir)
