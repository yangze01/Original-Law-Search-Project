#coding=utf8
import os
import sys
from pylab import *
import matplotlib as mpl
# from matplotlib.font_manager import *
import matplotlib.pyplot as plt
myfont = mpl.font_manager.FontProperties(fname="/usr/share/fonts/truetype/wqy/wqy-microhei.ttc")
mpl.rcParams['axes.unicode_minus'] = False
np.seterr(divide='ignore', invalid='ignore')

import heapq
# from key_get import *
# from data_helper import *
from gensim import corpora, models, similarities
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from optOnMysql.DocumentsOnMysql import *
from sklearn.externals import joblib
import numpy as np
from Segment import MyPosTag
from Segment import MySegment
import gensim
import datetime
from sklearn.manifold import TSNE

from sklearn.metrics import confusion_matrix
reload(sys)
sys.setdefaultencoding('utf8')
from get_element import *
# from word2vec import *
from sklearn.preprocessing import Imputer
from scipy.sparse.csr import csr_matrix
import pickle

# load model and others

fv_Word2Vec = BasePath + "/word2vec_model/fv_Word2Vec"#_test_min_count5"
#
w2v_model = gensim.models.Word2Vec.load(fv_Word2Vec)
#
w2v_model_min_count5 = gensim.models.Word2Vec.load(fv_Word2Vec + "_test_min_count5")
#
# # id索引
document_all_id_list = np.loadtxt(BasePath + "/data/document_full_index.txt")# 8000条数据版本

# document_all_id_list = np.loadtxt(BasePath + "/data/document_index.txt")# 11151条数据版本
# # document_all_id_list = np.loadtxt(BasePath + "/data/document_index_show.txt") #500条数据版本
#
print("load document index finished, the length is : {}".format(len(document_all_id_list)))
# ## 语料向量
x_sample = np.loadtxt(BasePath + "/word2vec_model/corpus_w2v_full_average.txt")
# x_sample = np.loadtxt(BasePath + "/word2vec_model/corpus_w2v_average.txt")
# # x_sample = np.loadtxt(BasePath + "/word2vec_model/corpus_w2v_average_show.txt")
print("load the corpus vector in : {}".format(BasePath + "/word2vec_model/corpus_w2v_average.txt"))

# 随机森林训练
clf_filepath = BasePath + "/data/clf_model_full_average.m"
if os.path.exists(clf_filepath):
    print("the model already exists in :{}".format(clf_filepath))
    clf = joblib.load(clf_filepath)
else:
    print("No model loaded!")
# 分词模块
myseg = MySegment()
opt_Document = DocumentsOnMysql()


def dev_sample(x_sample, y_sample, dev_sample_percentage):
    np.random.seed(10)
    print(len(y_sample))
    shuffle_indices = np.random.permutation(np.arange(len(y_sample)))
    print(shuffle_indices)
    x_shuffled = x_sample[shuffle_indices]
    y_shuffled = y_sample[shuffle_indices]

    dev_sample_index = -1 * int(dev_sample_percentage * float(len(x_sample)))

    x_train, x_test = x_shuffled[:dev_sample_index], x_shuffled[dev_sample_index:]
    y_train, y_test = y_shuffled[:dev_sample_index], y_shuffled[dev_sample_index:]
    return x_train, x_test, y_train, y_test

def plot_confusion_matrix(cm, title = "Confusion matrix", cmap = plt.cm.Blues):
    # classes = [u'交通肇事罪',
    #             u'过失致人死亡罪',
    #             u'故意杀人罪',
    #             u'故意伤害罪',
    #             u'抢劫罪',
    #             u'电信诈骗罪',
    #             u'拐卖妇女儿童罪']
    classes = [       u'交通肇事罪',  # 危险驾驶罪（危险 驾驶罪）
                      u'过失致人死亡罪', # 故意杀人罪（故意 杀人 杀人罪） 故意伤害罪（故意 伤害 伤害罪）
                      u'故意杀人罪',
                      u'故意伤害罪',
                      u'过失致人重伤罪',
                      u'抢劫罪',
                      u'诈骗罪', #（诈骗 诈骗罪 诈骗案）
                      u'拐卖妇女儿童罪'
                      ]
    # classes = ["crime of causing traffic casualties",
    #            "death by misadventure",
    #            "offence of intentional killing",
    #            "crime of inflicting serious bodily injury",
    #            "inflicting serious injury by misadventure",
    #            "crime of pillage",
    #            "financial fraud",
    #            "Crime of abducting and trafficking in women and children"]

    plt.imshow(cm, interpolation = "nearest", cmap = cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation = 45, fontproperties=myfont)
    plt.yticks(tick_marks, classes,fontproperties=myfont)
    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel("Predicted label")


def rf_similarity(path_vec):
    fea_size = len(path_vec)
    sim_vec = np.zeros([fea_size, fea_size])
    k = 0
    for i in range(0, fea_size):
        for j in range(i, fea_size):
            print(k)
            k = k+1
            num_path = np.sum(path_vec[i] & path_vec[j])
            sim_vec[i][j] = num_path
            sim_vec[j][i] = num_path
    return sim_vec/sim_vec.diagonal().T


def make_word2id(corpus):
    # corpus_file = BasePath + "/../jsonfile/courpus.json"
    # corpus = get_json_data(corpus_file)
    f_word_id = open(BasePath + "/../data/word_id.txt",'w+')
    word_set = set()
    for sentence in corpus[1:2200]:
        for word in sentence:
            word_set.add(word)
    print(len(word_set))
    i = 0
    for word in list(word_set):
        print(word)
        strstr = word.decode('utf8') + " " + str(i) + '\n'
        f_word_id.write(strstr)
        i += 1
    f_word_id.close()


def sentence2vec(model, sentence, randomvec = None, vec_type = "average"):
    # print(vec_type)
    if randomvec == None:
        randomvec = np.random.normal(size = 100)
    len_word = len(set(sentence))
    tmp_num = np.zeros(100)
    if vec_type == "average":
        if (len_word == 0):
            return np.zeros(100)
        for word in set(sentence):
            try:
                tmp_num += model[word.decode('utf8')]
            except:
                tmp_num += randomvec
        tmp_num = tmp_num / len_word
        # print(tmp_num.shape)


    elif vec_type == "minmax":
        # print("in minmax")
        if (len_word == 0):
            return np.zeros(200)
        for word in set(sentence):
            try:
                tmp_num = np.vstack((tmp_num, model[word.decode('utf8')]))
            except:
                tmp_num = np.vstack((tmp_num, randomvec))
        tmp_num = np.hstack((np.min(tmp_num, axis = 0), np.max(tmp_num, axis = 0)))

    return tmp_num


def sentences2docvec(model, sentences, vec_type = "average"):
    i = 0
    random_vector = np.random.normal(size = 100)
    corpus_vec = list()
    for sentence in sentences:
        # if (i == 2658):
        #     print(1)
        tmp_num = sentence2vec(model, sentence, randomvec = random_vector, vec_type = vec_type)
        # len_word = len(set(sentence))
        print(i)

        # tmp_num = np.zeros(300)
        # for word in set(sentence):
        #     try:
        #         tmp_num += model[word.decode('utf8')]
        #     except:
        #         tmp_num += random_vector
        # tmp_num = tmp_num/len_word
        corpus_vec.append(tmp_num)
        i = i + 1
    np.savetxt(BasePath + "/word2vec_model/corpus_w2v_full_" + vec_type + ".txt", np.array(corpus_vec))


def load_model():
    fv_Word2Vec = BasePath + "/word2vec_model/fv_Word2Vec"
    model = gensim.models.Word2Vec.load(fv_Word2Vec)
    return model

def corpus2word2vec(x_data):
    # w2v_model = load_model()
    sentences2docvec(w2v_model, x_data)


def get_candidate(topn, query_vec, corpus_vec):
    vec_sim = np.dot(query_vec, corpus_vec.T)  / (np.linalg.norm(corpus_vec, axis = 1) * np.linalg.norm(query_vec))
    topn_candidate = heapq.nlargest(topn, range(len(vec_sim)), vec_sim.take)
    return topn_candidate, vec_sim[topn_candidate]


def get_clf_sim(clf_model, seg_sentence_vec, candidate_vec, topn_candidate_index):
    path_of_sample, _ = clf.decision_path(candidate_vec[topn_candidate_index])
    path_of_seg_sentence, _ = clf.decision_path(seg_sentence_vec)
    seg_sentence_array = path_of_seg_sentence.toarray()
    sample_array = path_of_sample.toarray()
    clf_sim = np.sum(seg_sentence_array & sample_array, axis=1) / float(np.sum(seg_sentence_array & seg_sentence_array))

    top_clf_index = heapq.nlargest(50, range(len(clf_sim)), clf_sim.take)
    # return np.array(topn_candidate_index)[top_clf_index]
    return top_clf_index, clf_sim


def tsne_trans(input_vector):
    X_tsne = TSNE(learning_rate = 100).fit_transform(input_vector)
    return X_tsne


def get_sim_sentence(clf_model, seg_sentence, x_sample):
    # w2v_model = load_model()
    seg_sentence_vec = sentence2vec(w2v_model, seg_sentence, vec_type = "average")
    # vec_sim = np.dot(seg_sentence_vec, x_sample.T) / (np.linalg.norm(x_sample, axis=1) * np.linalg.norm(seg_sentence_vec))
    topn_candidate_index, candidate_vec_sim = get_candidate(300, seg_sentence_vec, x_sample)
    # print(topn_candidate_index)
    top_clf_index, clf_sim = get_clf_sim(clf_model, seg_sentence_vec, x_sample, topn_candidate_index)
    # document_ret_dict = dict()
    # document_ret_tuple = [(document_all_id_list[topn_candidate_index[i]], clf_sim[i], candidate_vec_sim[i]) for i in top_clf_index]

    # document_ret_dict = [(document_all_id_list[topn_candidate_index[i]], clf_sim[i]) for i in top_clf_index]

    # document_ret_dict = [{document_all_id_list[topn_candidate_index[i]]:clf_sim[i]} for i in top_clf_index]

    # print(top_clf_index)
    result_vec = x_sample[np.array(topn_candidate_index)[top_clf_index]]
    tsne_vec = tsne_trans(result_vec)
    # X_tsne = TSNE(learning_rate=100).fit_transform(tmp)
    # plt.scatter(tsne_vec[:, 0], tsne_vec[:, 1])
    # plt.show()
    # print(tsne_vec)
    tsne_vec_dict = {top_clf_index[i]:tsne_vec[i] for i in range(0, len(top_clf_index))}

    # result_vec = x_sample(list(np.array(topn_candidate_index)[top_clf_index]))
    # print(result_vec)


    document_ret_dict = [{'id' : document_all_id_list[topn_candidate_index[i]],
                          'final_sim' : clf_sim[i],
                          'vec_sim' : candidate_vec_sim[i],
                          'position' : {
                              'x' : tsne_vec_dict[i][0],
                              'y' : tsne_vec_dict[i][1]}

                         } for i in top_clf_index]

    document_ret_dict.sort(key=lambda x: x["final_sim"],reverse = True)

    # dict = sorted(document_ret_dict.items(), key = lambda d:d[1], reverse = True)
    # for i in top_clf_index:
    #     document_ret_dict[document_all_id_list[topn_candidate_index[i]]] = clf_sim[i]

    # for i in document_ret_tuple:
    #     print(i)

    # for json_ob in document_ret_dict:
    #     for key,value in json_ob.items():
    #         print(key,value)

    # return document_ret_tuple

    print(document_ret_dict)
    return document_ret_dict

def get_w2v_key(word):
    # print(word)
    word_tuple_list = w2v_model_min_count5.most_similar(word.decode('utf8'), topn=5)
    ret_dict = {'key': [wordtuple[0] for wordtuple in word_tuple_list],
                'value': [wordtuple[1] for wordtuple in word_tuple_list]}
    # print(ret_dict)
    return ret_dict

def get_keywords(seg_sentence):
    print(1)
    return_word_list = list()
    return_relation_list = dict()
    for word in set(seg_sentence):
        try:
            # word_tuple_list = w2v_model_min_count5.most_similar(word.decode('utf8'), topn=5)
            relation_dict = get_w2v_key(word)
            word_dict_list = [{'word' : key,
                               'cluster' : word.encode('utf8')} for key in relation_dict['key']]

            return_word_list += word_dict_list
            tmp_list = list()
            relation_word_dict = dict(zip(relation_dict['key'], relation_dict['value']))
            for key,value in relation_word_dict.items():
                print(key)
                print(value)

            for tuple in zip(relation_dict['key'], relation_dict['value']):
                tmp_list.append({'key':tuple[0], 'value':tuple[1]})
            return_relation_list[word] = tmp_list
            # return_relation_list.append({word:relation_dict})
            # return_relation_list.append({relation_dict})

        except:
            continue

    return return_word_list, return_relation_list

def impl_sim(search_type, sentence):

    seg_sentence = myseg.sen2word(sentence.encode('utf8'))

    # for word in set(seg_sentence):
    # for word in set(sentence):

    return_word_list, return_relation_list = get_keywords(seg_sentence)
    document_ret_dict = get_sim_sentence(clf, seg_sentence, x_sample)
    return_json_list = {'keywords':return_word_list,
                        'result':document_ret_dict,
                        'relation':return_relation_list}
    # print(return_json_list)
    return return_json_list

if __name__ == "__main__":
    # a = 1
    # while(True):
    #     print("请输入一句话或空格间隔的关键词，回车结束： ")
    #     sentence = raw_input()
    #     document_ret_dict = impl_sim(2, sentence)
    #     j = 1
    #     for json_obj in document_ret_dict['result'][0:5]:
    #         # print(json_obj['id'])
    #         # print(json_obj)
    #         print("----------------------- 第" + str(j) + "名匹配文档： -----------------------")
    #         print("----------------------- 第" + str(j) + "名匹配文档的clf相似度: {}------------------------------------".format(json_obj['final_sim']))
    #         print("----------------------- 第" + str(j) + "名匹配文档的vec相似度: {}------------------------------------".format(json_obj['vec_sim']))
    #
    #         print("document id {}".format(json_obj['id']))
    #         # print('\n'.join(document_list[document_tuple[0]].split('|')))
    #         # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #         print('\n'.join(opt_Document.getById(json_obj['id'])[25].split('|')))
    #         j += 1
    #
    #




    # print("----------------------- 加载数据中，请等待..... -----------------------")
    # [1]*1890 + [2]*1980 + [3]*1876 + [4]* 2004 + [5]*1927 + [6]*1214 + 260*[7]

    # opt_Document = DocumentsOnMysql()
    # document_all_id_list, document_list = get_criminal_list_data(opt_Document, criminal_list)
    # np.savetxt(BasePath + "/data/document_index.txt", np.array(document_all_id_list))
    #
    # # document_all_id_list = [int(i) for i in np.loadtxt(BasePath + "/data/document_index.txt")]
    # document_all_id_list = np.loadtxt(BasePath + "/data/document_index.txt")
    # print("load document index finished, the length is : {}".format(len(document_all_id_list)))
    #
    # # print(document_all_id_list)
    # # print(len(document_all_id_list))
    # # content_all_list, result_all_list = fetch_all_content_result(document_list)
    # # test_content = content_all_list[-1]
    # # use_content = content_all_list # [:-1]
    # # print(1)

    # x_sample = np.loadtxt(BasePath + "/word2vec_model/corpus_w2v_average.txt")
    # print("load the corpus vector in : {}".format(BasePath + "/word2vec_model/corpus_w2v_average.txt"))

    # # 随机森林训练
    # clf_filepath = BasePath + "/data/clf_model_average.m"
    # if os.path.exists(clf_filepath):
    #     print("the model already exists in :{}".format(clf_filepath))
    #     clf = joblib.load(clf_filepath)
    # else:
    #     print("No model loaded!")

    # myseg = MySegment()
    # # w2v_model = load_model()
    #
    # # opt_sql = DocumentsOnMysql()
    # print("请输入查询方式，整句查询请按1，关键词查询请按2： ")
    # i = input()
    # while True:
    #     if(i == 1):
    #         print("请输入一句话，回车结束： ")
    #         sentence = raw_input()
    #         seg_sentence = myseg.sen2word(sentence)
    #         document_ret_tuple = get_sim_sentence(clf, seg_sentence, x_sample)
    #     else:
    #         print("请输入关键词，以空格隔开，回车结束")
    #         seg_sentence = raw_input()
    #         seg_sentence = seg_sentence.encode('utf8').split(' ')
    #         document_ret_tuple = get_sim_sentence(clf, seg_sentence, x_sample)
    #     j = 1


    #     for key in document_ret_tuple.keys():
    #         print("----------------------- 第" + str(j) + "名匹配文档： -----------------------")
    #         print("----------------------- 第" + str(j) + "名匹配文档的clf相似度: {}------------------------------------".format(document_ret_tuple[key]['clf_sim']))
    #         print("----------------------- 第" + str(j) + "名匹配文档的vec相似度: {}------------------------------------".format(document_ret_tuple[key]['vec_sim']))
    #
    #         print(key)
    #         # print('\n'.join(document_list[document_tuple[0]].split('|')))
    #         # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #         print('\n'.join(opt_Document.getById(key)[5].split('|')))
    #         j += 1
    # myseg.close()
    #




























    # criminal_list = ['交通肇事罪',  # 危险驾驶罪（危险 驾驶罪）
    #                  '过失致人死亡罪',  # 故意杀人罪（故意 杀人 杀人罪） 故意伤害罪（故意 伤害 伤害罪）
    #                  '故意杀人罪',
    #                  '故意伤害罪',
    #                  '过失致人重伤罪',
    #                  '抢劫罪',
    #                  '诈骗罪',  # （诈骗 诈骗罪 诈骗案）
    #                  '拐卖妇女儿童罪'
    #                  ]
    #
    # opt_Document = DocumentsOnMysql()
    # document_all_id_list, document_list = get_criminal_list_data(opt_Document, criminal_list)
    # np.savetxt(BasePath + "/data/document_full_finance_index.txt", np.array(document_all_id_list))
    #

    num_topics = 100
    dev_sample_percentage = .3
    filepath_list = [BasePath + "/data/judgment" +"full_finance_" +str(i)+ "_" + "wordforword2vec" + ".txt" for i in range(0,8)]
    x_data, y_data = read_seg_document_list(filepath_list)
    corpus2word2vec(x_data)


    # x_sample = np.loadtxt(BasePath + "/word2vec_model/corpus_w2v_full_average.txt")
    # # x_sample = np.load(BasePath + "/word2vec_model/corpus_w2v_minmax.npy")
    # # print(x_sample[-1].shape)
    # x_sample = Imputer().fit_transform(x_sample)
    # # for i in x_sample:
    # #     print(i)
    # y_sample = np.array(y_data)
    # x_train, x_test, y_train, y_test = dev_sample(x_sample, y_sample, dev_sample_percentage)
    # print("data loaded finished.")
    #
    #
    # # 随机森林训练
    # clf_filepath = BasePath + "/data/clf_model_full_average.m"
    # if os.path.exists(clf_filepath):
    #     print("the model already exists.")
    #     clf = joblib.load(clf_filepath)
    # else:
    #     print("the model doesn't exists.")
    #     clf = RandomForestClassifier(n_estimators=100, bootstrap = True, oob_score = False , n_jobs = 16)
    #     clf_model = clf.fit(x_train, y_train)
    #     joblib.dump(clf, clf_filepath)
    #
    # # 评估模型准确率
    # clf_pre = clf.predict(x_test)
    # print(clf_pre)
    # print(y_test)
    #
    # # 评估模型准确率
    # acc = (clf_pre == y_test).mean()
    # print("精度为：")
    # print(acc)
    #
    # # # 输出决策树路径
    # # path_of_randomforest, _ = clf.decision_path(x_test)
    # # print(_)
    # # # print("path of randomforest")
    # # # print(path_of_randomforest.toarray())
    # # print("sim matrix")
    # # print(path_of_randomforest)
    # # print(path_of_randomforest.toarray())
    # # sim_matrix = rf_similarity(path_of_randomforest.toarray())
    # # print("end sim matrix")
    # # print(sim_matrix)
    #
    # #输出混淆矩阵
    # cm = confusion_matrix(y_test, clf_pre)
    # print("Confusion matrix, without normalization")
    # print(cm)
    #
    # # 正则化混淆矩阵
    # cm_normalized = cm.astype('float') / cm.sum(axis = 1)[:, np.newaxis]
    # print("Normalized confusion matrix")
    # print(cm_normalized)
    # plt.figure()
    # plot_confusion_matrix(cm_normalized, title = 'Normalized confusion matrix')
    # plt.show()
