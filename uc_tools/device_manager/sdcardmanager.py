# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.device_manager.SDCardManger
# 
# Creation      : 2013-10-30
# Author        : huangjj@ucweb.com
###########################################################################

from uc_tools import cmdexec
import logging
import time
from uc_tools import errors

class SDCardManager(object):
    """ SDcard管理器，可以获取SDcard的路径，或者等待sdcard安装就绪
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
        self._external_storage = ''
        
    def getExternalStorage(self):
        """ 获取拓展卡的路径，比如sdcard的

        :returns: 返回拓展卡的路径(eg: /storage/sdcard0)
        :rtype: string
        """
        if not self._external_storage:
            self._external_storage = self.cmd_exec.sendShellCommand('echo $EXTERNAL_STORAGE')[0]
            assert self._external_storage, 'Unable to find $EXTERNAL_STORAGE'
        return self._external_storage
        
    def waitForSdCardReady(self, timeout_time):
        """ 等待sdcard就绪

        :param timeout_time: 等待时间
        :type timeout_time: int
        """
        sdcard_ready = False
        attempts = 0
        wait_period = 5
        external_storage = self.getExternalStorage()
        while not sdcard_ready and attempts * wait_period < timeout_time:
            output = self.cmd_exec.sendShellCommand('ls ' + external_storage)
            if output:
                sdcard_ready = True
            else:
                time.sleep(wait_period)
                attempts += 1
        if not sdcard_ready:
            raise errors.WaitForResponseTimedOutError(
                                                      'SD card not ready after %s seconds' % timeout_time)
        