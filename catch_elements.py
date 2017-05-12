#coding=utf8
import os
import re
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')
BasePath = sys.path[0]
#define global variable for saving file name,identify how many items was successfully find

def get_prosecutor(document):

	pattern_person = re.compile(u"(原告）|原告人）|起诉方）|公诉机关）|原告|原告人|起诉方|公诉机关)(.*?)(，|。)")
	search_result = re.search(pattern_person, document)#research-->find???
	if search_result:
		return search_result.group(2),1
	else:
		return "unclear",0

def get_prosecutor_detail(document):
    pattern_person = re.compile(u"(原告|原告人|起诉方|公诉机关).*?\。")
    search_result = re.search(pattern_person, document)#research-->find???
    if search_result:
        return search_result.group(),1
    else:
        return "unclear",0

def get_appellee(document):
    pattern_person = re.compile(u"(被告人）|被诉方）|罪犯）|被告人|被诉方|罪犯)(.*?)(，|。)")
    search_result = re.search(pattern_person, document)#research-->find???
    if search_result:
        return search_result.group(2),1
    else:
        return "unclear",0

def get_appellee_detail(document):
    pattern_person = re.compile(u"(被告人|被诉方|罪犯).*?\。")
    search_result = re.search(pattern_person, document)#research-->find???
    if search_result:
        return search_result.group(),1
    else:
        return "unclear",0

def get_reason(document):
    pattern_character = re.compile(u"(危险驾驶|交通肇事|诈骗|非法拘禁|故意杀人)")
    search_result = re.search(pattern_character, document)
    if search_result:
        return search_result.group(),1
    else:
        return "empty",0

def get_type(document):
    pattern_character = re.compile(u"(刑事|民事|刑事附带民事)")
    search_result = re.search(pattern_character, document)
    if search_result:
        return search_result.group(),1
    else:
        return "empty",0
		
def get_character(document):
    pattern_character = re.compile(u"(民事判决书|民事裁定书|民事调解书|民事决定书|民事制裁决定书|刑事判决书|刑事裁定书|刑事附带民事判决书|刑事申诉状|刑事自诉案件反诉状|刑事反诉状|刑事答辩状|刑事自诉状|刑事上诉状)")
    search_result = re.search(pattern_character, document)
    if search_result:
        return search_result.group(),1
    else:
        return "empty",0
	
def get_judge(document):
    pattern_person = re.compile(u"(法官|审判长)(.*?)(代理审判员|助理审判员|审判员)")
    search_result = re.search(pattern_person, document)#research-->find???
    if search_result:
        return search_result.group(2),1
    else:
        return "empty",0

def	get_judex(document):
    pattern_person = re.compile(u"(代理审判员|助理审判员)(.*?)(代理审判员|助理审判员|一九九|二〇一|二〇〇|，|。)")
    search_result = re.search(pattern_person, document)#research-->find???
    if search_result:
        return search_result.group(2),1
    else:
        return "empty",0

def	get_recorder(document):
    pattern_person = re.compile(u"书记员(.*?)($|附相关|附：|。)")
    search_result = re.search(pattern_person, document)#research-->find???
    if search_result:
        return search_result.group(1),1
    else:
        return "empty",0
	
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
        return "",0

def get_confession_of_defense(document):
    pattern_behavior = re.compile(u"(被告人供诉与辩解|被告人供诉|被告人辩解|被告供诉与辩解|被告辩解|被告供诉).*?\。")
    search_result = re.search(pattern_behavior, document) #
    if search_result:
        return search_result.group(),1
    else:
        return "",0	

def get_facts_and_evidence(document):
    pattern_behavior = re.compile(u"(指控事实及证据|指控事实|指控证据).*?\。")
    search_result = re.search(pattern_behavior, document) #
    if search_result:
        return search_result.group(),1
    else:
        return "",0			
		
def get_advocate(document):
    pattern_behavior = re.compile(u"(辩护人意见：|辩护意见：|辩护观点|辩护人观点).*?\。")
    search_result = re.search(pattern_behavior, document) #
    if search_result:
        return search_result.group(),1
    else:
        return "",0		

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
            return "",0

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
        for key,value in line.items():
		    #value.decode('utf8')
		    value=''.join(value)
		    value.decode('utf8')
		    newline[key] = value
		# f.write(decode_line)
        return_document.append((decode_line.decode('utf8'), newline))
        
    return return_document

if __name__ == "__main__":
    file_path = BasePath + "/data/judgment_scam.txt"
    count_total = 0
    document_list = read_document(file_path)
    i = 0

    for (document,dit_line) in document_list:
        if(document):
            save_dict = dict()
            count_total = 0
            save_dict['title'] = dit_line['title'] # varchar(200)
            save_dict['court'] = dit_line['court'] # varchar(200)
            save_dict['case_num'] = dit_line['document_code'] # varchar(200)
            doc, count = get_type(dit_line['title'])
            count_total += count
            save_dict['type'] = "" # varchar(200)
            doc, count = get_reason(dit_line['title'])
            count_total += count
            save_dict['case_reason'] = "" # varchar(200)

            save_dict['date'] = dit_line['date'] # date

            doc, count = get_judge(document)
            count_total += count
            save_dict['judge'] = "" # varchar(200)
            doc, count = get_level(document)
            count_total += count
            save_dict['case_level'] = "" # varchar(200)
            doc, count = get_prosecutor(document)
            count_total += count
            save_dict['prosecutor'] = "" # varchar(200)
            doc, count = get_appellee(document)
            count_total += count
            save_dict['appellee'] = "" # varchar(200)
            doc, count = get_character(document)
            count_total += count
            save_dict['case_type'] = "" # varchar(200)


            save_dict['abstract'] = "" # varchar(2000)

            doc, count = get_prosecutor_detail(document)
            count_total += count
            save_dict['prosecutor_detail'] = "" # varchar(200)
            doc, count = get_appellee_detail(document)
            count_total += count
            save_dict['appellee_detail'] = "" # varchar(200)

            save_dict['url'] = dit_line['url'] # varchar(200)

            doc, count = get_inquisition(document)
            count_total += count
            save_dict['inquisition'] = "" # longtext

            doc, count = get_facts_and_evidence(document)
            count_total += count
            save_dict['facts_and_evidence'] = "" # longtext

            doc, count = get_confession_of_defense(document)
            count_total += count
            save_dict['confession_of_defense'] = "" # longtext

            doc, count = get_advocate(document)
            count_total += count
            save_dict['advocate'] = "" # longtext
            doc, count = get_details(document)
            count_total += count
            save_dict['details'] = "" # longtext
            doc, count = get_behavior(document)
            count_total += count
            save_dict['judge_reason'] = "" # judge_reason

            doc, count = get_result(document)
            count_total += count
            save_dict['judgment_result'] = "" # middletext

            doc, count = get_judex(document)
            count_total += count
            save_dict['judgment_people'] = "" # varchar(200)

            doc, count = get_recorder(document)
            count_total += count
            save_dict['recoder'] = "" # varchar(200)


            save_dict['content'] = document # longtext
            save_dict['criminal'] = "" # varchar(2000)
            save_dict['keywords'] = "" # varchar(10000)

    i += 1



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

