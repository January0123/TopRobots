# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File     : runcommand
# 
# Creation : 2013-8-24
# Author   : huangjj@ucweb.com
###########################################################################

# System imports
import errors
import signal
import subprocess
import tempfile
import threading
import time
import platform
 
# local imports
_abort_on_error = False

def setAbortOnError(abort=True):
    """设置当程序返回一个 ``error code`` 时是否抛出 ``AbortError`` 异常

    :param abort: 设置是否抛出 ``AbortError`` 异常
    :type about: bool
    """
    global _abort_on_error
    _abort_on_error = abort
       
def runCommand(cmd, timeout_time=None, retry_count=3, return_output=True,
               stdin_input=None, block=True):
    """新建一个子进程执行命令

    :param cmd: 需要执行的命令
    :type cmd: string

    :param timeout_time: 超时时间，当命令执行超过该限定时间时将会被kill掉。默认为 ``None`` ,表示无设置超时时间
    :type timeout_time: int

    :param retry_count: 重试次数，当任务执行超时或者失败，将会按照重试次数重新执行
    :type retry_count: int

    :param return_output: 如果值为 ``True`` ，将命令执行后的输出按照 ``string`` 类型输出，否则直接输出到控制台
    :type return_output: bool

    :param stdin_input: 数据输入流

    :param block: 如果值为 ``True`` ，则该命令执行为阻塞式
    :type block: bool

    :returns: 当 ``return_output`` 值为 ``True`` 并且 ``block`` 值为 ``False`` 时，以 ``string`` 类型返回命令执行结果;其他情况返回 ``None``

    :raises errors.WaitForResponseTimedOutError: 当命令多次重试仍然超时没有响应的时候跑出该异常
    """
    if not block:
        runWithoutBlock(cmd)
        return

    result = None
    while True:
        try:
            result = runOnce(cmd, timeout_time=timeout_time,
                             return_output=return_output, stdin_input=stdin_input)
        except errors.WaitForResponseTimedOutError:
            if retry_count == 0:
                raise
            retry_count -= 1
        else:
            # Success
            return result
        
def runWithoutBlock(cmd):
    """新建一个子进程以非阻塞的形式执行命令

    :param cmd: 需要执行的命令
    :type cmd: string
    """
    if platform.system().upper == "Windows".upper():
        subprocess.Popen(cmd, stdout=subprocess.PIPE)   
    else:
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)   
             
def runOnce(cmd, timeout_time=None, return_output=True, stdin_input=None):
    """新建一个子进程以阻塞的形式执行命令

    :param cmd: 需要执行的命令
    :type cmd: string

    :param timeout_time: 超时时间，当命令执行超过该限定时间时将会被kill掉。默认为 ``None`` ,表示无设置超时时间
    :type timeout_time: int

    :param return_output: 如果值为 ``True`` ，将命令执行后的输出按照 ``string`` 类型输出，否则直接输出到控制台
    :type return_output: bool

    :param stdin_input: 数据输入流

    :returns: 当 ``return_output`` 值为 ``True`` 时，返回输出结果

    :raises errors.WaitForResponseTimedOutError: 当命令在规定的时间爱你内没有执行完毕时将会跑出该异常
    :raises errors.AbortError: 当命令执行失败并且需要终止程序执行时，跑出该异常
    """
    so = []
    global _abort_on_error, error_occurred
    error_occurred = False
       
    if return_output:
        output_dest = tempfile.TemporaryFile(bufsize=0)
    else:
        # None means direct to stdout
        output_dest = None
    if stdin_input:
        stdin_dest = subprocess.PIPE
    else:
        stdin_dest = None

    pipe = None
    if platform.system().upper == "Windows".upper():
        pipe = subprocess.Popen(
                                cmd,
                                stdin=stdin_dest,
                                stdout=output_dest,
                                stderr=subprocess.STDOUT)
    else:
        pipe = subprocess.Popen(
                        cmd,
                        stdin=stdin_dest,
                        stdout=output_dest,
                        stderr=subprocess.STDOUT,
                        shell=True)
    def Run():
        global error_occurred
        try:
            pipe.communicate(input=stdin_input)
            output = None
            if return_output:
                output_dest.seek(0)
                output = output_dest.read()
                output_dest.close()
            if output is not None and len(output) > 0:
                so.append(output)
        except OSError, e:
            so.append("ERROR")
            error_occurred = True
        if pipe.returncode:
            error_occurred = True
            
    t = threading.Thread(target=Run)
    t.start()
    t.join(timeout_time)
    if t.isAlive():
        try:
            pipe.kill()
        except OSError:
                # Can't kill a dead process.
            pass
        finally:
            raise errors.WaitForResponseTimedOutError
    output = "".join(so)
    if _abort_on_error and error_occurred:
        raise errors.AbortError(msg=output)
    return output
