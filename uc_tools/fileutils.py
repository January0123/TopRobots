# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.fileutils
# 
# Creation      : 2013-10-31
# Author        : huangjj@ucweb.com
###########################################################################

import os
import stat
import errors
import shutil
import zipfile
  
"""
封装了常用的目录或者文件的创建、删除、复制、移动、压缩、解压的方法
"""

def delete(path):
    """ 删除目录或者文件

    :param path: 需要删除的目录或者文件的路径
    :type path: string

    :raise error.MsgException: 当文件夹不存在的时候，抛出该异常
    """
    exist = os.path.exists(path)
    if not exist:
        raise errors.MsgException("<%s> is not exists!")
    
    if os.path.isfile(path):
        try:
            os.remove(path)
        except:
            pass
    elif os.path.isdir(path):
        for item in os.listdir(path):
            itemsrc=os.path.join(path,item)
            delete(itemsrc) 
        try:
            os.rmdir(path)
        except:
            pass
        
def createFolder(path):
    """ 创建文件夹，例如我想在 ``/home/uc/`` 目录下创建一个 ``tech`` 目录，则传入 ``path="/home/uc/tech"`` 即可
    如果文件夹本身就存在，则不再去重新创建。

    :param path: 需要创建的文件夹的路径
    :type path: string
    """
    ex = os.path.exists(path)

    if(not ex):
        os.makedirs(path)
     
def createFile(path, content="",mode="w"):
    """ 创建文件

    :param path: 文件的路径，具体到该文件的名字
    :type path: string

    :param content: 如果 ``mode`` 不是只读，将会把content的内容写进去
    :type content: string

    :param mode: 文件创建的模式
    :type mode: string
    """
    ex = os.path.exists(path)

    if(not ex):
        f=open(path, mode)
        if mode != "r":
            f.write(content)
        f.close()
        
def copy(src, dst):
    """ 复制文件

    :param src: 需要复制的文件路径
    :type src: string

    :param dst: 需要将文件复制到的指定目录的路径
    :type dst: string

    :raise errors.MsgException: 文件复制失败
    """
    if os.path.isdir(src):
        names = os.listdir(src)
    elif os.path.isfile(src):
        shutil.copy2(src, dst)
        return

    if not os.path.exists(dst):
        os.mkdir(dst)
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.isdir(srcname):                
                copy(srcname, dstname)
            else:
                if (not os.path.exists(dstname)
                    or ((os.path.exists(dstname))
                        and (os.path.getsize(dstname) != os.path.getsize(srcname)))):
#                     print dstname
                    shutil.copy2(srcname, dst)
        except:
            raise errors.MsgException("folder and file copy failure")

def extract(zip_file_name, unzip_to_dir):
    """ 解压文件

    :param zip_file_name: 需要解压的文件的路径
    :type zip_file_name: string

    :param unzip_to_dir: 存放解压文件的路径
    :type unzip_to_dir: string

    .. note:: 当前仅支持解压zip格式的压缩包
    """
    f_zip = zipfile.ZipFile(zip_file_name, 'r')

    # extra all file to the unzip_to_dir
    f_zip.extractall(unzip_to_dir)
    f_zip.close()
    # extra each file to the unzip_to_dir
    # for f in f_zip.namelist():
    #     f_zip.extract(f, unzip_to_dir)
  
def compress(path, zip_file_name):
    """ 压缩文件为zip格式

    .. warning:: 该目录下的子文件夹的名字不能跟当前文件夹的名字一样

    :param path: 需要压缩的文件或者目录的路径
    :type path: string

    :param zip_file_name: 压缩后的文件的名字
    :type zip_file_name: string
    """
    zip_file = zip_file_name.split(os.sep)
    zip_file = zip_file[len(zip_file) - 1]
    # print zip_file
    if not os.path.exists(path):  
        raise errors.MsgException("function compress:not exists file or dir(%s)" % (path))  
    
    f = zipfile.ZipFile(zip_file_name,'w',zipfile.ZIP_DEFLATED)
    
    if os.path.isfile(path):
        f.write(path,os.path.split(path)[1])
    elif os.path.isdir(path):
        startdir = path
        for dirpath, dirnames, filenames in os.walk(startdir):
            for filename in filenames:
                abs_path = os.path.join(os.path.join(dirpath, filename))
                rel_path = os.path.relpath(abs_path, os.path.dirname(startdir))
                f.write(os.path.join(dirpath,filename), rel_path)
    f.close()

    if os.path.exists(zip_file_name):
        os.chmod(zip_file_name, stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH) # mode:744)

def getUCToolsLocation():
    """ 获取基类所在的路径

    :returns: 基类所在的父文件夹
    :rtype: string
    """
    path = os.path.split(os.path.realpath(__file__))[0]
    path = os.path.join(path,os.path.pardir)
    path = os.path.abspath(path)
    return path

# def createPath(path, folders):
#     """ 进行路径的拼接

#     :param path: 需要拼接的路径
#     :type path: string

#     :param folders: 文件路径字典
#     :type folders: list

#     :returns: 拼接后的字符串路径
#     :rtype: string
#     """
#     for folder in folders:
#         path = os.path.join(path, folder)
    # return path

def createPath(folders):
    """ 进行路径的拼接

    :param folders: 文件路径字典
    :type folders: list

    :returns: 拼接后的字符串路径
    :rtype: string
    """
    if not len(folders):
        return ""

    path = folders[0]

    for i in range(1, len(folders)):
        path = os.path.join(path, folders[i])
    return path
    