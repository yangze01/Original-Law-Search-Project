#coding=utf8
# from key_get import *
import os
import sys
from pylab import *
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
from data_helper import *
from gensim import corpora, models, similarities
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import numpy as np
from Segment import MyPosTag
from Segment import MySegment
import gensim
import datetime
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
reload(sys)
sys.setdefaultencoding('utf8')
from get_element import *
# from word2vec import *
# def read_seg_document():
from sklearn.preprocessing import Imputer


from scipy.sparse.csr import csr_matrix


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
    #classes = [u"交通肇事罪", u"意外致死罪", u"故意杀人罪", u"致人重伤罪", u"抢劫罪", u"电信诈骗罪", u"拐卖妇女儿童罪"]
    classes = ["crime of causing traffic casualties", "death by misadventure", "offence of intentional killing", "crime of inflicting serious bodily injury", "crime of pillage", "financial fraud", "Crime of abducting and trafficking in women and children"]
    plt.imshow(cm, interpolation = "nearest", cmap = cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation = 45)
    plt.yticks(tick_marks, classes)
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
#
def sentence2vec(model, sentence, randomvec):
    len_word = len(set(sentence))
    tmp_num = np.zeros(300)
    for word in set(sentence):
        try:
            tmp_num += model[word.decode('utf8')]
        except:
            tmp_num += randomvec
    tmp_num = tmp_num/len_word
    return tmp_num

def sentences2docvec(model, sentences):
    # f = open(BasePath + "/word2vec_model/corpus_w2v.txt", "w")
    i = 0
    random_vector = np.random.normal(size = 300)
    corpus_vec = list()
    for sentence in sentences:
        tmp_num = sentence2vec(model, sentence, random_vector)
        # len_word = len(set(sentence))
        # print(i)
        # tmp_num = np.zeros(300)
        # for word in set(sentence):
        #     try:
        #         tmp_num += model[word.decode('utf8')]
        #     except:
        #         tmp_num += random_vector
        # tmp_num = tmp_num/len_word
        corpus_vec.append(tmp_num)
        i = i + 1
    np.savetxt(BasePath + "/word2vec_model/corpus_w2v.txt", np.array(corpus_vec))
    # f.close()

def load_model():
    fv_Word2Vec = BasePath + "/word2vec_model/fv_Word2Vec"
    model = gensim.models.Word2Vec.load(fv_Word2Vec)
    return model

def corpus2word2vec(x_data):
    w2v_model = load_model()
    sentences2docvec(w2v_model, x_data)



if __name__ == "__main__":

    # file_path = BasePath + "/data/judgment_kill.txt"
    print("----------------------- 加载数据中，请等待..... -----------------------")
    # opt_Document = DocumentsOnMysql()
    # document_all_id_list, document_list = get_criminal_data(opt_Document, u'故意杀人罪')

    # content_all_list, result_all_list = fetch_all_content_result(document_list)
    # test_content = content_all_list[-1]
    # use_content = content_all_list # [:-1]
    # print(1)
    x_sample = np.loadtxt(BasePath + "/word2vec_model/corpus_w2v.txt")
    # 随机森林训练
    clf_filepath = BasePath + "/data/clf_model.m"
    if os.path.exists(clf_filepath):
        print("the model already exists.")
        clf = joblib.load(clf_filepath)
    else:
        print("No model loaded!")

    print("请输入查询方式，整句查询请按1，关键词查询请按2： ")
    i = input()
    while True:
        if(i == 1):
            print("请输入一句话，回车结束： ")
            sentence = raw_input()
            document_index_list = get_sim_sentence(sentence, use_content)
        else:
            print("请输入关键词，以空格隔开，回车结束")
            seg_sentence = raw_input()
            document_index_list = get_sim_sentence(seg_sentence, use_content)
        document_id_list = [document_all_id_list[document_index] for document_index in document_index_list]
        print("document index list is : ", document_index_list)
        print("document id list is : ", document_id_list)
        j = 1
        for document_index in document_index_list:
            print("----------------------- 第"+ str(j) + "名匹配文档： -----------------------")
            print(document_list[document_index])
            j += 1


































    # num_topics = 100
    dev_sample_percentage = .2
    filepath_list = [BasePath + "/data/judgment" + str(i) + "wordforword2vec" + ".txt" for i in range(1,8)]
    x_data,y_data = read_seg_document_list(filepath_list)

    # corpus2word2vec(x_data)
    x_sample = np.loadtxt(BasePath + "/word2vec_model/corpus_w2v.txt")
    x_sample = Imputer().fit_transform(x_sample)
    y_sample = np.array(y_data)
    x_train, x_test, y_train, y_test = dev_sample(x_sample, y_sample, dev_sample_percentage)
    print("data loaded finished.")

    # 随机森林训练
    clf_filepath = BasePath + "/data/clf_model.m"
    if os.path.exists(clf_filepath):
        print("the model already exists.")
        clf = joblib.load(clf_filepath)
    else:
        print("the model doesn't exists.")
        clf = RandomForestClassifier(n_estimators=100, bootstrap = True, oob_score = False , n_jobs = 16)
        clf_model = clf.fit(x_train, y_train)
        joblib.dump(clf, clf_filepath)

    # 评估模型准确率
    clf_pre = clf.predict(x_test)
    print(clf_pre)
    print(y_test)

    # 评估模型准确率
    acc = (clf_pre == y_test).mean()
    print("精度为：")
    print(acc)

    # # 输出决策树路径
    # path_of_randomforest, _ = clf.decision_path(x_test)
    # print(_)
    # # print("path of randomforest")
    # # print(path_of_randomforest.toarray())
    # print("sim matrix")
    # print(path_of_randomforest)
    # print(path_of_randomforest.toarray())
    # sim_matrix = rf_similarity(path_of_randomforest.toarray())
    # print("end sim matrix")
    # print(sim_matrix)

    # 输出混淆矩阵
    cm = confusion_matrix(y_test, clf_pre)
    print("Confusion matrix, without normalization")
    print(cm)

    # 正则化混淆矩阵
    cm_normalized = cm.astype('float') / cm.sum(axis = 1)[:, np.newaxis]
    print("Normalized confusion matrix")
    print(cm_normalized)
    plt.figure()
    plot_confusion_matrix(cm_normalized, title = 'Normalized confusion matrix')
    plt.show()



