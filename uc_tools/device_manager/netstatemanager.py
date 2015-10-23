# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.devicemanger.netstatemanager
# 
# Creation      : 2013-10-30
# Author        : huangjj@ucweb.com
###########################################################################

from uc_tools import cmdexec

class NetStateManager(object):
    """ 封装了手机网络状态的管理类

    .. note:: 当前仅支持 Android 4.0 或者更高版本
    """

    def __init__(self, device=None):
        """ 构造方法

        :param device: 设备串号
        :type device: string
        """
        self.cmd_exec = cmdexec.CMDExec()
        if device:
            self.cmd_exec.setTargetSerial(device)
        self._device = device
    
    def wifiEnable(self):
        """ 开启手机的wifi
        """
        self.cmd_exec.sendShellCommand("svc wifi enable")
        
    def wifiDisable(self):
        """ 关闭手机的wifi
        """
        self.cmd_exec.sendShellCommand("svc wifi disable")
        
    def wifiPrefer(self):
        """ 当 移动网络 和 wifi网络 同时存在时，设置手机优先使用wifi
        """
        self.cmd_exec.sendShellCommand("svc wifi prefer")
        
    def dataEnable(self):
        """ 开启手机的移动网络
        """
        self.cmd_exec.sendShellCommand("svc data enable")
        
    def dataDisable(self):
        """ 关闭手机的移动网络
        """
        self.cmd_exec.sendShellCommand("svc data disable")
        
    def dataPrefer(self):
        """ 当 移动网络 和 wifi网络 同时存在时，设置手机优先使用 移动网络
        """
        self.cmd_exec.sendShellCommand("svc data prefer")
        
    def getWifiIP(self):
        """ 获取手机wifi连接情况下的Ip地址

        :returns: 手机wifi连接情况下的Ip地址
        :rtype: string
        """
        wifi_ip = self.cmd_exec.sendShellCommand('getprop dhcp.wlan0.ipaddress')
        return wifi_ip

    def getMacAddress(self):
        """ 获取设备 mac 地址

        :returns: mac 地址
        :rtype: str
        """
        mac_address = self.cmd_exec \
            .sendShellCommand("cat /sys/class/net/wlan0/address")
        return mac_address.replace("\r\n", "", 1)
        