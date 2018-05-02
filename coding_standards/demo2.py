#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import pymysql

class SpiderByIp(object):

    ip_url = "https://www.ipip.net/ip.html"
    def actionSpider(self, ip):
        browser = webdriver.Chrome()
        browser.get(self.ip_url)
        time.sleep(2)
        input_str = browser.find_element_by_id('ip')
        input_str.send_keys(str(ip))
        time.sleep(1)
        button = browser.find_elements_by_tag_name("button")[0]
        button.click()
        time.sleep(4)

        need_text1 = browser.find_element_by_id('myself')
        need_text2 = browser.find_element_by_id('timezone')
        need_text3 = browser.find_element_by_xpath("/html/body/div[2]/div[4]/table[1]/tbody/tr[2]/td[2]")

        print(need_text1.text)
        print(need_text2.text)
        print(need_text3.text)
        insert_data = [ip]

        n1, n2 = need_text1.text.split(' ')
        # print(need_text2.text)
        n3, n4 = need_text3.text.split(' ', 1)

        jwd = need_text2.text.split(' ')
        print(jwd)
        n5 = jwd[-3].split("：")[-1]
        print("$$$")
        print(n5)
        n6 = jwd[-1]

        now_time = int(time.time())
        insert_data.append(n1) # address1
        insert_data.append(n3) # address2
        insert_data.append(n2) # websit  n4 company
        insert_data.append(n5) # jingdu
        insert_data.append(n6) # weidu
        insert_data.append(n4) # company name
        insert_data.append(now_time) # company name
        insert_data.append(now_time) # company name

        return insert_data;



        browser.close()


    def actionInsertData(self, insert_data, n):
        db = pymysql.connect(host = "localhost", user = "root", password = "123456", db = "yata_data_01", port = 3306, charset="utf8")
        cursor = db.cursor()
        sql = """INSERT INTO ip_to_info (ip, address_1, address_2, website, lon, lat, company_name, created_at, updated_at)   
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, %d)"""
        #try:
        insert_data = tuple(insert_data)
        print('ssss')
        print(insert_data)
        end_sql  = sql % insert_data
        cursor.execute(end_sql)
        db.commit()
        print("insert " + str(n) + " times")
        #except Exception as e:
            # print(e)
            # db.rollback()
            # print(sql % insert_data)
            # print("????error" * 10)

        db.close() 


app = SpiderByIp()
data = app.actionSpider("108.16.114.223")
app.actionInsertData(data, 1)