#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from optOnMysql.DocumentsOnMysql import *
from optOnMysql.DocumentUnit import *
import json
BasePath = sys.path[0]

def document_format(line):

    line = json.loads(line.decode('utf8'))
    document_unit = dict()
    document_unit["title"] = line['title']
    # print(len(document_unit['title']))
    document_unit["court"] = line['court']
    document_unit["url"] = line['url']
    document_unit["content"] = '|'.join(line['content'])
    # print(len(document_unit["content"]))
    document_unit["criminal"] = u'过失致人死亡罪'
    document_unit["date"] = line['date']
    return document_unit

def read_document(file_path):
    opt = DocumentsOnMysql()
    i = 0
    for line in open(file_path):

        print(i)
        i = i + 1
        document_unit = document_format(line)
        opt.insertOneDocuments(document_unit)
    opt.connClose()




if __name__ == "__main__":
    # opt = DocumentsOnMysql()
    # opt.insertOneDocuments(document_unit)
    # print(opt)
    # opt.findById("1")
    # a = opt.findall()
    # for i in a :
        # print(i)
    # opt.connClose()
    file_path =  BasePath + "/data/judgment_Death_by_obsolescence.txt"
    read_document(file_path)
    print(1)