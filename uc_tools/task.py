#!/usr/bin/python
# -*-coding=utf-8-*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : task.py
# 
# Creation      : 2013-9-10
# Author        : laijx@ucweb.com
###########################################################################

import os, sys
import glob, time, re
from PIL import Image
import urllib, urllib2
sys.path.append(os.getcwd())
import shutil, md5
import cookielib, subprocess

class image_diff():
    def __init__(self,p1,p2,smallsize=200):
        if(os.path.exists(p1) and os.path.exists(p2)):
            self.lf=Image.open(p1)
            self.rf=Image.open(p2)
        else:
            print "%s 或%s 不存在，比较失败" %(p1,p2)
            #exit()
            return
        
        #图片宽
        self.image_width,        self.image_height =self.lf.size 
        self.image_width =int(self.image_width/smallsize)*smallsize
        #图片高

        self.image_height=int(self.image_height/smallsize)*smallsize
        #分块计算的块宽度    
        self.part_width = self.image_width/smallsize

        #分块计算的块高度
        self.part_height = self.image_height/smallsize

        self.part_count = (self.image_width/self.part_width)*(self.image_height/self.part_height)*1.00
        
    def make_regalur_image(self,img):
        size = (self.image_width, self.image_height)
        
        return img.resize(size).convert('RGB')
    
    def split_image(self,img):
        part_size = (self.part_width, self.part_height)
        w, h = img.size
        pw, ph = part_size
        
        assert w % pw == h % ph == 0
        temp=[img.crop((i, j, i+pw, j+ph)).copy() for i in xrange(w/4, w/2, pw) for j in xrange(h/4, h/2, ph)]
        temp.extend([img.crop((i, j, i+pw, j+ph)).copy() for i in xrange(3*w/4, w, pw) for j in xrange(3*h/4, h, ph)])
        return temp
    
    def hist_similar(self,lh, rh):
        assert len(lh) == len(rh)
        ts= sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)
#         print ts,lh,rh
        return ts
    
    def calc_similar(self,li, ri):
    #    return hist_similar(li.histogram(), ri.histogram())
#         return sum(self.hist_similar(l.histogram(), r.histogram()) for l, r in zip(self.split_image(li), self.split_image(ri))) / self.part_count
        tempzip=zip(self.split_image(li), self.split_image(ri))
#         tempsum=sum(self.hist_similar(l.histogram(), r.histogram()) for l, r in tempzip)
        ll=[]
        rr=[]
        b=0.0
        for l,r in tempzip:
             
            ll.append(self.avhash(l))
            rr.append(self.avhash(r))
        for l1 in ll:
            if(l1 in rr):
                b=b+1
        return b/len(ll)

    
    def avhash(self,im):
    
#         if not isinstance(im, Image.Image):
#             im = Image.open(im)
        im = im.resize((self.part_width, self.part_height), Image.ANTIALIAS).convert('L')
        avg = reduce(lambda x, y: x + y, im.getdata()) /(self.part_width*self.part_height)
        return reduce(lambda x, (y, z): x | (z << y), enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),0)
            
    def compareimage(self):
        '''
        比较两张图片，返回两者的相似度
        一般>0.9则为相似,
        如果只传图片名称，则到当前目录的img下取图片，否则请传绝对路径
        '''


        li, ri = self.make_regalur_image(self.lf), self.make_regalur_image(self.rf) 
        li.save("li.jpg")
        ri.save("ri.jpg")
        return self.calc_similar(li, ri)
def get_image_diff(p1,p2):
    try:
        myimage_diff= image_diff(p1,p2)
    except:
        print "image_diff error"
        return 0.01
    return myimage_diff.compareimage()
if __name__ == '__main__':
    print "Test this Class"
