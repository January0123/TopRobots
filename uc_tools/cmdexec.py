# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.cmdexec
# 
# Creation      : 2013-10-30
# Author        : huangjj@ucweb.com
###########################################################################

import adbcommand
import errors
import os
import runcommand
import time
 
class CMDExec(object):
    """ 这个类主要用于帮助通过adb与Android设备进行交互的；这个类中的方法解决了大量的Android的兼容性问题。
    比如是否支持使用 ``su -c`` ,命令是否必须带有单引号, etc.

    下面是一个简单的使用例子::

        from uc_tools.cmdexec import CMDExec

        cmd_exec = CMDExec()    
        cmd_exec.setTargetSerial("123456789")    # 如果连接了多台Android设别，需要指定需要操作的设备
        result = cmd_exec.sendShellCommand("ls") # 执行shell命令并且获取执行结果
        print result    #输出结果
    """
    
    def __init__(self, serial=None):
        """构造方法
        当只连接了一部Android设备或者设置了手机串号的时候，直接进行手机兼容性适配

        :param serial: Android设备串号
        :type serial: string
        """
        # argument to pass to adb, to direct command to specific device
        self._target_arg = ""
        # argument to pass to adb, enable command execute with root 
        self._su_arg = "su -c"
        # argument to pass to adb , to make command compatible most of the android system
        self._single_quote_arg = ""
        
        devices = adbcommand.getAttachedDevices()
        if len(devices) == 1 :
            self.compatible()
        elif serial != None:
            self.setTargetSerial(serial)
            
    def setEmulatorTarget(self):
        """直接将所有的命令都指向运行着的唯一的模拟器
        """
        self._target_arg = "-e"
     
    def setDeviceTarget(self):
        """ 直接将所有的命令都指向运行着的通过USB连接过来的Android设备
        """
        self._target_arg = "-d"
    
    def setTargetSerial(self, serial):
        """将所有的命令都给指定的串号的Android设备执行
        
        :param serial: 手机串号
        :type serial: string
        """
        self._target_arg = "-s %s" % serial
        self.compatible()
      
    def setSuString(self):
        """ 判断手机是否已经root了并且支持su，如果支持，所有的shell命令将带上 ``su -c``

        执行命令的命令格式为 ``adb shell "su -c [shell命令]"`` ,eg::

            adb shell "su -c ls"

        如果不支持，所有的shell命令都不带 su -c，执行的命令格式为 ``adb shell "[shell命令]"`` ,eg::

            adb shell "ls"
        """
        if not self.isSuSupport():
            self._su_arg = ""
        
    def isSuSupport(self):
        """判断手机是否已经root了并且支持 ``su``

        :returns: 如果支持，返回 ``True`` , 否则返回 ``False``
        :rtype: bool
        """
        adb_cmd = "adb %s shell su -c ps" % self._target_arg
        result = runcommand.runCommand(adb_cmd)
        failure_string_list = ["su: not found", "connect ui: Timer expired"]

        for failure_string in failure_string_list:
            if failure_string in result:
                return False
        return True
    
    def isSingleQuoteSupport(self):
        """判断手机执行adb命令的时候是否需要给命令加上单引号 ``'``
        
        :returns: 如果支持，返回 ``True`` , 否则返回 ``False``
        :rtype: bool
        """
        su_arg = ""
        is_su_support = self.isSuSupport()

        if is_su_support:
            su_arg = "su -c"

        #setSuString
        adb_cmd = "adb %s shell \"%s 'ls /system'\"" % (self._target_arg, su_arg)
        result = runcommand.runCommand(adb_cmd)
        
        error_string_array = ["sdcard", "No such file or directory", "not found"]
        
        for error_string in error_string_array:
            if error_string in result:
                return False
        return True
        
    def setSingleQuote(self):
        """ 判断手机执行命令是否需要添加单引号，如果需要，所有的shell命令将带上 ``'``

        执行命令的命令格式为 ``adb shell "[su -c] '[shell命令]'"`` ,eg::

            adb shell "su -c 'ls'"

        如果不支持，所有的shell命令都不带 ``'`` ，执行的命令格式为 ``adb shell "[su -c]  [shell命令]"`` ,eg::

            adb shell "su -c ls"
        """
        if self.isSingleQuoteSupport():
            self._single_quote_arg = "'"
        
    def compatible(self):
        """ 进行手机命令兼容性的适配
        """
        self.setSuString()
        self.setSingleQuote()
        
    def sendCommand(self, command_string, timeout_time=20, retry_count=3, block=True):
        """ 通过adb发送一条命令给安卓设备执行

        :param command_string: 需要手机执行的adb命令
        :type serial: string

        :param timeout_time: 超时时间，当命令执行超过该限定时间时将会被kill掉。默认为 ``20`` ,表示超时时间为20s
        :type timeout_time: int

        :param retry_count: 重试次数，当任务执行超时或者失败，将会按照重试次数重新执行,默认为3
        :type retry_count: int

        :param block: 如果值为 ``True`` ，则该命令执行为阻塞式
        :type block: bool

        :returns: 以 ``string`` 类型返回命令执行结果

        :raises errors.WaitForResponseTimedOutError: 当命令多次重试仍然超时没有响应的时候跑出该异常
        """
        adb_cmd = "adb %s %s" % (self._target_arg, command_string)
 
        return runcommand.runCommand(adb_cmd, timeout_time=timeout_time,
                                      retry_count=retry_count,block=block)
        
    def sendShellCommand(self, cmd, timeout_time=20, retry_count=3,block=True):
        """ 发送一条shell命令给安卓设备执行

        :param cmd: 需要手机执行的adb shell命令
        :type serial: string       

        :param timeout_time: 超时时间，当命令执行超过该限定时间时将会被kill掉。默认为 ``20`` ,表示超时时间为20s
        :type timeout_time: int

        :param retry_count: 重试次数，当任务执行超时或者失败，将会按照重试次数重新执行,默认为3
        :type retry_count: int

        :param block: 如果值为 ``True`` ，则该命令执行为阻塞式
        :type block: bool

        :returns: 以 ``string`` 类型返回命令执行结果
        :rtype: string

        :raises errors.WaitForResponseTimedOutError: 当命令多次重试仍然超时没有响应的时候跑出该异常 
        """
        if "input text" in cmd:
            contents = cmd.split()[-1]
            return self.inputText(contents)


        if "am start" in cmd :
            #todo add compatiability with su command
            shell_command = "shell \"%s\"" % (cmd)
        else:    
            #todo add compatiability with su command
            shell_command = "shell \"%s %s%s%s\"" % (self._su_arg, 
                                                     self._single_quote_arg,
                                                     cmd, 
                                                     self._single_quote_arg)

        return self.sendCommand(shell_command, timeout_time=timeout_time,
                                retry_count=retry_count,block=block)   


    def inputText(self, contents):
        """ 执行input text往手机中输入内容

        :param contents: 需要输入的内容
        :type contents: str
        """
        index = 0
        length = len(contents)

        while (index<length):
            content = contents[index]
            if content == "\\":
                index = index + 1
                content = content + contents[index]
            cmd = "input text " + content
            shell_command = "shell \"%s %s%s%s\"" % (self._su_arg, 
                                                 self._single_quote_arg,
                                                 cmd, 
                                                 self._single_quote_arg)
            self.sendCommand(shell_command)
            index = index + 1
        return "" 

    
    
    def bugReport(self, path, timeout_time=60):
        """ 执行 ``adb bugreport`` 命令并且将他的结果信息导出到指定路径的文件中

        :param path: 保存命令执行结果的文件所在的路径
        :type path: string

        :param timeout_time: 超时时间，当命令执行超过该限定时间时将会被kill掉。默认为 ``60`` ,表示超时时间为60s
        :type timeout_time: int
        """
    
        bug_output = self.sendShellCommand("bugreport", timeout_time=timeout_time)
        bugreport_file = open(path, "w")
        bugreport_file.write(bug_output)
        bugreport_file.close()
    
    def push(self, src, dest,timeout_time=60):
        """ 将文件从PC端保存到手机指定目录中

        :param src: 需要保存到手机中的文件路径
        :type src: string

        :param dest: 保存PC中传送过来的文件的路径
        :type dest: string

        :param timeout_time: 超时时间，当命令执行超过该限定时间时将会被kill掉。默认为 ``60`` ,表示超时时间为60s
        :type timeout_time: int

        :returns: 将文件从PC端保存到手机指定目录下的命令执行结果
        :rtype: string
        """
        return self.sendCommand("push %s %s" % (src, dest), timeout_time=timeout_time)
    
    def pull(self, src, dest, timeout_time=60):
        """ 将指定文件从手机导出并且保存到PC指定的目录中

        :param src: 需要导出的指定目录
        :type src: string

        :param dest: 需要文件的指定路径
        :type dest: string

        :param timeout_time: 超时时间，当命令执行超过该限定时间时将会被kill掉。默认为 ``60`` ,表示超时时间为60s
        :type timeout_time: int

        :returns: 如果需要导出的文件存在于手机中，则输出(True, 命令执行结果),否则返回（False, 手机中不存在该目录）
        :rtype: tuple
        """
        # Create the base dir if it doesn't exist already
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
    
        if self.doesFileExist(src):
            cmd = "pull %s %s" % (src, dest)
            # print "pull file in base tools : " + cmd
            result = self.sendCommand(cmd, timeout_time=timeout_time)
            # print "pull file in base tools : " + result
            return (True, result)
        else:
            #logger.Log("ADB Pull Failed: Source file %s does not exist." % src)
            return (False, "ADB Pull Failed: Source file %s does not exist." % (src))
    
    def enableAdbRoot(self):
        """ 执行 ``adb root``允许设备以root权限运行

        :returns: 如果设备已经可以以root权限运行，则返回 ``True``，否则返回 ``False``
        :rtype: bool
        """
        output = self.sendCommand("root")
        if "adbd is already running as root" in output:
            return True
        elif "restarting adbd as root" in output:
            # device will disappear from adb, wait for it to come back
            self.sendCommand("wait-for-device")
            return True
        else:
            #logger.Log("Unrecognized output from adb root: %s" % output)
            return False
    
    def isRootEnabled(self):
        """ 检查设备是否已经root了

        :returns: 如果设备已经root过了，则返回 ``True`` ，否则返回 ``False``
        :rtype: bool
        """
        root_test_output = self.sendShellCommand('ls /root') or ['']
        return not 'Permission denied' in root_test_output[0]
    
    
    def doesFileExist(self, src):
        """ 判断设备上是否含有指定的路径文件

        :param src: 需要判断是否存在设备上的目录
        :type src: string 

        :returns: 如果存在，则返回 ``True`` ，否则返回 ``False``
        :rtype: bool
        """
        output = self.sendShellCommand("ls %s" % src)
        error = "No such file or directory"
    
        if error in output:
            return False
        return True
    
    def waitForDevicePm(self, wait_time=120):
        """ 等待指定设备的包管理器的启动

        :param wait_time: 等待时间
        :type wait_time: int

        :raises errors.WaitForResponseTimedOutErro: 如果在指定时间内包管理器没有启动，则抛出这个异常
        """
        #logger.Log("Waiting for device package manager...")
        self.sendCommand("wait-for-device")
        # Now the device is there, but may not be running.
        # Query the package manager with a basic command
        try:
            self._waitForShellCommandContents("pm path android",
                                              "package:",
                                              wait_time)
        except errors.WaitForResponseTimedOutError:
            raise errors.WaitForResponseTimedOutError("Package manager did not respond after %s seconds" % wait_time)
            
    def waitForProcess(self, name, wait_time=120):
        """ 等待进程开始

        :param name: 进程名字
        :type name: string

        :param wait_time: 等待时间
        :type wait_time: int
        """
        #logger.Log("Waiting for process %s" % name)
        self.sendCommand("wait-for-device")
        self._waitForShellCommandContents("ps", name, wait_time)
    
    def waitForProcessEnd(self, name, wait_time=120):
        """ 等待一个进程的结束

        :param name: 进程名字
        :type name: string

        :param wait_time: 等待时间
        :type wait_time: int

        :raises errors.WaitForResponseTimedOutErro: 如果在指定时间内指定进程依然运行，抛出这个异常
        """
        self._waitForShellCommandContents("ps", name, wait_time, invert=True)
    
    def _waitForShellCommandContents(self, command, expected, wait_time,
                                       raise_abort=True, invert=False):
        """ 执行命令，直到命令执行后出现预期中的结果或者超过等待时间爱你才停止

        :param command: 需要手机执行的shell命令
        :type command： string

        :param expected: 期望命令执行后的结果中含有的子字符串
        :type expected: string

        :param wait_time: 命令执行的等待时间
        :type wait_time: int

        :param raise_abort: 决定着当命令执行失败时是否抛出异常，默认为 ``True``
        :type raise_abort: bool

        :param invert: 如果设置为 ``True`` , 则仅当运行结果中不出现预期中的结果就算命令正确执行
                        如果设置为 ``False`` , 则仅当运行结果中出现语气中的结果才算命令正确执行
        :type invert: bool

        :raises errors.WaitForResponseTimedOutError: 如果命令在指定时间内依然没有执行成功，抛出这个异常
        """
        # Query the device with the command
        success = False
        attempts = 0
        wait_period = 5
        while not success and (attempts*wait_period) < wait_time:
            # assume the command will always contain expected in the success case
            try:
                output = self.sendShellCommand(command, retry_count=1)
                if ((not invert and expected in output) or (invert and expected not in output)):
                    success = True
            except errors.AbortError:
                if raise_abort:
                    raise
            # ignore otherwise
            if not success:
                time.sleep(wait_period)
                attempts += 1
    
        if not success:
            raise errors.WaitForResponseTimedOutError()
          
    def waitForBootComplete(self, wait_time=120):
        """ 等待手机重启完毕

        :param wait_time: 等待时间，默认为120s
        :type wait_time: int

        :raises errors.WaitForResponseTimedOutErro: 如果手机在指定时间内依然没有重启成功，抛出这个异常
        """
        #logger.Log("Waiting for boot complete...")
        self.sendCommand("wait-for-device")
        # Now the device is there, but may not be running.
        # Query the package manager with a basic command
        boot_complete = False
        attempts = 0
        wait_period = 5
        while not boot_complete and (attempts*wait_period) < wait_time:
            output = self.sendShellCommand("getprop dev.bootcomplete", retry_count=1)
            output = output.strip()
            if output == "1":
                boot_complete = True
            else:
                time.sleep(wait_period)
                attempts += 1
        if not boot_complete:
            raise errors.WaitForResponseTimedOutError(
                                                      "dev.bootcomplete flag was not set after %s seconds" % wait_time)
    
    def getSerialNumber(self):
        """ 获取指定设备的串号

        :returns: 指定设备的串号
        :rtype: string
        """
        return self.sendCommand("get-serialno").strip()
    
    def isOnline(self):
        """ 检测指定的设备状态是否为 device

        :returns: 如果手机的状态为device,返回 ``True``，否则返回 ``False``
        :rtype: bool
        """
        out = self.sendCommand('get-state')
        return out.strip() == 'device'
    
    def getDeviceYear(self):
        """ 获取手机中的年份信息

        :returns: 设备中的年份信息
        :rtype: string
        """
        return self.sendShellCommand('date +%Y')
    
    def restartShell(self):
        """ 通过 ``stop`` 和 ``start`` 重启设备
        """
        self.sendShellCommand('stop')
        self.sendShellCommand('start')

    def makeSystemFolderWritable(self):
        """ 设置安卓设备的system目录可读写

        :raises errors.MsgException: 当设置失败时抛出该异常 
        """
        out = self.sendCommand('remount')
        if out.strip() != 'remount succeeded':
            raise errors.MsgException('Remount failed: %s' % out)
            
        