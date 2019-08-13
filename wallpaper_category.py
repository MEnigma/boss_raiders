import requests
from lxml import etree


def headers():
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        #'Cookie': 'ip_ck=7sWB4vL1j7QuOTIwNTgyLjE1NjU3MDA5NDg%3D; lv=1565700951; vn=1; z_pro_city=s_provice%3Dbeijing%26s_city%3Dbeijing; questionnaire_pv=1565654401;Hm_lvt_ae5edc2bc4fc71370807f6187f0a2dd0=1565700951; Hm_lpvt_ae5edc2bc4fc71370807f6187f0a2dd0=1565700951',
        'Host': 'sj.zol.com.cn',
        'If-Modified-Since': 'Tue, 13 Aug 2019 09:52:12 GMT',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }

def get_category_list():
    response = requests.get("http://sj.zol.com.cn/bizhi/", headers=headers())
    print(response)
    html_code = response.text
    print(html_code)
    html_element = etree.HTML(html_code)
    tags = html_element.xpath("//dd[@class='brand-sel-box clearfix']/a")
    print(tags)

get_category_list()

