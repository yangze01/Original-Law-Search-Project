#coding: utf-8
import requests
from lxml import etree
from optOnMysql.optOnMysql import *
from Segment.MySegment import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')
BasePath = sys.path[0]
chs_arabic_map = {u'零':0, u'一':1, u'二':2, u'三':3, u'四':4,
        u'五':5, u'六':6, u'七':7, u'八':8, u'九':9,
        u'十':10, u'百':100, u'千':10 ** 3, u'万':10 ** 4,
        u'〇':0, u'壹':1, u'贰':2, u'叁':3, u'肆':4,
        u'伍':5, u'陆':6, u'柒':7, u'捌':8, u'玖':9,
        u'拾':10, u'佰':100, u'仟':10 ** 3, u'萬':10 ** 4,
        u'亿':10 ** 8, u'億':10 ** 8, u'幺': 1,
        u'０':0, u'１':1, u'２':2, u'３':3, u'４':4,
        u'５':5, u'６':6, u'７':7, u'８':8, u'９':9}
def chinese2num (chinese_digits, encoding="utf-8"):
    if isinstance (chinese_digits, str):
        chinese_digits = chinese_digits.decode (encoding)

    result  = 0
    tmp     = 0
    hnd_mln = 0
    for count in range(len(chinese_digits)):
        curr_char  = chinese_digits[count]
        curr_digit = chs_arabic_map.get(curr_char, None)
        # meet 「亿」 or 「億」
        if curr_digit == 10 ** 8:
            result  = result + tmp
            result  = result * curr_digit
            # get result before 「亿」 and store it into hnd_mln
            # reset `result`
            hnd_mln = hnd_mln * 10 ** 8 + result
            result  = 0
            tmp     = 0
        # meet 「万」 or 「萬」
        elif curr_digit == 10 ** 4:
            result = result + tmp
            result = result * curr_digit
            tmp    = 0
        # meet 「十」, 「百」, 「千」 or their traditional version
        elif curr_digit >= 10:
            tmp    = 1 if tmp == 0 else tmp
            result = result + curr_digit * tmp
            tmp    = 0
        # meet single digit
        elif curr_digit is not None:
            tmp = tmp * 10 + curr_digit
        else:
            return result
    result = result + tmp
    result = result + hnd_mln
    return result

web = requests.get("http://www.lawtime.cn/faguizt/23.html")
html = web.text.replace("</p>\r\n<p>\r\n\t", "")
tree = etree.HTML(html)
p_nodes = tree.xpath('//p[@class="f-article-title-tiny"]')
print(u"一共有" + str(len(p_nodes)) + u"项法律条文")

law_key_list = p_nodes[0].xpath('//span[@class="f-article-txt-fb"]/text()')
law_text_list = tree.xpath('//p[@class="f-article-title-tiny"]/text()')
law_value_list = []
for i, item in  enumerate(law_text_list):
    value = item.strip()
    if value != '':
        law_value_list.append(value)
#display top10 item
save_dict = dict()
for j,a in enumerate(zip(law_key_list, law_value_list)):
    # print(j)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    num = chinese2num(a[0][1:-1])
    save_dict[num] = save_dict.get(num, "") +  a[1] + "\n"
doc2vec_train = dict()
doc2vec_train['docs'] = list()
doc2vec_train['labels'] = list()
myseg = MySegment()
for key, value in save_dict.items():
    print(myseg.sen2word(value.encode('utf8')))



opt_connect = OptOnMysql()
for key ,value in save_dict.items():
    try:
        print(key)
        sql = "insert into rule (rule_id, rule_value) values('{0}', '{1}')".format(key, value)
        # print(sql)
        opt_connect.exeQuery(sql)
    except:
        print("error")
opt_connect.connClose()


