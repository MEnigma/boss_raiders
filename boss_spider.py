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
            'cookie': 'lastCity=101010100; _uab_collina=156509435369098913376332; __c=1566223014; __g=-; __l=l=%2Fwww.zhipin.com%2F&r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D3T-D7CFZorMLSfk37tqPEyhS6yLRDVihE5X3sdui0bxtSJOCp_EkcNdU092DXGCt%26wd%3D%26eqid%3Da07fedd300028c1a000000025d5aaaa0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1565094354,1565404726,1566223014; __zp_stoken__=c839QoxxJZbv9ctb1NDfYpQhUs6hC%2FN0h%2FA9mzYComOHIUGhsdRtEZSt1wke6zcqG74neN1kBLXy1Lk4bbuHYkoogA%3D%3D; __a=1712998.1565094354.1565404726.1566223014.25.3.4.25; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1566223347',
            'referer': 'https://www.zhipin.com/web/common/security-check.html?seed=QbRi4A+65gFWRajo+UKSDq4LoKJTgLKoBbORaTUGx9o=&name=d3f4b0ad&ts=1566223304539&callbackUrl=/c101010100-p100199/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
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
        print(">> {}page got {} list of job info".format(page, len(joblist)))
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
        current_category_path = os.path.join(os.path.dirname(__file__),category)
        print("CATEGORY PATH {} exists:{}".format(current_category_path,os.path.exists(current_category_path)))
        if os.path.exists(current_category_path) == False:
            print("MENTION  no categoy dir ,will create")
            os.makedirs(current_category_path)
        export_file_name = "{}/{}-{}.csv".format(category,page,category)
        export_file_name = os.path.join(os.path.dirname(__file__),export_file_name)
        
        if len(next_page) > 0:
            print("no next page and will do final write", end='  ')
            # dbframe = pd.DataFrame(self.job_list)
            dbframe = pd.DataFrame(index_group)
            dbframe.to_csv(export_file_name)
            print("WIRTE DONE")
        else:
            dbframe = pd.DataFrame(index_group)
            dbframe.to_csv(export_file_name)
            print("WRITE DONE")
            print("SHOULD FETCH NEXT page:{}".format(page))

            self.fetchIndexPageInf(page=page+1,category=category)

            
def read():
    categoryname = "category.csv"
    file_path = os.path.join(os.path.dirname(__file__),categoryname)
    print("file path :{}".format(file_path))
    form = pd.read_csv(file_path, encoding='utf-8')    
    data_group = [dict(zip(form.keys().tolist(),val.tolist()))for val in form.values]
    for data in data_group:
        cate = data['url']
        cate = cate.replace("/",'')
        if data['finished'] == True:
            continue
        print("will fetch   category:{}  code:{}".format(data['title'],cate))
        BossSpider().fetchIndexPageInf(category=cate)


read()