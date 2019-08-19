import requests
import pandas as pd
import os
from lxml import etree
from ippool import IPPools
import time


class BossJobModel:
    title = None
    salary = None
    adress = None
    experi = None
    educate = None
    company = None
    company_type = None
    company_statue = None
    company_size = None
    hr_job = None
    hr_name = None
    hr_head = None

    def toDict(self):
        return {
            'title' : self.title,
            'salary' : self.salary,
            'adress' : self.adress,
            'experi' : self.experi,
            'educate' : self.educate,
            'company' : self.company,
            'company_type' : self.company_type,
            'company_statue' : self.company_statue,
            'company_size' : self.company_size,
            'hr_job' : self.hr_job,
            'hr_name' : self.hr_name,
            'hr_head' : self.hr_head,
        }


class BossSpider:

    ip_pool = IPPools()
    job_list = []
    last_request_time = None

    def makeUrl(self, page=1, category='c101010100-p100199'):
        if page <= 1:
            return "https://www.zhipin.com/{}/".format(category)
        else:
            return "https://www.zhipin.com/{}/?page={}".format(category, page)

    def headers(self):
        return {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': '_uab_collina=155305913216567736648592; lastCity=101010100; _bl_uid=gejz5zj790mmy60Ckx7RxzykspCR; JSESSIONID=""; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1565687647,1565748170,1565922676,1566209124; __c=1566209124; __g=-; __l=l=%2Fwww.zhipin.com%2F&r=; __zp_stoken__=c839siC63ueeCcCCNBQc%2F0bBbQDRW9S35RLqvXzQIW3ZVDA3E523rfzUwbyVVjYSgX%2FqupbHL5mMWAGUFzl1XsCpiA%3D%3D; __a=21201824.1553059131.1565922676.1566209124.221.17.3.221; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1566209215',
            'sec-fetch-mode': 'navigate',
            'referer': 'https://www.zhipin.com/web/common/security-check.html?seed=V6mIAvvU3v6Aha3JvLMcKpnX2d9eKeNc4UPcuQvkuck%3D&name=d3f4b0ad&ts=1566209213463&callbackUrl=%2Fc101010100-p100199%2F%3Fpage%3D200%26ka%3Dpage-200',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        }
    def getCategoryList(self):
        response = requests.get("https://www.zhipin.com",headers=self.headers())
        response.encoding = 'utf-8'
        html_element = etree.HTML(response.text)
        tags = html_element.xpath("//div[@class='text']/a")
        group = []
        for tag in tags:
            title = tag.xpath("text()")[0]
            category = tag.xpath("@href")[0]
            group.append({
                "title":title,
                "url":category,
                "page":1,
                "finished":False
            })
        pd.DataFrame(group).to_csv("category.csv")

    def proxies(self):
        randomip = self.ip_pool.randomIp()
        return {
            "http": randomip,
            "https": randomip,
        }

    def fetchIndexPageInf(self, page=1, category="c101010100-p100199"):
        """
        获取当前页码求职资料
        """
        print("开始沉睡,防止ip封禁",end='    ')
        if page > 1:
            time.sleep(15)
        response = requests.get(url=self.makeUrl(page=page, category=category), headers=self.headers())
        print(response.url)
        response.encoding = 'utf-8'
        html_code = response.text
        html_element = etree.HTML(html_code)
        joblist = html_element.xpath("//div[@class='job-list']/ul/li/div[@class='job-primary']")
        print("{}页有 {} 条职位信息".format(page, len(joblist)))
        index_group = []
        if len(joblist) == 0:
            print(" ------ WARNNING ------")
            print(html_code)
            return;
        for card in joblist:
            model = BossJobModel()
            model.title = card.xpath("div[@class='info-primary']/h3/a/div[1]/text()")[0]
            model.salary = card.xpath("div[@class='info-primary']/h3/a/span/text()")[0]
            expands = card.xpath("div[@class='info-primary']/p/text()")
            if len(expands) == 3:
                model.adress = expands[0]
                model.experi = expands[1]
                model.educate = expands[2]
            else:
                model.adress = ""
                model.experi = ""
                model.educate = ""
            model.company = card.xpath("div[@class='info-company']/div/h3/a/text()")[0]
            company_expand = card.xpath("div[@class='info-company']/div/p/text()")
            if len(company_expand) == 3:
                model.company_type = company_expand[0]
                model.company_statue = company_expand[1]
                model.company_size = company_expand[2]
            else:
                model.company_type = ''
                model.company_statue = ''
                model.company_size = ''
            model.hr_head = card.xpath("div[@class='info-publis']/h3/img/@src")[0]
            hr_expand = card.xpath("div[@class='info-publis']/h3/text()")
            if len(hr_expand) == 2:
                model.hr_name = hr_expand[0]
                model.hr_job = hr_expand[1]
            else:
                model.hr_name = ''
                model.hr_job = ''
            
            # self.job_list.append(model.toDict())
            index_group.append(model.toDict())
        
        next_page = html_element.xpath("//a[@class='next disabled']")
        if os.path.exists(os.path.join(os.path.dirname(__file__),category)) == False:
            os.makedirs(os.path.join(os.path.dirname(__file__),category))
        if len(next_page) > 0:
            print("没有下一页,数据获取结束,执行写入操作...", end='  ')
            # dbframe = pd.DataFrame(self.job_list)
            dbframe = pd.DataFrame(index_group)
            dbframe.to_csv("{}/{}-{}.csv".format(category,page,category))
            print("写入完成")
        else:
            dbframe = pd.DataFrame(index_group)
            dbframe.to_csv("{}/{}-{}.csv".format(category,page,category))
            print("写入完成")
            print("下一页查取 page:{}".format(page))

            self.fetchIndexPageInf(page=page+1,category=category)

            
def read():
    form = pd.read_csv('category.csv')    
    data_group = [dict(zip(form.keys().tolist(),val.tolist()))for val in form.values]
    for data in data_group:
        cate = data['url']
        cate = cate.replace("/",'')
        
        BossSpider().fetchIndexPageInf(category=cate)


read()