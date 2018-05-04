#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from scrapy import Selector
import pymysql

db = pymysql.connect(host = "localhost", user = "root", password = "", db = "yata_data_01", port = 3306, charset="utf8")
cursor = db.cursor()

class GetProxy(object):

    def update_available_ip(self, ip, status):
        updated_sql = "updated proxy_ip set status = {0} where ip = '{1}'".format(status, ip)
        cursor.execute(updated_sql)
        db.commit()
        return True

    def delete_ip(self, ip):
        delete_sql = "delete from proxy_ip where ip = '{0}'".format(ip)
        cursor.execute(delete_sql)
        db.commit()
        return True

    def decide_ip(self, ip, port):
        http_url = "http://ipinfo.io/"
        proxy_url = "http://{0}:{1}".format(ip, port)

        print("proxy_url ", proxy_url)
        try:
            proxy_dict = {
                'http': proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Except as e:
            print("[没有返回]---代理 ip {0} 及 端口号 {1} 不可用，即将从数据库中删除".format(ip, port))
            self.update_available_ip(ip, 0)
            return False
        else:
            code = response.status_code
            if code >= 200 or code < 300:
                print("代理----ip {0} 及 端口号 {1} 可用".format(ip, port))
                return True
            else:
                print("[有返回，但是状态码异常]代理----ip {0} 及 端口号 {1} 不可用，即将从数据库中删除".format(ip, port))
                self.update_available_ip(ip, 0)
                return False


    def get_random_proxy(self):
        random_sql = "select ip,port from proxy_ip order by rand() limit 1"
        cursor.execute(random_sql)
        line = cursor.fetchone()
        ip = line[0]
        port = line[1]

        judge_re = self.decide_ip(ip, port)
        if judge_re:
            self.update_available_ip(ip, 1)
            return "http://{0}:{1}".format(ip, port)
        else:
            return self.get_random_proxy()

    
    def crawl_ips(self):
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}

        for i in range(1, 3):
            response = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
            selector = Selector(text=response.text)
            all_trs = selector.css("#ip_list tr")
            ip_list = []
            for tr in all_trs[1:]:

                ip = tr.css("td")[1].extract()
                port = tr.css("td")[2].extract()
                server_address = tr.css("td:nth-child(4)")[0]
                print(server_address)
                return True
                # title = speed_str.css(".bar::attr(title)").extract()[0]
                # if title:
                #     pass
                #     speed = float(title.split("秒")[0])
                # all_texts = tr.css("td::text").extract()
                # print(all_texts)

                # ip = all_texts[0]
                # port = all_texts[1]
                # attr = all_texts[4]
                # type = all_texts[5]
                # if attr == 'HTTPS' or attr == 'HTTP':
                #     attr = '----------'
                #     type = all_texts[4]

                # ip_list.append((ip, port, speed, type))

app = GetProxy()
app.crawl_ips()