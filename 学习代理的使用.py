"""
爬虫思路
        一、数据来源分析
            1、爬什么（需求分析）
                -获取IP的归属地
                -ip值
            2、去哪爬（接口分析）
                静态的 url = "https://ip.900cha.com/"


        二、爬虫代码实现
            1、发送请求
            2、获取数据
            3、解析数据
            4、保存数据


"""
import csv

import lxml
import requests
from lxml import etree
import 自动获取免费代理 as auto_get

# 定义爬虫类
class IpCha(object):

    def __init__(self, url):   # 当实例化一个爬虫对象时用
        self.url = url
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
        }
        self.html = ""
        self.proxies = {}
        self.ip_pool = []

    def get_html(self):
        while True:
            try:
                response = requests.get(url=self.url, headers=self.headers, proxies=self.proxies)
                response.raise_for_status()  # 根据状态码抛出异常
                response.encoding = response.apparent_encoding
                self.html = response.text
                break
            except Exception as e:
                print(e)
                self.ip_pool.pop(0)

    def parse_html(self):
        try:
            # 1、实例化一个标签树
            tree = etree.HTML(text=self.html)
            # 2、根据XPath语法取定位标签
            li_tag = tree.xpath('//ul[@class="list-unstyled"]/li')
            # 3、获取标签内容
            for li in li_tag:
                s = li.xpath('./text()')[0].strip()
                print(s)
        except Exception as e:
            print(e)


    def get_ip_pool(self):
        g = auto_get.GetIp(url="https://www.kuaidaili.com/free/inha/")
        g.run()
        with open('proxies_data.csv', 'r', encoding='utf-8-sig') as f:
            # 1、实例化csv读取器
            csv_reader = csv.DictReader(f, fieldnames=['ip', 'port', 'method'])
            self.ip_pool = list(csv_reader)
            # 2、读取文件
            for row in csv_reader:
                # print(row['ip'])
                # print(row['port'])

                ip = row['ip']
                port = row['port']
                method = row['method']
                self.proxies = {
                    "http": f"{method}://{ip}:{port}",
                    "https": f"{method}://{ip}:{port}"
                }

    def run(self):
        # 发送请求，获取数据
        self.get_html()
        self.parse_html()
        self.get_ip_pool()


if __name__ == '__main__':
    # 实例化爬虫对象
    p = IpCha(url="https://ip.900cha.com/")
    p.run()
    # 执行爬虫