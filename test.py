#coding=utf8
import numpy as np
import heapq

a = np.array([[1,1,3,4],
              [2,3,4,5],
              [3,2,4,5],
              [4,2,3,6]])
print(a[1:])
a_min = np.min(a, axis=0)
a_max = np.max(a, axis=0)
print(np.min(a, axis=0))
print(np.max(a, axis=0))
# print(a_min+a_max)
# print(np.concatenate((a_min, a_max)))
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(np.hstack((a_min,a_max)))
print("++++++++++++++++++++++++++++++++++++++++++++")
print(np.vstack((a_min,a_max)))
b = a[1]
# tmp_num = np.zeros(4)
#
# for i in range(0,1000):
#     tmp_num = np.vstack((tmp_num,b))
#     print(tmp_num.shape)
# tmp_num = np.hstack((np.min(tmp_num, axis=0), np.max(tmp_num, axis=0)))
# print(tmp_num.reshape(1,-1))

a = {str(i):i for i in range(10)}
print(a)
for key,value in a.items():
    print(key, value)

# print np.extend()
# np.extend(a_min, a_max)
#
#
# def rf_similarity(path_vec):
#     fea_size = len(path_vec)
#     sim_vec = np.zeros([fea_size, fea_size])
#     k = 0
#     for i in range(0, fea_size):
#         for j in range(i, fea_size):
#             print(k)
#             k = k+1
#             num_path = np.sum(path_vec[i] & path_vec[j])
#             sim_vec[i][j] = num_path
#             sim_vec[j][i] = num_path
#     return sim_vec/sim_vec.diagonal().T
import tensorflow as tf
a = tf.constant(1)
b = tf.constant(2)
sess = tf.Session()
print(sess.run(a+b))
# print(2123)

