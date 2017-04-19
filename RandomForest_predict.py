#coding=utf8
import sys
from pylab import *
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
from data_helper import *
from gensim import corpora, models, similarities
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import numpy as np
import gensim
import datetime
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
reload(sys)
sys.setdefaultencoding('utf8')
BasePath = sys.path[0]

def make_dictionary(seg_corpus):
    dictionary_file = BasePath + "/data/dict.pickle"

    if os.path.exists(dictionary_file):
        dictionary = corpora.Dictionary.load(dictionary_file)
    else:
        print("do not have a previous dict")
        dictionary = corpora.Dictionary(seg_corpus)
        corpora.Dictionary.save(dictionary, dictionary_file)
    print("make dictionary finished")
    return dictionary

def doc2bag_corpus(dictionary, seg_corpus):

    bag_of_words_corpus = [dictionary.doc2bow(pdoc) for pdoc in seg_corpus]
    print("bag_of words finished finished")
    return bag_of_words_corpus

def make_lda(bag_of_words_corpus, _dictionary, _nums_topic = 100):
    lda_filepath = BasePath + '/data/lda.pkl'
    starttime = datetime.datetime.now()
    if os.path.exists(lda_filepath):
        lda_model = models.LdaModel.load(lda_filepath)
    else:
        # lda_model = models.LdaModel(bag_of_words_corpus, id2word=_dictionary, num_topics=_nums_topic)
        lda_model = gensim.models.ldamulticore.LdaMulticore(corpus=bag_of_words_corpus, num_topics=_nums_topic, id2word=_dictionary, workers=32, chunksize=2000,
                                                passes=1, batch=False, alpha='symmetric', eta=None, decay=0.5,
                                                offset=1.0, eval_every=10, iterations=50, gamma_threshold=0.001,
                                                random_state=None)
        lda_model.save(fname = lda_filepath)
    endtime = datetime.datetime.now()
    print("lda using time")
    print((endtime - starttime).seconds)
    return lda_model

def tup2vec(_dictionary, lda_model, bag_of_words_corpus, _nums_topic = 100):
    lda_vec = list()
    lda_corpus = lda_model[bag_of_words_corpus]
    # print(type(lda_corpus))
    for lda_tuple_list in lda_corpus:
        tmp_vector = [0.] * _nums_topic
        for lda_tuple in lda_tuple_list:
            tmp_vector[lda_tuple[0]] = lda_tuple[1]
        lda_vec.append(tmp_vector)
    return np.array(lda_vec)

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
    #classes = [u'交通肇事罪',
    #           u'过失致人死亡罪',
    #           u'故意杀人罪',
    #           u'故意伤害罪',
    #           u'抢劫罪',
    #           u'电信诈骗罪',
    #           u'拐卖妇女儿童罪']
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
    for i in range(0,fea_size):
        for j in range(i, fea_size):
            num_path = np.sum(path_vec[i] & path_vec[j])
            sim_vec[i][j] = num_path
            sim_vec[j][i] = num_path
    return sim_vec/sim_vec.diagonal().T

def get_criminal_data(opt_Documents, crim):

    '''
    :param crim: 罪名
    :return: document_id_list, document_list
    '''

    document_id_list = list()
    document_list = list()

    print("in get_criminal")
    iter = opt_Documents.findbycriminal(crim)
    print("in segment")
    for it in iter:
        document_id_list.append(it[0])
        document_list.append(it[5])
    return document_id_list, document_list




if __name__ == "__main__":
    # print(1)
    # num_topics = 100
    # dev_sample_percentage = .2
    # 数据获取及划分
    clf_filepath = BasePath + "/data/clf_lda_model.m"
    if os.path.exists(clf_filepath):
        print("the model alread exitst %s"%(clf_filepath))
        clf = joblib.load(clf_filepath)

    # 输出决策树路径
    path_of_randomforest, _ = clf.decision_path(x_test)
    print(_)
    # print("path of randomforest")
    # print(path_of_randomforest.toarray())
    print("sim matrix")
    print(rf_similarity(path_of_randomforest.toarray()))












