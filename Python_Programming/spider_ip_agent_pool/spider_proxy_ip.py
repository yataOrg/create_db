#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, re, time
from scrapy import Selector
import pymysql

db = pymysql.connect(host="localhost", user="root", password="", db="yata_data_01", port=3306, charset="utf8")
cursor = db.cursor()


class MakeProxyIp(object):
    def crawl_ips(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}

        for i in range(1, 5):
            response = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
            selector = Selector(text=response.text)
            all_trs = selector.css("#ip_list tr")
            ip_list = []
            for tr in all_trs[1:]:

                ip = tr.css("td::text")[0].extract()
                port = tr.css("td::text")[1].extract()
                # print(tr.css("td:nth-child(4) > a::text").extract())
                if [] == tr.css("td:nth-child(4) > a::text").extract():
                    server_address = ''
                else:
                    server_address = tr.css("td:nth-child(4) > a::text").extract()[0]
                anonymous = tr.css("td::text")[4].extract()
                ip_type = tr.css("td::text")[5].extract()
                speed = tr.css("td:nth-child(7) > div::attr(title)").extract()[0]
                speed = re.sub("[^0-9\.]", "", speed)  #
                con_time = tr.css("td:nth-child(8) > div::attr(title)").extract()[0]
                con_time = re.sub("[^0-9\.]", "", con_time)  #

                alive_time = tr.css("td::text")[10].extract()
                check_time = tr.css("td::text")[11].extract()
                status = 1
                now_time = int(time.time())
                # print(check_time)
                # print(ip, port, server_address, anonymous)
                ip_list.append((ip, port, server_address, anonymous, ip_type, speed, con_time, alive_time, check_time,
                                status, now_time, now_time))

                # insert into database

            for ip_info in ip_list:
                insert_sql = '''
                    insert into proxy_ip (ip, port, server_address, anonymous, type, speed, con_time, alive_time, check_time, status, created_at, updated_at)  
                    values('{0}', {1}, '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', {9}, {10}, {11})'''.format(
                    ip_info[0], ip_info[1], ip_info[2], ip_info[3],
                    ip_info[4], ip_info[5], ip_info[6], ip_info[7], ip_info[8], ip_info[9], ip_info[10], ip_info[11])
                # print(insert_sql)
                # return
                cursor.execute(insert_sql)
                db.commit()

            print("insert ip list over " + str(i) + " pages")
        print("insert ip list end @@@@")
