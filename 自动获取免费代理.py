import  requests
from lxml import etree
import csv

class GetIp(object):

    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
        }
        self.html = ""
        self.ip_pool = []

    def get_html(self):
        try:
            response = requests.get(url=self.url, headers=self.headers)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            self.html = response.text
            # print(self.html)
        except Exception as e:
            print(e)


    def parse_html(self):
        # 实例化一个标签树
        tree = etree.HTML(text=self.html)
        # 根据xpath来定位标签
        tr_tag = tree.xpath('//tbody/tr')
        # 获取标签内容
        for tr in tr_tag:
            tr_dict = {
                'ip': tr.xpath('./td[1]/text()')[0],
                'port': tr.xpath('./td[2]/text()')[0],
                'method': tr.xpath('./td[4]/text()')[0]
            }
            self.ip_pool.append(tr_dict)




    def save_data(self):
        # 1、打开一个csv文件获取文件句柄
        with open('proxies_data.csv', 'a', newline='', encoding='utf-8-sig') as f:
            # 2、实例化csv写手对象
            csv_writer = csv.DictWriter(f, fieldnames=['ip', 'port', 'method'])
            # 3、写入数据
            csv_writer.writerows(self.ip_pool) # ["", "", "", ...]
    def run(self):
        self.get_html()
        self.parse_html()
        self.save_data()


if __name__ == '__main__':
    g = GetIp(url="https://www.kuaidaili.com/free/inha/")
    g.run()