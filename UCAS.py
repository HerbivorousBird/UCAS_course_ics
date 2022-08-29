import requests
from lxml import etree
import re


class classes:

    def __init__(self):
        # 懒得异常处理
        try:
            with open('选择课程-选课系统.html',encoding='UTF-8') as f:
                html = etree.HTML(f.read())
                self.tbody = html.xpath(
                    '/html/body/div[3]/div/div[3]/div[2]/table/tbody')[0]
        except Exception as e:
            print('检查目录下是否存在“选择课程-选课系统.html”。如果还有问题，新生群里问吧')

    def get_classes(self):
        classes_list = []
        for tr in self.tbody.xpath('tr'):
            name, teacher, url = tr.xpath('td[2]/a/text()')[0], tr.xpath('td[7]/a/text()')[0], tr.xpath('td[2]/a/@href')[0]
            attr_list = self._get_class_attr(url)
            for attr in attr_list:
                classes_list.append([name,teacher]+attr)
        return classes_list

    def _get_class_attr(self, url):
        headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        }
        res = requests.get('https://jwxk.ucas.ac.cn'+url,headers=headers)
        html = etree.HTML(res.text)
        tbody = html.xpath('/html/body/div[2]/div/div[2]/div[2]/table/tbody')[0]
        tds = tbody.xpath('tr/td')
        
        attr_list = []
        for i in range(len(tds)//3):
            re_ = re.search('星期(.)： 第([0-9、]+)节。', tds[i*3+0].text)
            class_weekday,class_time = '空一二三四五六日'.index(re_[1]),[int(i) for i in re_[2].split('、')]
            class_loc = tds[i*3+1].text
            class_week = [int(i) for i in tds[i*3+2].text.split('、')]
            attr_list.append([class_loc,class_week,class_weekday,class_time])
        return attr_list


class school:	

	name = "UCAS"

	classTime = [
		(8, 30),
		(9, 20),
		(10, 30),
        (11, 20),
		(13, 30),
		(14, 20),
		(15, 30),
		(16, 20),
		(18, 10),
		(19, 00),
		(20, 10),
		(21, 00)
	]                         
	classPeriod = 50     
	starterDay = [2022, 8, 22]


if __name__ == '__main__':
    print(classes().get_classes())