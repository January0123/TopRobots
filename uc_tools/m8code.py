#!/usr/bin/python
#coding=utf-8
#########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File   : yun.py
# 
# Creation      : 2013-10-29
# Author : lizd@ucweb.com
# m8加解密处理
###########################################################################
import struct
import os
import sys
import re

def m8_encode(x):
    '''
    内容加密
    Args:
    x:加密内容
    Return：
    加密后的内容
    '''
    mask=[238, 185, 233, 179, 129, 142, 151, 167]
    #mask=[126, 147, 115, 241, 101, 198, 215, 134]
    maskS=0
    leng=len(x)
    bytes = ''
    for i in range(0,leng):
        a = struct.pack('c',x[i])
        a = struct.unpack('B',a)
        b = a[0] ^ mask[i % 8]
        bytes += struct.pack('B',b)
        maskS = maskS ^ a[0]
    bytes +=struct.pack('B',maskS ^ mask[0])
    bytes +=struct.pack('B',maskS ^ mask[1])
    return bytes
def m8_decode(x):
    '''
    内容解密
    Args:
    x:解密内容
    Return：
    解密后的内容
    '''
    mask=[238, 185, 233, 179, 129, 142, 151, 167]
    #mask=[126, 147, 115, 241, 101, 198, 215, 134]
    maskS=0
    leng=len(x)
    bytes = ''
    for i in range(0,leng-2):
        a = struct.pack('c',x[i])
        a = struct.unpack('B',a)
        b = a[0] ^ mask[i % 8]
        bytes += struct.pack('B',b)
        maskS = maskS ^ a[0]
    return bytes
def help():
    '''
    显示帮助内容
     'usage:  m8code.py [option] [source file]\r'
     '        e: Encode the source file\r'
     '        d: Dncode the source file\r'
     '        es: Encode the source files\r'
     '        ds: Dncode the source files\r'
    '''
    print 'usage:  m8code.py [option] [source file]\r'
    print '        e: Encode the source file\r'
    print '        d: Dncode the source file\r'
    print '        es: Encode the source files\r'
    print '        ds: Dncode the source files\r'
#h = m8_encode('abc123..$%^12')
#print m8_decode(h)
#print struct.unpack('BBBBBBBBBBBBBBB',h)
if len(sys.argv) > 2:
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    #print arg1
    #print arg2
    if arg1 == 'e':
        #arg3 = 'encode_' + re.findall("[^\/]*$",arg2,re.M)[0]
        arg3 = re.findall("[^\/]*$",arg2,re.M)[0]
        input = open(arg2, 'rb')
        dat = input.read()
        dst = m8_encode(dat)
        output = open(arg3, 'wb')
        output.write(dst)
        output.close()
        print 'encode sucess,encode file :'+arg3
    elif arg1 == 'd':
        #arg3 = 'decode_' + re.findall("[^\/]*$",arg2,re.M)[0]
        arg3 = re.findall("[^\/]*$",arg2,re.M)[0]
        input = open(arg2, 'rb')
        dat = input.read()
        dst = m8_decode(dat)
        output = open(arg3, 'wb')
        output.write(dst)
        output.close()
        print 'decode sucess,decode file:'+arg3
    elif arg1 == 'es':
        for parent, dirnames, filenames in os.walk(arg2):
            for filename in filenames:
                arg3 =os.path.join(parent, filename)
                arg4 =os.path.join(parent,'encode_'+filename)
                input = open(arg3, 'rb')
                dat = input.read()
                dst = m8_encode(dat)
                output = open(arg4, 'wb')
                output.write(dst)
                output.close()
                print 'encode sucess,encode file :'+arg4
    elif arg1 == 'ds':
        for parent, dirnames, filenames in os.walk(arg2):
            for filename in filenames:
                arg3 =os.path.join(parent, filename)
                arg4 =os.path.join(parent,'decode_'+filename)
                input = open(arg3, 'rb')
                dat = input.read()
                dst = m8_decode(dat)
                output = open(arg4, 'wb')
                output.write(dst)
                output.close()
                print 'decode sucess,decode file:'+arg4
    else :
        help()
else :
    help()
    
    
    
