#coding=utf8
from __future__ import division
# import numpy as np
# import heapq
# import tensorflow as tf





# a = np.array([[1,1,3,4],
#               [2,3,4,5],
#               [3,2,4,5],
#               [4,2,3,6]])
# print(a[1:])
# a_min = np.min(a, axis=0)
# a_max = np.max(a, axis=0)
# print(np.min(a, axis=0))
# print(np.max(a, axis=0))
# # print(a_min+a_max)
# # print(np.concatenate((a_min, a_max)))
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# print(np.hstack((a_min,a_max)))
# print("++++++++++++++++++++++++++++++++++++++++++++")
# print(np.vstack((a_min,a_max)))
# b = a[1]
# tmp_num = np.zeros(4)

# for i in range(0,1000):
#     tmp_num = np.vstack((tmp_num,b))
#     print(tmp_num.shape)

# tmp_num = np.hstack((np.min(tmp_num, axis=0), np.max(tmp_num, axis=0)))
# print(tmp_num.reshape(1,-1))

# # print np.extend()
# # np.extend(a_min, a_max)
# #
# #
# # def rf_similarity(path_vec):
# #     fea_size = len(path_vec)
# #     sim_vec = np.zeros([fea_size, fea_size])
# #     k = 0
# #     for i in range(0, fea_size):
# #         for j in range(i, fea_size):
# #             print(k)
# #             k = k+1
# #             num_path = np.sum(path_vec[i] & path_vec[j])
# #             sim_vec[i][j] = num_path
# #             sim_vec[j][i] = num_path
# #     return sim_vec/sim_vec.diagonal().T
# a = {str(i):i for i in range(1,15)}
# print(a)
# a = tf.constant(1)
# b = tf.constant(2)
# sess = tf.Session()
# print(sess.run(a+b))
#
#
# a = "张某驾车逃逸，被警察逮捕。"
#
# print(a[:3*4])#
from Segment import MySegment
from optOnMysql import optOnMysql
from optOnMysql.DocumentsOnMysql import *
import requests
import json
# sentence = u"张某 酒后 驾车 ， 撞死 行人，之后 驾车 逃逸"
# sentence1 = u"解决"
sentence2 = u"李某  拐卖妇女儿童 残疾  自首"
# # sentence = None
# # a = requests.post("http://0.0.0.0:5000/api_sim",data={'search_type':1,'sentence':sentence1})
# b = requests.post("http://0.0.0.0:5000/api_sim",data={'search_type':1,'sentence':sentence2})
b = requests.post("http://0.0.0.0:5000/api_relation",data={'word':"交通"})
# b = requests.post("http://10.168.103.10:5000/test",data={'roomid':1653327,'flag':1})
# # # b = requests.get("http://0.0.0.0:5000/api_sim",data={'search_type':1,'sentence':sentence})
# # # url = "http://0.0.0.0:5000/api_sim?search_type=" + str(1) + "&" + "sentence='%s'"%sentence
# # # print(url)
#
# b = requests.get(url)
# print(b)
# # print(a)
# a_decode = json.loads(a.content)
b_decode = json.loads(b.content)
# # print(a_decode)
# print(b_decode)
# # print(a)
print(' '.join(b_decode['交通'.decode('utf8')]))
# print(b_decode['relation'])
# # print(a_decode)
opt_Document = DocumentsOnMysql()
# while (True):
#     print("请输入一句话或空格间隔的关键词，回车结束： ")
#     print(sentence2)
#     # sentence = raw_input()
#     document_ret_dict = b_decode
#     print(document_ret_dict['result'])
#     j = 1
#     for json_obj in document_ret_dict['result'][0:5]:
#         # print(json_obj['id'])
#         # print(json_obj)
#         print("----------------------- 第" + str(j) + "名匹配文档： -----------------------")
#         print("----------------------- 第" + str(j) + "名匹配文档的clf相似度: {}------------------------------------".format(
#             json_obj['final_sim']))
#         print("----------------------- 第" + str(j) + "名匹配文档的vec相似度: {}------------------------------------".format(
#             json_obj['vec_sim']))
#
#         print("document id {}".format(json_obj['id']))
#         # print('\n'.join(document_list[document_tuple[0]].split('|')))
#         # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         print('\n'.join(opt_Document.getById(json_obj['id'])[5].split('|')))
#         j += 1
#     break

# # for i in a_decode:
# #     print(i)
# # print(type(a_decode))
# # # print(b_decode)
# # # print(a_decode['out'])
# import json
# from collections import OrderedDict
# # d = {str(i):i for i in range(10)}
# # print(d)
# # json_d = json.dumps(d,sort_values= True)
# # print(json_d)
# # d = OrderedDict(sorted(d.items(),key = lambda t:t[0]))
# # e = {key:value for key,value in d.items()}
# # print(d)

# a = set()
# a.add(1)
# a.add(2)
# a.add(3)
# # if 1 in a:
# #     print(True)
# # print(a)
num_dict = dict()
num_dict[1] = 'a'
num_dict[2] = 'b'
num_dict[3] = 'c'
#
# print(num_dict)
#
# if 4 in num_dict:
#     print(True)
# else:
#     print(False)
# print([1,2,3] + [4, 5, 6])
# print(a)

# del num_dict[1]
# print(num_dict)

# for key,value in num_dict.items():
#     if(value == 'c'):
#         del num_dict[key]

# print(num_dict)
from itertools import combinations,product
import numpy as np
a = [1,2,3]
b = np.array(a)/3
print(b)
