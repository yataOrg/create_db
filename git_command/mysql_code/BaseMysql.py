#!/usr/bin/python3
# -*- coding: utf-8

'a demo'
__author__ = 'peng'

import pymysql

def insert_data():
	# 打开数据库连接
	# db = pymysql.connect("116.62.38.251","root","yata123","yata_data_01")
	db = pymysql.connect("localhost", "root", "", "get_yii")
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
 
	# SQL 插入语句
	sql = """INSERT INTO en_test (comment_id, 
        	key_word, weight) 
        	VALUES (%d, '%s', '%s')"""
	n = 0
	while n <= 70000:
		n += 1
		try:
			# 执行sql语句
	   		cursor.execute(sql % (n, 'key_word_' + str(n), 'weight_' + str(n)))
	   		# 提交到数据库执行
	   		db.commit()
	   		print("@@@" * 5 + str(n))
		except:
	   		# 事务回滚
	   		db.rollback()
	   		print(u"??????????报错了")
	db.close()

if __name__ == '__main__':
	print('test')
	insert_data()