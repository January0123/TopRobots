# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.pkgmanager
# 
# Creation      : 2013-10-31
# Author        : huangjj@ucweb.com
###########################################################################

import os
import re
import platform

import errors
import cmdexec
import fileutils
import processmanager
import runcommand

class PKGManager(object):
    """ 包管理对象，可以帮助我们安装、启动、卸载、关闭APP等操作
    """

    def __init__(self, pkg_name=None, activity=None, device=None):
        """构造方法

        :param pkg_name: APP的包名, 建议在初始化的时候就配置好
        :type pkg_name: string

        :param activity: Activity的名字，建议在初始化的时候就配置好，因为在启动APP的时候有使用到
        :type activity: string

        :param device: 手机串号，在PC连接有多手机的时候，必须设置
        :type device：string
        """
        #: 进程管理对象
        self.process_manager = processmanager.ProcessManager(device)
        #: 用于执行手机命令
        self.cmd_exec = cmdexec.CMDExec()
        if device:
            self.cmd_exec.setTargetSerial(device)
        self.device = device
        #: 包名
        self.pkg_name = pkg_name
        #: activity 名
        self.activity = activity
        
    def setPKGName(self, pkg_name):
        """ 修改包名

        :param pkg_name: APP的包名
        :type pkg_name: string
        """
        self.pkg_name = pkg_name
        
    def setActivity(self, activity):
        """修改包名

        :param activity: APP的activity名
        :type activity: string
        """
        self.activity = activity
        
    def install(self, package_file_path, reinstall=False, timeout_time=4 * 60):
        """ 安装指定的包到指定的安卓设备中,如果 ``pkg_name`` 不为 ``None`` 安装之后会校验是否安装成功。
        如果安装失败，将会进行异常处理并且重新安装3次。

        :param package_file_path: 安装包的路径
        :type package_file_path: string

        :param reinstall: 是否是覆盖安装，默认为 ``False``
        :type reinstall: bool

        :param timeout_time: 安装超时时间,默认为240s
        :param timeout_time: int

        :returns: (是否安装成功, 安装状态输出)
        :rtype: tuple(bool, string)
        """
        install_cmd = ['install']
    
        if reinstall:
            install_cmd.append('-r')
    
        install_cmd.append(package_file_path)
        install_cmd = ' '.join(install_cmd)

        is_install_success = False
        reinstall_time = 1
        result = ""
        while (not is_install_success) and (reinstall_time < 4):
            temp = self.cmd_exec.sendCommand(install_cmd,
                                     timeout_time=timeout_time,
                                     retry_count=0)
            result = result + "The " + str(reinstall_time) + " time to install the apk : \n" + temp + "\n"
            if not self.pkg_name:
                return result
            is_install_success = self.__verifyInstall(temp)

            reinstall_time = reinstall_time + 1
        return (is_install_success, result)

    def __verifyInstall(self, result):
        """ 安装校验

        :param result: 安装结果
        :type result: string

        :returns: 是否安装成功
        :rtype: bool
        """
        try :
            if "success".upper() in result.upper():
                return True
            else:
                self.__removeLeftPkg()
                return False 
        except Exception, e:
            print "Exception in preliminary : " + str(e)
            return False

    def uninstall(self,timeout_time=60):
        """ 卸载APP

        :param timeout_time: 超时时间,默认60s
        :type timeout_time: int
        """
        assert self.pkg_name
        cmd = "uninstall " + self.pkg_name
        self.cmd_exec.sendCommand(cmd, timeout_time=timeout_time)

        if not self.pkg_name: 
            self.__removeLeftPkg()

    def __removeLeftPkg(self, dir_path="/data/data/"):
        """ 删除卸载过后的残余文件

        :param dir_path:包的路径
        :type dir_path: string
        """
        path = dir_path + self.pkg_name

        if self.cmd_exec.doesFileExist(path):
            self.cmd_exec.sendShellCommand("rm -r " + path)

    
    def disablePackage(self):
        """ 使用 ``pm disable`` 命令禁用APP
        """
        assert self.activity
        cmd = "pm disable " + self.pkg_name + "/" + self.activity
        self.cmd_exec.sendShellCommand(cmd)
        
    def enablePackage(self):
        """ 使用 ``pm enable`` 命令取消APP的禁用状态
        """
        assert self.activity
        cmd = "pm enable " + self.pkg_name + "/" + self.activity
        self.cmd_exec.sendShellCommand(cmd)  
        
    def getPid(self):
        '''获取当前APP的PID

        :returns: 返回APP 对应的进程PID
        :rtype: int
        '''
        assert self.pkg_name
        return self.process_manager.getPid(self.pkg_name)
    
    def killPid(self, signum=9):
        """ 获取APP进程PID并且杀掉进程

        :param signum: kill命令信号量，默认为9
        :type signum: int
        """
        i = 3
        pid = self.getPid()
        while (i > 0) and  (pid != ''):
            self.process_manager.killPid(pid, signum)
            pid = self.getPid()
            i = i - 1


        
    def _getActivityCommand(self,
                            package,
                            activity, 
                            wait_for_completion,
                            action,
                            category,
                            data,
                            extras,
                            trace_file_name,
                            force_stop,
                            flags):
        """ 拼接APP启动命令

        :param wait_for_completion:  是否等待启动完成, 默认为False
        :type wait_for_completion: bool

        :param action: 默认是 ``android.intent.action.VIEW``
        :type action: string

        :param category: (e.g. "android.intent.category.HOME")
        :type category: string 

        :param data: 需要传送给activity中的数据
        :type data: string

        :param extras: 需要传递给activity的额外参数
        :type extras: dict

        :param trace_file_name: 启动分析器并且存储相应的结果到指定文件中
        :type trace_file_name:  string

        :param force_stop: 决定着在启动APP之前是否先终止之前的activity，默认为False
        :type force_stop: bool

        :param flags: 给intent添加标记,默认为None

        :returns: 启动返回的结果
        """
        cmd = 'am start -a %s' % action
        if force_stop:
            cmd += ' -S'
        if wait_for_completion:
            cmd += ' -W'
        if category:
            cmd += ' -c %s' % category
        if package and activity:
            cmd += ' -n %s/%s' % (package, activity)
        if data:
            cmd += " -d '%s'" % data
            
        if extras:
            for key in extras:
                value = extras[key]
                if isinstance(value, str):
                    cmd += ' --es'
                elif isinstance(value, bool):
                    cmd += ' --ez'
                elif isinstance(value, int):
                    cmd += ' --ei'
                cmd += ' %s %s' % (key, value)
        if trace_file_name:
            cmd += ' --start-profiler ' + trace_file_name
        if flags:
            cmd += ' -f %s' % flags
        return cmd 
    
    def startActivity(self,
                      wait_for_completion=False,
                      action='android.intent.action.VIEW',
                      category=None,
                      data=None,
                      extras=None,
                      trace_file_name=None,
                      force_stop=False,
                      flags=None):
        """ 启动APP

        :param wait_for_completion:  是否等待启动完成,False
        :type wait_for_completion: bool

        :param action: 默认是 ``android.intent.action.VIEW``
        :type action: string

        :param category: (e.g. "android.intent.category.HOME")
        :type category: string 

        :param data: 需要传送给activity中的数据
        :type data: string

        :param extras: 需要传递给activity的额外参数
        :type extras: dict

        :param trace_file_name: 启动分析器并且存储相应的结果到指定文件中
        :type trace_file_name:  string

        :param force_stop: 决定着在启动APP之前是否先终止之前的activity，默认为False
        :type force_stop: bool

        :param flags: 给intent添加标记,默认为None

        :return: 启动返回的结果
        """
        if not self.activity:
            raise errors.MsgException("Activity of PKGManager( %s ) can not be None" % self.pkg_name)
        
        cmd = self._getActivityCommand(self.pkg_name, self.activity, wait_for_completion,
                                       action, category, data, extras,
                                       trace_file_name, force_stop, flags)
        return self.cmd_exec.sendShellCommand(cmd)   
        
    def goHome(self):
        """ 让设备返回主页，这个方法是阻塞的。
        """ 
        self.cmd_exec.sendShellCommand('am start -W -a android.intent.action.MAIN -c android.intent.category.HOME')
        
    def getApplicationPath(self):
        """ 获取已经安装了的APK的路径

        :returns: 如果APP已经安装了，返回APP所在的路径，否则返回None
        :rtype: string 或者 None
        """
        pm_path_output = self.cmd_exec.sendShellCommand('pm path ' + self.pkg_name)
        # The path output contains anything if and only if the package
        # exists.
        if pm_path_output:
            # pm_path_output is of the form: "package:/path/to/foo.apk"
            return pm_path_output[0].split(':')[1]
        else:
            return None
        
    def clearApplicationState(self):
        """ 使用命令 ``pm clear`` 关闭并且APP的所有状态值
        """
        # Check that the package exists before clearing it. Necessary because
        # calling pm clear on a package that doesn't exist may never return.
        pm_path_output  = self.cmd_exec.sendShellCommand('pm path ' + self.pkg_name)
        # The path output only contains anything if and only if the package exists.
        if pm_path_output:
            self.cmd_exec.sendShellCommand('pm clear ' + self.pkg_name)
        
    def getPKGList(self):
        """ 获取手机已经安装有的所有APP

        :returns: 手机已经安装了的APP的包名列表
        :rtype: list
        """                    
        pkg_list = self.cmd_exec.sendShellCommand("ls /data/data")
        return pkg_list.split("\r\n")

def getApkInfo(apk_path):
    r""" 获取APK的信息（apk_size, versioncode, versionname, packagename, launchActivity）,
    其中APK的大小以MB为单位

    :param apk_path: apk包所在的路径
    :type apk_path: string

    :returns: 返回APK信息，格式如下: 
            {'versioncode': 'xxx', 'launchActivity': 'xxx',
                'packagename': 'xxx', 'versionname': 'xxx', 'app_size': 'xxx'}
    :rtype: dict
    """
    system = platform.system()
    tools_location = fileutils.getUCToolsLocation()
    aapt_path = fileutils.createPath([tools_location, "uc_tools","resource","aapt"])

    if system.upper() == "Windows".upper():
        aapt_path = fileutils.createPath([aapt_path, "aapt_windows.exe"])
    else:
        aapt_path = fileutils.createPath([aapt_path, "aapt_linux"])

    apk_info_list = {}
    cmd_aapt = aapt_path + " d badging "+ apk_path
    # cmd_aapt = r"F:\git\qmsinterceptor\resource\aapt\aapt_windows d badging "+ apk_path
    out = runcommand.runCommand(cmd_aapt)
    rs = out
    pkg = re.match('package: ' ,rs)
 
    apk_info = pkg.string.split('\n')
    reg = re.compile(r"'.+'")
    package = reg.findall(apk_info[0].split()[1])[0].strip('\'')
    versioncode = reg.findall(apk_info[0].split()[2])[0].strip('\'')
    versionname = reg.findall(apk_info[0].split()[3])[0].strip('\'')
    
    for i in range(len(apk_info)):
        if ("launchable-activity" in apk_info[i]):
            launchActivity = reg.findall(apk_info[i].split()[1])[0].strip('\'')
    
    apk_path = apk_path.replace("\\(","(").replace("\\)",")")

    app_size = os.path.getsize(apk_path)
    app_size = str(app_size/(1024.0*1000))

    apk_info_list["apk_size"] = app_size
    apk_info_list["versioncode"] = versioncode
    apk_info_list["versionname"] = versionname
    apk_info_list["packagename"] = package
    apk_info_list["launchActivity"] = launchActivity
    return apk_info_list
        