#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import pymysql

class SpiderByIp(object):

    ip_url = "https://www.ipip.net/ip.html"

    def actionOpen(self):
        browser = webdriver.Chrome()
        browser.get(self.ip_url)
        time.sleep(2)

        return browser
        


    def actionSpider(self, ip, browser):
        
        input_str = browser.find_element_by_id('ip')
        input_str.clear()
        input_str.send_keys(str(ip))
        time.sleep(1)
        button = browser.find_elements_by_tag_name("button")[0]
        button.click()
        time.sleep(3)

        need_text1 = browser.find_element_by_id('myself')
        need_text2 = browser.find_element_by_id('timezone')
        
        need_text3 = browser.find_element_by_xpath("/html/body/div[2]/div[last()-1]/table[1]/tbody/tr[2]/td[2]")
        
        # print(need_text1.text)
        # print(need_text2.text)
        # print(need_text3.text)
        insert_data = [ip]

        out_text1 = need_text1.text.split(' ', 1)
        if (1 == len(out_text1)):
            n1 = out_text1[0]
            n2 = ''
        else:
            n1, n2 = need_text1.text.split(' ', 1)
        # print(need_text2.text)
        n3, n4 = need_text3.text.split(' ', 1)

        if '' == need_text2.text:
            n5 = 0
            n6 = 0
        else: 
            jwd = need_text2.text.split(' ')
            # print(jwd)
            n5 = jwd[-3].split("：")[-1]
            # print("$$$")
            # print(n5)
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


    def actionConnect(self):
        db = pymysql.connect(host = "localhost", user = "root", password = "123456", db = "yata_data_01", port = 3306, charset="utf8")
        cursor = db.cursor()
        return (cursor, db)


    def actionInsertData(self, insert_data, n, db):
        
        sql = """INSERT INTO ip_to_info (ip, address_1, address_2, website, lon, lat, company_name, created_at, updated_at)   
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, %d)"""
        #try:
        insert_data = tuple(insert_data)
        # print('ssss')
        # print(insert_data)
        end_sql  = sql % insert_data
        # print(end_sql)
        cursor.execute(end_sql)
        db.commit()
        print("insert id = " + str(n) + " ip =" + insert_data[0] + " times")
        #except Exception as e:
            # print(e)
            # db.rollback()
            # print(sql % insert_data)
            # print("????error" * 10)



    def actionMain(self, cursor, browser, db):
        select_sql = "select distinct IP_Address,id  from ip_address where id >= 1748 and length(IP_Address) <= 16 and IP_Address != '0' order by  id asc"
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        if rows is not None:
            
            for v in rows:
                use_data = self.actionSpider(v[0], browser)
                #print(use_data)
                self.actionInsertData(use_data, v[1], db)

            db.close()

        print("this task had over")


    


app = SpiderByIp()
o_list = app.actionOpen()
cursor, db = app.actionConnect()
app.actionMain(cursor, o_list, db)