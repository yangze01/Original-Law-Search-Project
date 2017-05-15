#coding=utf8
import codecs
import requests
import sys
reload(sys)
BasePath = sys.path[0]
sys.setdefaultencoding('utf8')
from lxml import etree
f = requests.get("http://www.zuiming.net/51.html")
content = f.content
print("..............................................")
selector = etree.HTML(content.decode('utf8'))
content_filed = selector.xpath('//*[@id="post-51"]/div[2]/table/tbody/tr[*]/td[2]/a/@title')
print(len(content_filed))
save_file = open(BasePath + "/criminal.txt", 'w')
print(BasePath + "/criminal.txt")
save_file.write('\n'.join(content_filed).encode('utf8'))
print("finished")