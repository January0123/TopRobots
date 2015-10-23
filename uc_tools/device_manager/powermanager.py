# -*- coding: utf-8 -*-

##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.device_manager.powermanager
# 
# Creation      : 2013-10-30
# Author        : huangjj@ucweb.com
###########################################################################

from uc_tools import cmdexec
import time
import sdcardmanager

class PowerManager(object):
    """ 手机的电源管理器
    """

    def __init__(self, device=None):
        """ 构造方法

        :param device: 设备串号
        :type device: string
        """
        self.sdcard_manager = sdcardmanager.SDCardManager(device)
        self.cmd_exec = cmdexec.CMDExec()
        if device:
            self.cmd_exec.setTargetSerial(device)
        self._device = device
        
        
    def powerStayOn(self, state="true"):
        """ 设置手机保持唤醒的状态

        :param state: 手机保持唤醒的状态
        :type state: string

        手机state的状态参数是有类型限制的，当前有以下四种类型::

            true  : always keep awake 
            false : don't keep awake
            usb   : only keep awake while the usb connect
            ac    : only keep awake while the ac

        """
        svc_cmd = "svc power stayon %s" % (state)
        self.cmd_exec.sendShellCommand(svc_cmd)
        
    def reboot(self, full_reboot=True):
        """ 设备重启

        :param full_reboot: 是否完全重启，如果值为 ``True`` ,将会执行 ``reboot`` 命令，否则直接执行重启shell
        :type full_reboot: bool
        """
        # TODO(torne): hive can't reboot the device either way without breaking the
        # connection; work out if we can handle this better
    
        if full_reboot or not self.isRootEnabled():
            self.cmd_exec.sendCommand('reboot')
            timeout = 300
            retries = 1
            # Wait for the device to disappear.
            while retries < 10 and self.cmd_exec.isOnline():
                time.sleep(1)
                retries += 1
        else:
            self.cmd_exec.restartShell()
            timeout = 120
        # To run tests we need at least the package manager and the sd card (or
        # other external storage) to be ready.
        self.cmd_exec.waitForDevicePm()
        self.sdcard_manager.waitForSdCardReady(timeout)
        
    def shutdown(self):
        """ 关闭设备
        """
        self.cmd_exec.sendCommand('reboot -p')
        