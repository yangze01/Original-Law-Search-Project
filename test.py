import numpy as np
import heapq




a = np.array([1, 6, 3, 4, 5])

# print(heapq.nlargest(3, range(len(a)), a.take))






#
b = np.array([[1,6,3,4,5],
              [2,3,4,5,6],
              [2,1,2,3,1],
              [3,1,2,5,6]]*10000)

#
# print(np.dot(a, b.T)/ (np.linalg.norm(b,axis = 1)*np.linalg.norm(a)))

c = np.array([1, 0, 1, 0, 1])

# index = [0,2]

d = np.array([[1, 0, 1, 0, 1],
              [0, 1, 1, 0, 1],
              [0, 1, 1, 0, 1]])

# print(d[index])

print(np.sum(c & d, axis=1))
num_path = np.sum(c & d, axis=1) / float(np.sum(c & c))
# # print()
print(num_path)

a = np.array([1, 2, 3, 4, 5])
# a = [1, 2, 3, 4, 5]
b = [1,2,3]
print(a[b])




#
#
#
#
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
