#coding=utf8
# import numpy as np
# import heapq
#
#
# import tensorflow as tf
#
#
#
#
#
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
#
# for i in range(0,1000):
#     tmp_num = np.vstack((tmp_num,b))
#     print(tmp_num.shape)
#
# tmp_num = np.hstack((np.min(tmp_num, axis=0), np.max(tmp_num, axis=0)))
# print(tmp_num.reshape(1,-1))
#
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
# print(a[:3*4])


# import requests
# import json
# sentence = "张某 酒后 驾车 ， 撞死 行人，之后 驾车 逃逸"
# # sentence = None
# a = requests.post("http://0.0.0.0:5000/api_sim",data={'search_type':1,'sentence':sentence})
# # b = requests.get("http://0.0.0.0:5000/api_sim",data={'search_type':1,'sentence':sentence})
# # url = "http://0.0.0.0:5000/api_sim?search_type=" + str(1) + "&" + "sentence='%s'"%sentence
# # print(url)
# # b = requests.get(url)
# # print(b)
# a_decode = json.loads(a.content)
# # b_decode = json.loads(b.content)
# print(a)
# # print(b)
# print(a_decode)
# # print(b_decode)
# # print(a_decode['out'])
import json
from collections import OrderedDict
d = {str(i):i for i in range(10)}
print(d)
json_d = json.dumps(d,sort_values= True)
print(json_d)
# d = OrderedDict(sorted(d.items(),key = lambda t:t[0]))
# e = {key:value for key,value in d.items()}
# print(d)