# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : uc_tools.smtpmailmanager
# 
# Creation      : 2013-10-31
# Author        : huangjj@ucweb.com
###########################################################################

import smtplib

from email.mime.text import MIMEText 

def sendMail(mail_host, mail_user, mail_passwd, mail_to, subject, content):
	""" 发送邮件

	:param mail_host: 用于发送邮件的服务器地址,如：mail.ucweb.com
	:type mail_host: string

	:param mail_user: 邮件发送人的邮箱，如：uctools@ucweb.com
	:type mail_user: string

	:param mail_passwd: 邮件发送人密码
	:type mail_passwd: string

	:param mail_to: 邮件接收人
	:type mail_to: list

	:param subject: 邮件主题
	:type subject: string

	:param content: 邮件内容
	:type content: string
	"""
	smtp_obj = initSTMPObject(mail_host, mail_user, mail_passwd)
	message = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个实例，这里设置为html格式邮件
	message['Subject'] = subject    #设置主题
	message['From'] = mail_user  
	message['To'] = ";".join(mail_to)
	smtp_obj.sendmail(mail_user, mail_to, message.as_string())
	smtp_obj.close()

def initSTMPObject(mail_host, mail_user, mail_passwd):
	""" 初始化SMTP对象

	:param mail_host: 用于发送邮件的服务器地址,如：mail.ucweb.com
	:type mail_host: string

	:param mail_user: 邮件发送人的邮箱，如：uctools@ucweb.com
	:type mail_user: string

	:param mail_passwd: 邮件发送人密码
	:type mail_passwd: string

	:returns: 返回SMTP对象
	:rtype:  smtplib.SMTP	
	"""
	smtp_obj = smtplib.SMTP()
	smtp_obj.connect(mail_host)
	smtp_obj.login(mail_user, mail_passwd)
	return smtp_obj
