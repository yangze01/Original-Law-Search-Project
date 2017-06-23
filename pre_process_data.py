#coding=utf8
import os
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import codecs
BasePath = sys.path[0] + '/test_data/'
# parent,dirnames,filenames in os.walk(BasePath)
dir_list = os.listdir(BasePath)


for dir in dir_list:
    # print(dir)
    with open(BasePath + dir, 'r') as f:
        data = f.read().decode('gbk')
        print(data.split('\n')[5])

















