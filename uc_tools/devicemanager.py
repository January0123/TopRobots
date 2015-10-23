# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.devicemanger
# 
# Creation      : 2013-10-30
# Author        : huangjj@ucweb.com
###########################################################################

from device_manager import netstatemanager, sdcardmanager, deviceinfomanager, powermanager

class DeviceManager(object):
    """ 通过adb命令获取设备相关的网络、电源、sdcard、硬件信息，etc

    下面是一个简单的使用例子::

        from uc_tools.devicemanager import DeviceManager

        device_manager = DeviceManager(serial="123456") 
        net_state_manager = device_manager.getNetStateManger()  # 获取手机网络管类对象
        net_state_manager.wifiEnable()  # 开启手机网络状态
    """
 
 
    def __init__(self,serial=None):
        """ 构造方法
            
        :param serial: 设备串号
        :type serial: string
        """
        #: 设备串号
        self.serial = serial
        
    def getNetStateManager(self):
        """ 获取手机的网络状态管理对象
        """
        return netstatemanager.NetStateManager(self.serial)
    
    def getPowerManager(self):
        """ 获取手机电源管理对象
        """
        return powermanager.PowerManager(self.serial)
    
    def getSDCardManager(self):
        """ 获取设备sdcard的管理对象
        """
        return sdcardmanager.SDCardManager(self.serial)
    
    def getDeviceInfoManager(self):
        """ 获取设备硬件信息管理对象
        """
        return deviceinfomanager.DeviceInfoManager(self.serial)
        
        