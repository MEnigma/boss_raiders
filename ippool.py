import requests
import re
import os
import pandas as pd
from lxml import etree


class IPPools:
    ip_pool = []
    location = 0
    page = 1

    def __init__(self):
        try:
            iplist: pd.DataFrame = pd.read_csv('iplist.csv')
            self.ip_pool = iplist.values.tolist()
        except Exception as e:
            print("初始化 csv文件转换操作失败： {}".format(e))
            pass
        
        try:
            with open("page.a", 'r+') as page_record:
                page_str = "1"
                try:
                    page_str = page_record.readline()
                except Exception as e:
                    pass
                self.page = int(page_str)
        except Exception as e:
            pass

    def chooseIp(self,):
        self.location+=1
        if self.location >= len(self.ip_pool):
            print("当前ip池数量不足，将进行爬取...")
            os.remove("iplist.csv")
            self.ip_pool = None
            self.ip_pool = []
            self.location = 0
            self.fetchPage(page=self.page)

        infs: list = self.ip_pool[self.location]
        return "http://{}:{}".format(infs[1], infs[2])

    def verifyIpPoolCount(self,):
        if(len(self.ip_pool)==0):
            self.fetchPage(page=self.page)

    def makeUrl(self, page = 1):
        if page <= 1:
            return "https://www.kuaidaili.com/free/inha/"
        else :
            return "https://www.kuaidaili.com/free/inha/{}/".format(page)
    
    def makeHeaders(self):
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'channelid=0; sid=1565699763795455; _ga=GA1.2.1929640738.1565701483; _gid=GA1.2.891005545.1565701483; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1565701483; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1565701497',
            'Host': 'www.kuaidaili.com',
            'Referer': 'https://www.kuaidaili.com/free/inha/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def fetchPage(self, page=1):
        response = requests.get(url=self.makeUrl(page=page),headers=self.makeHeaders())
        html_code = response.text
        html_element = etree.HTML(html_code)
        trs = html_element.xpath("//div[@id='list']/table/tbody/tr")
        for tr in trs:
            tds_text = tr.xpath("td/text()")
            tds_title = tr.xpath("td/@data-title")
            res = dict(zip(tds_title,tds_text))
            try:
                speed = re.search("\d*.?\d+",res['响应速度']).group(0)
                if float(speed) > 2.0:
                    continue
                res['响应速度'] = speed
            except Exception as e:
                print(format(e))
            print("开始验证ip.....",end='  ')
            if self.verifyIpAvailable(res['IP'], res['PORT']):
                print("验证结束，可用")
                self.ip_pool.append(res)
            else:
                print("验证结束，不可用")

            
        print("当前以采集ip :{} 条".format(len(self.ip_pool)))
        if len(self.ip_pool) < 100:
            print("开始采集第{}页".format(page))
            self.fetchPage(page=page+1)
        else:
            try:
                with open("page.a", 'w+') as page_record:
                    page_record.write(page)
            except Exception as e:
                pass

            try:
                pd.DataFrame(self.ip_pool).to_csv("iplist.csv")
            except Exception as e:
                pass

    def verifyIpAvailable(self, ip, port) -> bool:
        """
        @return 验证代理ip是否可用
        """
        proxies = {
            "http": "http://{}:{}".format(ip, port)
        }
        try:
            resposne = requests.get(url='https://www.baidu.com/', proxies=proxies, timeout=2)
            return resposne.status_code == 200
        except Exception as e:
            return False


ippool = IPPools()
print(ippool.chooseIp())