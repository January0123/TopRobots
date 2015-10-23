# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.processmanager
# 
# Creation      : 2013-10-31
# Author        : huangjj@ucweb.com
###########################################################################

from uc_tools import cmdexec
import re


MEMORY_INFO_RE = re.compile('^(?P<key>\w+):\s+(?P<usage_kb>\d+) kB$')
NVIDIA_MEMORY_INFO_RE = re.compile('^\s*(?P<user>\S+)\s*(?P<name>\S+)\s*'
                                   '(?P<pid>\d+)\s*(?P<usage_bytes>\d+)$')

class ProcessManager(object):
    """ 安卓设备的进程管理
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
        
    def getPid(self, pkg_name):
        """ 获取当前包对应的进程PID

        :param pkg_name: 包名
        :type pkg_name: string

        :returns: 当前包对应的进程PID
        :rtype: string
        """
        pid = ''
        cmd = "ps"
        text= self.cmd_exec.sendShellCommand(cmd)
        lines=text.split('\r\n')
        index = 1
        for line in lines:
            if len(line) <= 0:
                continue
            line = line.strip('\r')
            pkglist=line.split()
  
            if " PID " in line:
                for i in range(len(pkglist)):
                    if pkglist[i] == "PID":
                        index = i
                        continue
            elif (pkg_name in line) \
                    and (pkg_name == pkglist[-1]):

                pid = pkglist[index]
                break
        return pid
        
    def killPid(self, pid, signum=9):
        """ 根据PID杀掉进程

        :param pid: 进程的PID号
        :type pid: int 或者 str

        :param signum: 杀进程的信号量，默认为9
        :type signum:  int
        """
        kill_cmd = "kill  -" + str(signum) + " " + str(pid)
        self.cmd_exec.sendShellCommand(kill_cmd)
        
#     def extractPid(self, process_name):
#         '''
#         Extracts Process Ids for a given process name from Android Shell.
#     
#         Args:
#             process_name: name of the process on the device.
#     
#         Returns:
#             List of all the process ids (as strings) that match the given name.
#             If the name of a process exactly matches the given name, the pid of
#             that process will be inserted to the front of the pid list.
#         '''
#         pids = []
#         for line in self.cmd_exec.sendShellCommand('ps'):
#             data = line.split()
#             print data
#             try:
#                 if process_name in data[-1]:  # name is in the last column
#                     print process_name
#                     if process_name == data[-1]:
# #                        print process_name
#                         pids.insert(0, data[1])  # PID is in the second column
#                 else:
#                     pids.append(data[1])
#             except IndexError:
#                 pass
#         return pids
#     
#     
#     
#     def killAll(self, process):
#         '''
#         Android version of killall, connected via adb.
#     
#         Args:
#           process: name of the process to kill off
#     
#         Returns:
#           the number of processes killed
#         '''
#         pids = self.extractPid(process)
#         if pids:
#             self.cmd_exec.sendShellCommand('kill -9 ' + ' '.join(pids))
#         return len(pids)
#     
#     def killAllBlocking(self, process, timeout_sec):
#         '''
#         Blocking version of killall, connected via adb.
#     
#         This waits until no process matching the corresponding name appears in ps'
#         output anymore.
#     
#         Args:
#           process: name of the process to kill off
#           timeout_sec: the timeout in seconds
#     
#         Returns:
#           the number of processes killed
#         '''
#         processes_killed = self.killAll(process)
#         if processes_killed:
#             elapsed = 0
#             wait_period = 0.1
#             # Note that this doesn't take into account the time spent in ExtractPid().
#             while self.extractPid(process) and elapsed < timeout_sec:
#                 time.sleep(wait_period)
#                 elapsed += wait_period
#             if elapsed >= timeout_sec:
#                 return 0
#         return processes_killed
#         
#     def getProtectedFileContents(self, filename, log_result=False):
#         '''
#         Gets contents from the protected file specified by |filename|.
#     
#         This is less efficient than GetFileContents, but will work for protected
#         files and device files.
#         '''
#         # Run the script as root
#         return self.cmd_exec.sendShellCommand('cat "%s"' % filename)
#  
#     def getMemoryUsageForPid(self, pid):
#         '''
#         Returns the memory usage for given pid.
#     
#         Args:
#           pid: The pid number of the specific process running on device.
#     
#         Returns:
#           A tuple containg:
#           [0]: Dict of {metric:usage_kb}, for the process which has specified pid.
#           The metric keys which may be included are: Size, Rss, Pss, Shared_Clean,
#           Shared_Dirty, Private_Clean, Private_Dirty, Referenced, Swap,
#           KernelPageSize, MMUPageSize, Nvidia (tablet only).
#           [1]: Detailed /proc/[PID]/smaps information.
#         '''
#         usage_dict = collections.defaultdict(int)
#         smaps = collections.defaultdict(dict)
#         current_smap = ''
#         contents = self.getProtectedFileContents('/proc/%s/smaps' % pid, log_result=False)
#         key = None
#         usage_kb = 0
#         for line in contents:
#             items = line.split()
#             # See man 5 proc for more details. The format is:
#             # address perms offset dev inode pathname
#             if len(items) > 5:
#                 current_smap = ' '.join(items[5:])
#             elif len(items) > 3:
#                 current_smap = ' '.join(items[3:])
#             match = re.match(MEMORY_INFO_RE, line)
#             if match:
#                 key = match.group('key')
#                 usage_kb = int(match.group('usage_kb'))
#                 usage_dict[key] += usage_kb
#             if key not in smaps[current_smap]:
#                 smaps[current_smap][key] = 0
#                 smaps[current_smap][key] =  smaps[current_smap][key] + usage_kb
#             if not usage_dict or not any(usage_dict.values()):
#                 # Presumably the process died between ps and calling this method.
#                 logging.warning('Could not find memory usage for pid ' + str(pid))
#         print smaps
    
#     def processesUsingDevicePort(self, device_port):
#         '''
#         Lists processes using the specified device port on loopback interface.
#     
#         Args:
#           device_port: Port on device we want to check.
#     
#         Returns:
#           A list of (pid, process_name) tuples using the specified port.
#         '''
#         tcp_results = self.cmd_exec.sendShellCommand('cat /proc/net/tcp', log_result=False)
#         tcp_address = '0100007F:%04X' % device_port
#         pids = []
#         for single_connect in tcp_results:
#             connect_results = single_connect.split()
#             # Column 1 is the TCP port, and Column 9 is the inode of the socket
#             if connect_results[1] == tcp_address:
#                 socket_inode = connect_results[9]
#                 socket_name = 'socket:[%s]' % socket_inode
#                 lsof_results = self.cmd_exec.sendShellCommand('lsof', log_result=False)
#                 for single_process in lsof_results:
#                     process_results = single_process.split()
#                     # Ignore the line if it has less than nine columns in it, which may
#                     # be the case when a process stops while lsof is executing.
#                     if len(process_results) <= 8:
#                         continue
#                     # Column 0 is the executable name
#                     # Column 1 is the pid
#                     # Column 8 is the Inode in use
#                     if process_results[8] == socket_name:
#                         pids.append((int(process_results[1]), process_results[0]))
#                 break
#         return pids
        