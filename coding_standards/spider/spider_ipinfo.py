#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, re, time
from scrapy import Selector
import pymysql

db = pymysql.connect(host = "localhost", user = "root", password = "123456", db = "yata_data_01", port = 3306, charset="utf8")
cursor = db.cursor()

class GetProxy(object):

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
    
    def update_available_ip(self, ip, status):
        updated_sql = "update proxy_ip set status = {0} where ip = '{1}'".format(status, ip)
        cursor.execute(updated_sql)
        db.commit()
        return True

    def delete_ip(self, ip):
        delete_sql = "delete from proxy_ip where ip = '{0}'".format(ip)
        cursor.execute(delete_sql)
        db.commit()
        return True

    def decide_ip(self, ip, port, type):
        http_url = "https://ipinfo.io/"
        proxy_url = "{2}://{0}:{1}".format(ip, port, type)

        # print("proxy_url ", proxy_url)
        try:
            proxy_dict = {
                type: proxy_url
            }
            response = requests.get(http_url, headers = app.headers, verify = True, proxies = proxy_dict, timeout = 4)
        except Exception as e:
            print("[没有返回]---代理 ip {0} 及 端口号 {1} 不可用，即将从数据库中删除".format(ip, port))
            self.delete_ip(ip)
            #self.update_available_ip(ip, 0)
            return False
        else:
            code = response.status_code
            if code >= 200 or code < 300:
                print("代理----ip {0} 及 端口号 {1} 可用".format(ip, port))
                return True
            else:
                print("[有返回，但是状态码异常]代理----ip {0} 及 端口号 {1} 不可用，即将从数据库中删除".format(ip, port))
                # self.update_available_ip(ip, 0)
                self.delete_ip(ip)
                return False


    def get_random_proxy(self):
        random_sql = "select ip,port,type from proxy_ip order by rand() limit 1"
        cursor.execute(random_sql)
        line = cursor.fetchone()

        if line is None:
            self.crawl_ips()
            judge_re = False
        else:
            ip = line[0]
            port = line[1]
            ip_type = line[2]
            judge_re = self.decide_ip(ip, port, type)
            print("proxy is {0}:{1}".format(line[0], line[1]) + str(judge_re))

        if judge_re:
            self.update_available_ip(ip, 1)
            print('@@@@@@' *5)
            
            print("use this {0}:{1}---".format(line[0], line[1]))
            return {
                ip_type: "{2}://{0}:{1}".format(ip, port, ip_type)
            }
        else:
            print("use next")
            return self.get_random_proxy()

    
    def crawl_ips(self):
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}

        for i in range(1, 3):
            response = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
            selector = Selector(text=response.text)
            all_trs = selector.css("#ip_list tr")
            ip_list = []
            for tr in all_trs[1:]:

                ip = tr.css("td::text")[0].extract()
                port = tr.css("td::text")[1].extract()
                server_address = tr.css("td:nth-child(4) > a::text").extract()[0]
                anonymous = tr.css("td::text")[4].extract()
                ip_type = tr.css("td::text")[5].extract()
                speed = tr.css("td:nth-child(7) > div::attr(title)").extract()[0]
                speed = re.sub("[^0-9\.]", "", speed) #
                con_time = tr.css("td:nth-child(8) > div::attr(title)").extract()[0]
                con_time = re.sub("[^0-9\.]", "", con_time) #

                alive_time = tr.css("td::text")[10].extract()
                check_time = tr.css("td::text")[11].extract()
                status = 1
                now_time = int(time.time())
                # print(check_time)
                # print(ip, port, server_address, anonymous)
                ip_list.append((ip, port, server_address, anonymous, ip_type, speed, con_time, alive_time, check_time, status, now_time, now_time))

                # insert into database
            
            for ip_info in ip_list:
                insert_sql = '''
                    insert into proxy_ip (ip, port, server_address, anonymous, type, speed, con_time, alive_time, check_time, status, created_at, updated_at)  
                    values('{0}', {1}, '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', {9}, {10}, {11})'''.format(ip_info[0], ip_info[1], ip_info[2], ip_info[3], 
                        ip_info[4], ip_info[5], ip_info[6], ip_info[7], ip_info[8], ip_info[9], ip_info[10], ip_info[11])
                #print(insert_sql)
                # return
                cursor.execute(insert_sql)
                db.commit()   


            print("insert ip list over " + str(i) + " pages")
        print("insert ip list end @@@@")        

if __name__ == '__main__':
    app = GetProxy()
    # app.crawl_ips()

    proxy_dict = app.get_random_proxy()
    print('start!!!!!!!!!'*10)
    print(proxy_dict)

    response = requests.get("https://ipinfo.io/8.8.8.8/", headers = app.headers, verify = True, proxies = proxy_dict, timeout = 4)
    # print(response.text)