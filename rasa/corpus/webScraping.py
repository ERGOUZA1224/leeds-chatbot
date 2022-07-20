import requests
import time
import random
import csv
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from lxml import etree

# 每个子标题的深度不一定都是4级，这里采用递归做深度遍历穷尽
def get_content(url, dict):
    try:
        # 本来不想加的，鉴于对方服务器稳定性差，还是加了随机等待时间，模拟用户访问
        time.sleep(random.randint(5, 10) * 0.1)
        page = session.get(url, headers=headers, timeout=10)
        page.encoding = 'utf-8'
        # print(page.status_code) 仅用于测试获取链接是否成功
        tree = etree.HTML(page.text)
        # 获取当前页面所有子标题
        title_list = tree.xpath('//div[@class="grid js-equalizer"]//div[@class="js-equal grid__item grid__box"]')
        # 如果有子标题，则说明当前页面为中间的子节点（非叶子节点），继续遍历他的所有子节点
        if len(title_list) > 0:
            dict['next'] = []
            for title in title_list:
                d = {}  # 用来存储当前子节点，并与上一级父节点形成关联
                d['title'] = title.xpath('./a/h3/text()')[0]
                dict['next'].append(d)
                href = title.xpath('./a/@href')[0]  # 获取下级子节点的链接，进行深度遍历
                if href[0] == '/':  # 部分链接以//开头，部分直接是https://开头，需对前一个进行处理，否则访问失败
                    href = 'https:' + href
                print(href)
                get_content(href, d)
        else:
            d = {}
            d['title'] = tree.xpath('//h1[@class="heading heading--overview-main"]/text()')[0]
            dict['next'] = d
            # 把所有叶节点的标题和正文存到一个数组里，方便输出
            item = BeautifulSoup(page.text, "html.parser")
            title = tree.xpath('//h1[@class="heading heading--overview-main"]/text()')[0]
            content = item.find('div', class_='document').text.replace('&nbsp;', '')
            a.append([title, content])
    except:
        print("连接超时")

a = []  # 用于存储所有的叶节点标题+正文内容
dict = {'title': 'home'}  # 用于存储所有的子标题，用字典树形结构存储
ua = UserAgent()  # 随机header头
session = requests.session()
url = 'https://ses.leeds.ac.uk/'
headers = {
    'User-Agent': str(ua.random),
    'Cookie': 'PHPSESSID=re5j7qj3pn3rtaogrrkpctc6kqdhdhnp; TEST_COOKIE_NAME=TEST_COOKIE_VALUE; NSC_QTUHSQ_XFC_QSPEVDUJPO2=ffffffff8203a06945525d5f4f58455e445a4a42378b; _gcl_au=1.1.300417691.1656833020; _ga=GA1.3.510630176.1656833020; _gid=GA1.3.1536792503.1656833020; _gat_UA-12466371-1=1',
}   # cookie非必须
get_content(url, dict)

with open("corpus.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for k in a:
        writer.writerow([k[0],k[1]])  # 输出所有的叶节点标题+正文内容
    writer.writerow([dict])  # 输出所有的字典树形结构，实测内容太多了，会被分成多个单元格，需借助在线json进一步做下整理
