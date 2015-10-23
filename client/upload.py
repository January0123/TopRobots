#!/usr/bin/python
# -*- coding: utf8 -*-

import MultipartPostHandler, urllib2, cookielib, os
import traceback, urllib, string, time, sys

reload(sys)
sys.setdefaultencoding('utf8')
print sys.argv[1]
print sys.argv[2]
result = sys.argv[1]
url = sys.argv[2]

print " "
print "================================================="

login_url = "http://uctest.ucweb.com:81/wml/auth.php?referer=/liuxx5/"
upload_url = "http://uctest.ucweb.com:81/zhangjie3/php_server/upload/upload.php"
#upload_url = "http://uctest.ucweb.com:81/yelq/daily-upload/upload/upload.php"
#upload_url = "http://localhost/daily-upload/upload/upload.php"

pic_dir = "client/pics"

user = "zhangjie3"
passwd = "7o8bLopd"

result_dir = "./client/result/"
if not os.path.exists(result_dir):
    os.makedirs(str(result_dir))

def writeRes(res, outfile):
    try:
        tmp = res.readlines()
        rtn_str = string.join(tmp)
        if not res.code == 200:
            print rtn_str
        file = open(result_dir + outfile, "wb")
        file.writelines(rtn_str)
        file.close()
    except Exception, e:
        print ""

def login() :
    params = { 'origURL' : login_url, 'u' : user, 'p' : passwd, "Connection" : "keep-alive"}
    print 'url: "' + login_url + '" login.......'
    try:
        req = urllib2.Request(login_url, urllib.urlencode(params))
        res = urllib2.urlopen(req)
        print "login sucessfully! res: "
        writeRes(res, "login.html")
        print " "
    except Exception, e:
        writeRes(e, filename + "-failed.html")
        print "login failed!"

def upload(filename, date_str):
    cookies = cookielib.CookieJar()
    
    image_path = os.getcwd() + os.path.sep + pic_dir + os.path.sep + filename
    print "os.path.abspath('..') " +os.path.abspath('..')
    print "os.getcwd " + os.getcwd()
    print "os.path.sep " + os.path.sep
    print  "pic_dir " + pic_dir
    print "filename " + filename	
    print "source file: " + image_path
    print "upload_url: " + upload_url
    
    params = { "u" : user, "p" : passwd,
               "file" : open(image_path, "rb"),
               "date" : date_str,
               "re" : result,
               "url" : url}

    print "start upload file: " + image_path
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
        MultipartPostHandler.MultipartPostHandler)
    try:
        res = opener.open(upload_url, params)
        writeRes(res, filename + ".html")
        print "upload successfully!"
    except Exception, e:
        errorstr = traceback.format_exc()
        print errorstr
        writeRes(e, filename + "-failed.html")



if not os.path.exists(pic_dir):
    print "ERROR: dir '" + pic_dir + "' not found!"
    exit()
    
#login()
    
upload_count = 0
#date_str = "20140223103055"
date_str = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()));
print "upload time: " + date_str

for filename in os.listdir(pic_dir):
    print "------------"
    upload(filename, date_str)
    upload_count = upload_count + 1

print "------------"
print "All done, count: " + str(upload_count) + "."

del_pics = 'del /Q "'+pic_dir+'"'
os.system(del_pics)
