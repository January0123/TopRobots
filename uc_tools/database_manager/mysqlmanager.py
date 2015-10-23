# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : mysqlmanager
# 
# Creation      : 2013-12-20
# Author        : huangjj@ucweb.com
###########################################################################
 
import MySQLdb,MySQLdb.cursors

class  MySQLManager(object):
	""" 数据库连接管理器
	"""

	def  __init__(self, host, user, passwd, db, port=3306,charset='utf8',cursorclass = MySQLdb.cursors.DictCursor):
		""" 构造方法

		:param host: 数据库所在主机IP
		:type host: string

		:param user: 数据库用户名
		:type user: string


		:param passwd: 数据库密码
		:type passwd: string

		:param db: 数据库名字
		:type db: string

		:param port: 数据库使用的端口
		:type port: int

		:param charset:	数据库使用的字符集， 默认是 ``utf8-8``
		:type: charset: string

		:param cursorclass:	 数据库使用的cursorclass，默认是 ``MySQLdb.cursors.DictCursor``，返回一个字典
		:type: cursorclass: MySQLdb.cursors
		"""
		self.__host = host
		self.__user = user
		self.__passwd = passwd
		self.__db = db
		self.__port = port
		self.__charset = charset
		self.__connection = None
		self.__cursor = None
		self.cursorclass = cursorclass

	def __connect(self):
		""" 创建一个新的数据库连接
		"""
		self.__connection = MySQLdb.connect(host=self.__host,
				user=self.__user,passwd=self.__passwd, port=self.__port, charset=self.__charset, cursorclass=self.cursorclass)
		self.__connection.select_db(self.__db)
		self.__cursor = self.__connection.cursor()

	def __checkInit(self):
		""" 检查是否需要进行数据库连接，如果需要，创建新的连接
		"""
		if not self.__connection:
			self.__connect()

		if not self.__cursor:
			self.__connect()

	def getConnection(self):
		""" 获取数据库连接

		:returns: 一个数据库连接对象
		"""
		self.__checkInit()
		return self.__connection

	def getCursor(self):
		""" 获取Cursor对象

		:returns: 返回一个Cursor对象
		"""
		self.__checkInit()
		return  self.__cursor

	def insert(self, sql, values):
		""" 进行数据库插入操作

		:param sql: 数据库插入语句
		:type sql: string

		:param values: 需要插入数据库的值
		:type values: list

		:returns: 数据插入后的Id
		"""
		self.__execute(sql, values)
		data_id = self.__cursor.lastrowid
		self.__connection.commit()
		self.closeCursor()
		self.closeConnection()
		return data_id

	def __execute(self, sql, params):
		""" 数据库操作语句

		:param sql: 数据库插入语句
		:type sql: string

		:param params: 需要插入数据库的值
		:type params: list
		"""
		if not self.__cursor:
			self.__connect()
		try:
			self.__cursor.execute(sql, params)
		except (AttributeError, MySQLdb.OperationalError):
			self.closeCursor()
			self.closeConnection()
			self.__checkInit()
			self.__cursor.execute(sql, params)

	def executeSQL(self, sql, params, fetch="all"):
		""" 数据库操作语句

		:param sql: 数据库插入语句
		:type sql: string

		:param params: 需要插入数据库的值
		:type params: list

		:param params: 需要插入数据库的值
		:type params: list

		:param fetch: 是否获取全部值，默认是 ``all``,如果值是 ``one``,只返回一条结果
		:type fetch: string	

		:returns: 	如果 ``fetch`` 的值是 ``all``, 返回查询到的所有数据，如果值是 ``one``,只返回一条结果
		"""
		self.__execute(sql, params)
		self.__connection.commit()

		if fetch == "all":
			result = self.__cursor.fetchall()
		elif fetch == "one":
			result = self.__cursor.fetchone()
		else:
			result = None
		self.closeCursor()
		self.closeConnection()
		return result

	def closeCursor(self):
		""" 关闭cursor
		"""
		if self.__cursor:
			self.__cursor.close()
			self.__cursor = None

	def closeConnection(self):
		""" 关闭数据库连接
		"""
		if self.__connection:
			self.__connection.close()
			self.__connection = None

	def __del__(self):
		""" 当对象被回收时，检测并且关闭数据库连接
		"""
		if self.__cursor:
			self.__cursor.close()
			
		if self.__connection :
			self.__connection.close()

