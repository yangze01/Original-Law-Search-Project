#coding=utf8
from __future__ import print_function
from __future__ import division
from correlation import *
from itertools import combinations
from sklearn.manifold import TSNE
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import gc
# 语料向量
x_sample = np.loadtxt(BasePath + "/word2vec_model/corpus_w2v_minmax.txt")
print("load the corpus vector in : {}".format(BasePath + "/word2vec_model/corpus_w2v_minmax.txt"))


tmp = x_sample[0:50]
y = [1]*1890 + [2]*1980 + [3]*1876 + [4]* 2004 + [5]*1927 + [6]*1214 + 260*[7]
# y = np.array(y)
del x_sample
gc.collect()

# iris = load_iris()
# print(iris.target)

# iris = load_iris()
# x = np.array([[1,2,3,4,5,6,7,8,9,0]])
print("del x_sample")
X_tsne = TSNE(learning_rate=100).fit_transform(tmp)
plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
plt.show()
print(X_tsne)

# print("tsne fit")
# X_pca = PCA().fit_transform(tmp)
# print("pca fit")
# plt.figure(figsize=(10, 5))
# plt.subplot(121)
# plt.scatter(X_tsne[:, 0], X_tsne[:, 1],c = y)
# # plt.legend(loc = 'upper right')
#
# plt.subplot(122)
# plt.scatter(X_pca[:, 0], X_pca[:, 1], c = y)
# # plt.legend(loc = 'upper right')
# plt.show()
#

# def tsne_trans(input_vector):
#     X_tsne = TSNE(learning_rate = 100).fit_transform(input_vector)
#     return X_tsne