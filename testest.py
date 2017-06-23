# #coding=utf8
# from __future__ import print_function
# from __future__ import division
# from correlation import *
# from itertools import combinations
# from sklearn.manifold import TSNE
# from sklearn.datasets import load_iris
# from sklearn.decomposition import PCA
# import matplotlib.pyplot as plt
# import gc
# # 语料向量
# x_sample = np.loadtxt(BasePath + "/word2vec_model/corpus_w2v_minmax.txt")
# print("load the corpus vector in : {}".format(BasePath + "/word2vec_model/corpus_w2v_minmax.txt"))
#
#
# tmp = x_sample[0:50]
# y = [1]*1890 + [2]*1980 + [3]*1876 + [4]* 2004 + [5]*1927 + [6]*1214 + 260*[7]
# # y = np.array(y)
# del x_sample
# gc.collect()
#
# # iris = load_iris()
# # print(iris.target)
#
# # iris = load_iris()
# # x = np.array([[1,2,3,4,5,6,7,8,9,0]])
# print("del x_sample")
# X_tsne = TSNE(learning_rate=100).fit_transform(tmp)
# plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
# plt.show()
# print(X_tsne)

# # print("tsne fit")
# # X_pca = PCA().fit_transform(tmp)
# # print("pca fit")
# # plt.figure(figsize=(10, 5))
# # plt.subplot(121)
# # plt.scatter(X_tsne[:, 0], X_tsne[:, 1],c = y)
# # # plt.legend(loc = 'upper right')
# #
# # plt.subplot(122)
# # plt.scatter(X_pca[:, 0], X_pca[:, 1], c = y)
# # # plt.legend(loc = 'upper right')
# # plt.show()
# #
#
# # def tsne_trans(input_vector):
# #     X_tsne = TSNE(learning_rate = 100).fit_transform(input_vector)
# #     return X_tsne




# #-*- encoding:utf-8 -*-
# from textrank4zh import TextRank4Keyword,TextRank4Sentence
# import codecs
#
# #file = r"/mnt/hgfs/shareUbuntu/zip/THUctc/THUCNews/test/type1/0.txt"
# #text = codecs.open(file,'r','utf-8').read()
#
# word = TextRank4Keyword()
# text = "本院认为，上诉人吴金龙、庄靖凡、刘岩、韩艺芸、黄清峻、周结文、蒙月娇、聂小瑛、龙凤、江俊明、王志勇、段小建、原审被告人林燕梅、王雅明、
# 蔡荣周、林加宝、潘某等人以非法占有为目的，伙同他人通过互联网等电信技术方式发布虚假信息，对不特定多数人实施诈骗活动，其中上诉人吴金龙、庄靖凡、
# 刘岩、韩艺芸、黄清峻、周结文、蒙月娇、龙凤、江俊明、王志勇、原审被告人林燕梅、王雅明参与诈骗数额达人民币10192500元；上诉人聂小瑛、段小建、原审被告人蔡荣周、
# 林加宝参与诈骗数额达10103820元；原审被告人潘某参与诈骗数额达159480元，其行为均已构成诈骗罪，其中上诉人吴金龙、庄靖凡、刘岩、韩艺芸、黄清峻、周结文、蒙月娇、
# 龙凤、江俊明、王志勇、聂小瑛、段小建、原审被告人林燕梅、王雅明、蔡荣周、林加宝犯罪数额特别巨大；原审被告人潘某犯罪数额巨大。在共同犯罪中，上诉人吴金龙、庄靖凡负责召集、
# 管理、培训人员，起主要作用，是主犯；上诉人刘岩、韩艺芸、黄清峻、周结文、蒙月娇、聂小瑛、龙凤、江俊明、王志勇、段小建、原审被告人林燕梅、王雅明、蔡荣周、林加宝、
# 潘某受召集在该团伙中分工配合实施诈骗行为，起次要或辅助作用，是从犯。原审被告人林加宝犯罪后自动投案，并如实供述自己的罪行，是自首。原判认定的事实清楚，证据充分，
# 定罪准确，并充分考虑本案诈骗共同犯罪的特点及各上诉人、原审被告人在共同犯罪中所起作用、认罪态度、悔罪表现等情节减轻、从轻处罚，量刑适当，审判程序合法。上诉人吴金龙、
# 庄靖凡、刘岩、韩艺芸、黄清峻、周结文、蒙月娇、聂小瑛、龙凤、江俊明、王志勇、段小建要求改判较轻刑罚的上诉意见，依法无据，不予采纳。据此，依照《中华人民共和国刑法》第二百
# 六十六条、第二十五条、第二十六条第一款、第二十七条、第六十七条、第六十四条、《中华人民共和国刑事诉讼法》第二百二十五条第一款第（一）项之规定，裁定如下：驳回上诉，维持原判。
# 本裁定为终审裁定。审判长柯志同审判员张黛代理审判员夏简二〇一五年十二月七日书记员蔡凌轩附：本案适用的法律条文《中华人民共和国刑法》第二百六十六条诈骗公私财物，数额较大的，
# 处三年以下有期徒刑、拘役或者管制，并处或者单处罚金；数额巨大或者有其他严重情节的，处三年以上十年以下有期徒刑，并处罚金；数额特别巨大或者有其他特别严重情节的，处十年以上有
# 期徒刑或者无期徒刑，并处罚金或者没收财产。本法另有规定的，依照规定。第二十五条共同犯罪是指二人以上共同故意犯罪。二人以上共同过失犯罪，不以共同犯罪论处；应当负刑事责任的，
# 按照他们所犯的罪分别处罚。第二十六条组织、领导犯罪集团进行犯罪活动的或者在共同犯罪中起主要作用的，是主犯。三人以上为共同实施犯罪而组成的较为固定的犯罪组织，是犯罪集团。
# 对组织、领导犯罪集团的首要分子，按照集团所犯的全部罪行处罚。对于第三款规定以外的主犯，应当按照其所参与的或者组织、指挥的全部犯罪处罚。第二十七条在共同犯罪中起次要或者辅助
# 作用的，是从犯。对于从犯，应当从轻、减轻处罚或者免除处罚。第六十七条犯罪以后自动投案，如实供述自己的罪行的，是自首。对于自首的犯罪分子，可以从轻或者减轻处罚。其中，犯罪较
# 轻的，可以免除处罚。被采取强制措施的犯罪嫌疑人、被告人和正在服刑的罪犯，如实供述司法机关还未掌握的本人其他罪行的，以自首论。犯罪嫌疑人虽不具有前两款规定的自首情节，但是如
# 实供述自己罪行的，可以从轻处罚；因其如实供述自己罪行，避免特别严重后果发生的，可以减轻处罚。第六十四条犯罪分子违法所得的一切财物，应当予以追缴或者责令退赔；对被害人的合法
# 财产，应当及时返还；违禁品和供犯罪所用的本人财物，应当予以没收。没收的财物和罚金，一律上缴国库，不得挪用和自行处理。《中华人民共和国刑事诉讼法》第二百二十五条第二审人民法
# 院对不服第一审判决的上诉、抗诉案件，经过审理后，应当按照下列情形分别处理：（一）原判决认定事实和适用法律正确、量刑适当的，应当裁定驳回上诉或者抗诉，维持原判；（二）原判
# 决认定事实没有错误，但适用法律有错误，或者量刑不当的，应当改判；（三）原判决事实不清楚或者证据不足的，可以在查清事实后改判；也可以裁定撤销原判，发回原审人民法院重新审判。原审人民法院对"

# word.analyze(text,window = 2,lower = True)
# w_list = word.get_keywords(num = 20,word_min_len = 1)
#
# print '关键词:'
# print
# for w in w_list:
#     print w.word,w.weight
# print
# phrase = word.get_keyphrases(keywords_num = 5,min_occur_num=2)
#
# print '关键词组:'
# print
# for p in phrase:
#     print p
# print
# sentence = TextRank4Sentence()
#
# sentence.analyze(text,lower = True)
# s_list = sentence.get_key_sentences(num = 3,sentence_min_len = 5)
#
# print '关键句:'
# print
# for s in s_list:
#     print s.sentence,s.weight
# print

for i in range(1,10):
    print(i)
