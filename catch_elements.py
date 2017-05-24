#coding=utf8
import os
import re
import sys
import json
from optOnMysql.optOnMysql import *#
from Segment.MySegment import *
import jieba.analyse

reload(sys)
sys.setdefaultencoding('utf8')
BasePath = sys.path[0]
from optOnMysql import *
#define global variable for saving file name,identify how many items was successfully find
# with open(BasePath + '/criminal.txt','r') as f:
#     content = f.read()
#     criminal_set = content.split()
# print(' '.join(criminal_set))
def get_prosecutor(document):

    pattern_person = re.compile(u"(原告）|原告人）|起诉方）|公诉机关）|原告|原告人|起诉方|公诉机关)(.*?)(，|。)")
    search_result = re.search(pattern_person, document)#research-->find???
    if search_result:
        return search_result.group(2),1
    else:
        return "unclear",0
        # return "", 0

def get_prosecutor_detail(document):
    pattern_person = re.compile(u"(原告|原告人|起诉方|公诉机关).*?\。")
    search_result = re.search(pattern_person, document) # research-->find???
    if search_result:
        return search_result.group(),1
    else:
        return "unclear",0
        # return "", 0

def get_appellee(document):
    pattern_person = re.compile(u"(被告人）|被诉方）|罪犯）|被告人|被诉方|罪犯)(.*?)(，|。)")
    search_result = re.search(pattern_person, document) #research-->find???
    if search_result:
        return search_result.group(2), 1
    else:
        return "unclear",0
        # return "", 0

def get_appellee_detail(document):
    pattern_person = re.compile(u"(被告人|被诉方|罪犯).*?\。")
    search_result = re.search(pattern_person, document) #research-->find???
    if search_result:
        return search_result.group(),1
    else:
        return "unclear",0
        # return "", 0

def get_reason(document):
    pattern_character = re.compile(u"(危险驾驶|交通肇事|诈骗|非法拘禁|故意杀人)")
    search_result = re.search(pattern_character, document)
    if search_result:
        return search_result.group(), 1
    else:
        return "empty",0
        # return "", 0

def get_type(document):
    pattern_character = re.compile(u"(刑事|民事|刑事附带民事)")
    search_result = re.search(pattern_character, document)
    if search_result:
        return search_result.group(),1
    else:
        return "empty",0
		# return "",0

def get_character(document):
    pattern_character = re.compile(u"(民事判决书|民事裁定书|民事调解书|民事决定书|民事制裁决定书|刑事判决书|刑事裁定书|刑事附带民事判决书|刑事申诉状|刑事自诉案件反诉状|刑事反诉状|刑事答辩状|刑事自诉状|刑事上诉状)")
    search_result = re.search(pattern_character, document)
    if search_result:
        return search_result.group(),1
    else:
        return "empty",0
	    # return "", 0
def get_judge(document):
    pattern_person = re.compile(u"(法官|审判长)(.*?)(代理审判员|助理审判员|审判员)")
    search_result = re.search(pattern_person, document)#research-->find???
    if search_result:
        return search_result.group(2),1
    else:
        return "empty",0
        # return "", 0
def	get_judex(document):
    pattern_person = re.compile(u"(代理审判员|助理审判员)(.*?)(代理审判员|助理审判员|一九九|二〇一|二〇〇|，|。)")
    search_result = re.search(pattern_person, document)#research-->find???
    if search_result:
        return search_result.group(2),1
    else:
        return "empty",0
        # return "", 0
def	get_recorder(document):
    pattern_person = re.compile(u"书记员(.*?)($|附相关|附：|。)")
    search_result = re.search(pattern_person, document)#research-->find???
    if search_result:
        return search_result.group(1),1
    else:
        return "empty",0
	    # return "", 0

def get_inquisition(document):
    pattern_details = re.compile(u"(.*)(201|199|200)(.*?)(现已审理终结|已审理|审理终结)(.*?)\。")
    search_result = re.search(pattern_details, document)
    if search_result:
        return search_result.group(),1
    else:
        return document[0:3*200],1
	
def get_behavior(document):
    # pattern_behavior = re.compile(u"(本院认为).*?\。")
    pattern_behavior = re.compile(u"(本院认为|本院认定|本院裁定)(.*)依照")
    search_result = re.search(pattern_behavior, document) #
    if search_result:
        return search_result.group(1)+search_result.group(2),1
    else:
        # return "empty",0
        return document[0:3*200], 0

def get_confession_of_defense(document):
    pattern_behavior = re.compile(u"(被告人供诉与辩解|被告人供诉|被告人辩解|被告供诉与辩解|被告辩解|被告供诉).*?\。")
    search_result = re.search(pattern_behavior, document) #
    if search_result:
        return search_result.group(),1
    else:
        return "empty",0
def get_facts_and_evidence(document):
    pattern_behavior = re.compile(u"(指控事实及证据|指控事实|指控证据).*?\。")
    search_result = re.search(pattern_behavior, document) #
    if search_result:
        return search_result.group(),1
    else:
        return "empty",0

def get_advocate(document):
    pattern_behavior = re.compile(u"(辩护人意见：|辩护意见：|辩护观点|辩护人观点).*?\。")
    search_result = re.search(pattern_behavior, document) #
    if search_result:
        return search_result.group(),1
    else:
        return "empty",0

def get_level(document):
    pattern_3 = re.compile(u"(三审|第三审|终审)")
    pattern_2 = re.compile(u"(第二审|二审)")
    pattern_1 = re.compile(u"(第一审|一审)")
    search_result_3 = re.search(pattern_3, document)
    search_result_2 = re.search(pattern_2, document)
    search_result_1 = re.search(pattern_1, document)
    if search_result_3:
        return search_result_3.group(),1
    elif search_result_2:
        return search_result_2.group(),1
    elif search_result_1:
        return search_result_1.group(),1
    else:
        return "unknown",0

def get_result(document):
    pattern_result = re.compile(u"(判决如下|裁定如下|判处如下|决定如下|判决意见如下).*?(如不服)")
    search_result = re.search(pattern_result, document)
    if search_result:
        return search_result.group(),1
    else:
        pattern_result = re.compile(u"(判决如下|裁定如下|判处如下|决定如下|判决意见如下).*?\。")
        search_result = re.search(pattern_result, document)
        if search_result:
            return search_result.group(),1
        else:
            return "empty", 0

def get_details(document):
    pattern_details = re.compile(u".*?(上述事实).*?\。")
    search_result = re.search(pattern_details, document)
    if search_result:
        return search_result.group(),1
    else:
        return document[0:3*200],0

def get_(document):
    pattern_details = re.compile(u".*?().*?\。")
    search_result = re.search(pattern_details, document)
    if search_result:
        return search_result.group(),1
    else:
        return document[0:3*200],0

def read_document(file_path):
    return_document = list()
    i = 0
    for line in open(file_path):
        # f.write(i)
        #i += 1
        #if i==3:break
        line = json.loads(line.decode('utf8'))
        #f.write(type(line)) dict        
        #f.write(len(line))  2
        # decode = ''.join(line['content'])
        # decode_line = ''.join(decode.split())
        decode_line = '|'.join(line['content'])
        line.pop('content')

        newline = {}
        # print(line.items())

        for key,value in line.items():
            try:
                #value.decode('utf8')
                value=''.join(value)
                value.decode('utf8')
                newline[key] = value
                # f.write(decode_line)
            except:
                continue
        return_document.append((decode_line.decode('utf8'), newline))
        
    return return_document
def get_abstract(content, document):
    if(content):
        abstract = content[content.find('。') + 1:content.find('。', content.find('。') + 200) + 1]
    else:
        abstract = document[document.find('。') + 1:document.find('。', document.find('。') + 200) + 1]

    # abstract = content[0:content.find('。',content.find('。')+100)]
    return abstract



if __name__ == "__main__":
    filepath_list = [BasePath + "/data/judgment.txt", \
                     BasePath + "/data/judgment_Death_by_obsolescence.txt", \
                     BasePath + "/data/judgment_kill.txt", \
                     BasePath + "/data/judgment_negligence_caused_serious_injury.txt", \
                     BasePath + "/data/judgment_robbery.txt", \
                     BasePath + "/data/judgment_scam.txt", \
                     BasePath + "/data/judgment_trafficking.txt"]
    # criminal_list = ['交通肇事罪',  # 危险驾驶罪（危险 驾驶罪）
    #                  '过失致人死亡罪' # 故意杀人罪（故意 杀人 杀人罪） 故意伤害罪（故意 伤害 伤害罪）
    #                   '故意杀人罪'
    #                   '故意伤害罪'
    #                   '过失致人重伤罪'，
    #                   ‘抢劫罪’,
    #                   '诈骗罪', #（诈骗 诈骗罪 诈骗案）
    #                   '拐卖妇女儿童罪'
    #                   ]
    file_path = filepath_list[6] # BasePath + "/data/judgment_scam.txt"
    word1 = '拐卖'
    word2 = '拐卖'
    word3 = '拐卖'
    criminal_data = "拐卖妇女儿童罪"

    count_total = 0
    document_list = read_document(file_path)
    i = 0
    opt_connect = OptOnMysql()
    myseg = MySegment()
    # test = opt_connect.exeUpdate("update document set keywords = '{0}' where _id = '{1}'".format("测试,插入,数据",1))
    # j = 0
    for (document,dit_line) in document_list:
        # j += 1
        # if(i<115):
        #     continue

        count_total = 0
        document1  = document.replace('|','')
        if(document1):
            save_dict = dict()
            save_dict['title'] = dit_line['title'] # varchar(200)
            title_word_list = myseg.sen2word(dit_line['title'].encode('utf8'))

            if word1 not in set(title_word_list) and word2 not in set(title_word_list):
                # print("continue")
                print(' '.join(title_word_list))
                continue
            save_dict['court'] = dit_line['court'] # varchar(200)
            save_dict['case_num'] = dit_line['document_code'] # varchar(200)
            save_dict['date'] = dit_line['date']  # date

            # 案件类型
            doc, count = get_type(dit_line['title'])
            count_total += count
            save_dict['type'] = doc # varchar(200)

            # 案由
            doc, count = get_reason(dit_line['title'])
            count_total += count
            save_dict['case_reason'] = doc # varchar(200)

            #法官
            doc, count = get_judge(document1)
            count_total += count
            save_dict['judge'] = doc # varchar(200)

            # 审级
            doc, count = get_level(document1)
            count_total += count
            save_dict['case_level'] = doc # varchar(200)

            # 原告
            doc, count = get_prosecutor(document1)
            count_total += count
            save_dict['prosecutor'] = doc # varchar(200)

            # 被告
            doc, count = get_appellee(document1)
            count_total += count
            save_dict['appellee'] = doc # varchar(200)

            # 文书性质
            doc, count = get_character(document1)
            count_total += count
            save_dict['case_type'] = doc # varchar(200)

            # 原告信息
            doc, count = get_prosecutor_detail(document1)
            count_total += count
            save_dict['prosecutor_detail'] = doc # varchar(200)

            #被告信息
            doc, count = get_appellee_detail(document1)
            count_total += count
            save_dict['appellee_detail'] = doc # varchar(200)

            # 地址
            save_dict['url'] = dit_line['url'] # varchar(200)

            # 审理经过
            doc, count = get_inquisition(document1)
            count_total += count
            save_dict['inquisition'] = doc # longtext

            # 指控事实及证据
            doc, count = get_facts_and_evidence(document1)
            count_total += count
            save_dict['facts_and_evidence'] = doc # longtext

            # 被告人供诉及辩解
            doc, count = get_confession_of_defense(document1)
            count_total += count
            save_dict['confession_of_defense'] = doc # longtext

            # 辩护人意见
            doc, count = get_advocate(document1)
            count_total += count
            save_dict['advocate'] = doc # longtext

            # 查明事实
            doc, count = get_details(document1)
            count_total += count
            save_dict['details'] = doc # longtext
            key_word_tfidf = jieba.analyse.extract_tags(doc, topK=10, withWeight=False,
                                                        allowPOS=('ns', 'n', 'vn', 'v'))
            key_words = ',' + ','.join(key_word_tfidf) + ','
            save_dict['keywords'] = key_words  # varchar(10000)
            save_dict['abstract'] = get_abstract(doc, document1) # varchar(2000)

            #裁判理由
            doc, count = get_behavior(document1)
            count_total += count
            save_dict['judge_reason'] = doc # longtext


            # 裁判结果
            doc, count = get_result(document1)
            count_total += count
            save_dict['judgment_result'] = doc # middletext

            #裁判人员
            doc, count = get_judex(document1)#
            count_total += count
            save_dict['judgment_people'] = doc # varchar(200)
#
            # 书记员
            doc, count = get_recorder(document1)
            count_total += count
            save_dict['recoder'] = doc.strip() # varchar(200)

            # 正文
            save_dict['content'] = document # longtext
            # 罪名
            save_dict['criminal'] = criminal_data.encode('utf8') # varchar(2000)

            # COLstr1 = ''
            # ROWstr1 = ''
            # print(count_total)
            # title_word_list = myseg.sen2word(dit_line['title'].encode('utf8'))
            # if count_total > 12 and ('交通' in set(title_word_list) or '交通' in set(title_word_list)):
            # if '交通' in set(title_word_list) or '交通' in set(title_word_list):
            if (word1 in set(title_word_list) and word2 in set(title_word_list)) or (word1 in set(title_word_list) and word3 in set(title_word_list)):
                print(i)
                i = i + 1
                # if(i < 127):# 165
                #     continue
                COLstr = list()
                ROWstr = list()
                for key in save_dict.keys():
                    COLstr.append(key)
                    ROWstr.append('"' + save_dict[key].encode('utf8') + '"')
                try:
                    sql = "insert into document ({0}) values ({1})".format(','.join(COLstr), ','.join(ROWstr))
                    opt_connect.exeQuery(sql)
                except:
                    continue
    myseg.close()
    opt_connect.connClose()

    # insert
    # into
    # document (appellee_detail, abstract, date, case_num, keywords, confession_of_defense, case_reason, appellee,
    #          case_level, court, title, facts_and_evidence, content, details, prosecutor_detail, criminal, type,
    #          prosecutor, inquisition, recoder, advocate, judge, url, judge_reason, case_type, judgment_result,
    #          judgment_people, )
    # values("", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", )

            # print(len(ROWstr.split(',')))
            # print('\n'.join(ROWstr.split(',')))

            # for key, value in save_dict.items():
            #     print(key)
            #     print(value)

            # with open(BasePath + "/data_make/"+str(i)+".txt",'w') as f:#全部被处理文件保存位置
            #     f.write("[标题]".decode('utf8'))
            #     f.writelines('\n')
            #     f.write(dit_line['title'])
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("[案件基本信息]".decode('utf8'))
            #     f.writelines('\n')
            #     f.write("审理法院：".decode('utf8'))
            #     f.write(dit_line['court'])
            #     f.writelines('\n')
            #     f.write("案    号：".decode('utf8'))
            #     f.write(dit_line['document_code'])
            #     f.writelines('\n')
            #
            #
            #     f.write("案件类型：".decode('utf8'))
            #     doc,count = get_type(dit_line['title'])
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.write("案    由：".decode('utf8'))
            #     doc,count = get_reason(dit_line['title'])
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.write("裁判日期：".decode('utf8'))
            #     f.write(dit_line['date'])
            #     f.writelines('\n')
            #     f.write("法    官：".decode('utf8'))
            #     doc,count = get_judge(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.write("审级：".decode('utf8'))
            #     doc,count = get_level(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.write("原    告：".decode('utf8'))
            #     doc,count = get_prosecutor(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.write("被    告：".decode('utf8'))
            #     doc,count = get_appellee(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.write("文书性质：".decode('utf8'))
            #     doc,count = get_character(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.write("[案例要旨]")
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("[正文]".decode('utf8'))
            #     f.writelines('\n')
            #     f.write("当事人信息".decode('utf8'))
            #     f.writelines('\n')
            #     doc,count = get_prosecutor_detail(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     doc,count = get_appellee_detail(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("审理经过".decode('utf8'))
            #     f.writelines('\n')
            #     doc,count = get_inquisition(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("指控事实及证据".decode('utf8'))###########
            #     f.writelines('\n')
            #     doc,count = get_facts_and_evidence(document)
            #     count_total += count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("被告人供诉与辩解".decode('utf8'))###################
            #     f.writelines('\n')
            #     doc,count = get_confession_of_defense(document)
            #     count_total += count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("辩护人意见".decode('utf8'))
            #     f.writelines('\n')
            #     doc,count = get_advocate(document)
            #     count_total += count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("查明事实".decode('utf8'))
            #     f.writelines('\n')
            #     doc,count = get_details(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("裁判理由".decode('utf8'))
            #     f.writelines('\n')
            #     doc,count = get_behavior(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("裁判结果".decode('utf8'))
            #     f.writelines('\n')
            #     doc,count = get_result(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("审判人员".decode('utf8'))
            #     f.writelines('\n')
            #     doc,count = get_judex(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("裁判日期".decode('utf8'))
            #     f.writelines('\n')
            #     f.write(dit_line['date'])
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("书记员".decode('utf8'))
            #     f.writelines('\n')
            #     doc,count = get_recorder(document)
            #     count_total+=count
            #     f.write(str(doc))
            #     f.writelines('\n')
            #     f.writelines('\n')
            #     f.write("===========================================")
            #     f.close()
            #
            #     if count_total>15:
            #         os.system ("copy %s %s" % ("E:\\Sifa\\scam\\"+str(i)+".txt", "E:\\Sifa\\scam_count\\"+str(i)+".txt"))#后一个是挑选出来的
            #

