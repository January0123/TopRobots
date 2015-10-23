# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.device_manager.deviceinfomanager
# 
# Creation      : 2013-10-30
# Author        : huangjj@ucweb.com
###########################################################################

import re

from uc_tools import cmdexec

class DeviceInfoManager(object):
    """ 手机信息管理，可以帮助获取手机品牌，型号，系统信息等等
    """


    def __init__(self, device=None):
        """ 构造方法

        :param device: 手机串号
        :type device: string
        """
        self.cmd_exec = cmdexec.CMDExec()
        if device:
            self.cmd_exec.setTargetSerial(device)
        self._device = device
        
    def getBuildId(self):
        """ 获取手机Build ID  (e.g. JZO54K)

        :returns: 手机Build ID 
        :rtype: string
        """
        build_id =  self.cmd_exec.sendShellCommand('getprop ro.build.id')
        assert build_id
        return build_id
    
    def getBuildType(self):
        """ 获取手机BuildType (e.g. mione_plus).

        :returns: 手机BuildType  
        :rtype: string
        """
        build_type = self.cmd_exec.sendShellCommand('getprop ro.build.type')
        assert build_type
        return build_type
    
    def getBuildProduct(self):
        """ 获取手机型号 (e.g. mione_plus).

        :returns: 手机型号  
        :rtype: string
        """
        build_product = self.cmd_exec \
            .sendShellCommand('getprop ro.build.product')
        assert build_product
        return build_product
    
    def getProductName(self):
        """ 获取手机产品名字(e.g. mione_plus)

        :returns: 手机产品名字  
        :rtype: string
        """
#         name = self.cmd_exec.sendShellCommand('getprop ro.product.name')[0]
        name = self.cmd_exec.sendShellCommand('getprop ro.product.name')
        assert name
        return name
    
    def getBuildFingerprint(self):
        """ 获取手机Fingerprint
        (e.g. Xiaomi/mione_plus/mione_plus:4.1.2/JZO54K/3.10.11:user/release-keys)

        :returns: 手机Fingerprint  
        :rtype: string
        """
        build_fingerprint = self.cmd_exec \
            .sendShellCommand('getprop ro.build.fingerprint').replace("\r\n", "")
        assert build_fingerprint
        return build_fingerprint
    
    def getDescription(self):
        """ 获取设备描述（eg:"mione_plus-user 4.1.2 JZO54K 3.10.11 release-keys"）

        :returns: 设备描述
        :rtype: string
        """
        description = self.cmd_exec \
            .sendShellCommand('getprop ro.build.description')
        assert description
        return description

    def getProductBrand(self):
        """ 获取手机品牌
        """
        brand = self.cmd_exec.sendShellCommand("getprop ro.product.brand").replace("\r\n", "")
        assert brand
        return brand
    
    def getProductModel(self):
        """ 获取手机型号(e.g. "Galaxy Nexus") 

        :returns: 手机型号
        :rtype: string
        """
        model = self.cmd_exec.sendShellCommand('getprop ro.product.model').replace("\r\n", "")
        assert model
        return model
    
    def getSubscriberInfo(self):
        """ 获取手机Subscriber Info  (e.g. GSM and device ID)

        :returns: 手机Subscriber Info
        :rtype: string
        """
        iphone_sub = self.cmd_exec.sendShellCommand('dumpsys iphonesubinfo')
        assert iphone_sub
        return iphone_sub
    
    def getBatteryInfo(self):
        """ 获取电池信息(e.g. status, level, etc)

        :returns: 电池信息
        :rtype: string
        """
        battery = self.cmd_exec.sendShellCommand('dumpsys battery')
        assert battery
        return battery
    
    def getSetupWizardStatus(self):
        """ 获取 SetupWizard 状态 (e.g. DISABLED)

        :returns:  setup wizard状态
        :rtype: string
        """
        status = self.cmd_exec.sendShellCommand('getprop ro.setupwizard.mode')
        assert status
        return status

    def getOSVersion(self):
        """ 获取Android系统版本
        """
        os_version = self.cmd_exec \
            .sendShellCommand("getprop ro.build.version.release").replace("\r\n", "")
        assert os_version
        return os_version

    def getWindowSize(self):
        """ 获取手机分辨率

        :returns:  手机分辨率。eg：[1080,1920]
        :rtype: 元组
        """
        cmd = "dumpsys window"
        result = self.cmd_exec.sendShellCommand(cmd)
        regex = r"init=\d*\w\d*"
        pattern = re.compile(regex)
        match = pattern.search(result)

        if match:
            window_size = match.group()
            window_size = window_size.replace("init=", "").split("x")
            return window_size
        return None
        
    def getImeiNumber(self):
        """ 获取设备Imei号

        :returns: 设备Imei号
        :rtype: str
        """
        imei_number = ""

        cmd = "dumpsys iphonesubinfo"
        result = self.cmd_exec.sendShellCommand(cmd)
        result_lines = result.split("\r\n")

        for result_line in result_lines:
            if "Device ID".upper() in result_line.upper():
                imei_number = result_line.split("=")[1].strip()

        if imei_number == "null" or imei_number == "":
            imei_number = "--"
        return imei_number

    def getTotalMemory(self):
        """ 获取设备总内存大小

        :returns: 设备总内存大小
        :rtype:
        """
        cmd = "cat /proc/meminfo"
        result = self.cmd_exec.sendShellCommand(cmd)

        total_meminfo = result.split("\r\n")[0]

        regex = r"\d+"
        pattern = re.compile(regex)
        match = pattern.search(total_meminfo)

        if match:
            total_meminfo = match.group()
            return total_meminfo
        return None

    def getDeviceInfo(self):
        """ 获取设备信息

        :returns: 设备信息
        :rtype: dict
        """
        device_info = {
            "phone_brand" : self.getProductBrand(),
            "phone_model" : self.getProductModel(),
            "phone_os" : "Android",
            "os_version" : self.getOSVersion(),
            "win_size" : self.getWindowSize(),
            "imei" : self.getImeiNumber(),
            "finger_print" : self.getBuildFingerprint(),
            "ram" : self.getTotalMemory(),
            "serial_number": self.cmd_exec.getSerialNumber()
        }
        return device_info

