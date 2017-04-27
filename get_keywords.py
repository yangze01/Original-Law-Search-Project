#coding=utf8
from gensim import corpora, models, similarities
from data_helper import *
import logging
from optOnMysql.DocumentsOnMysql import *
import gensim
import datetime
from optOnMysql.DocumentsOnMysql import *
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import sys
BasePath = sys.path[0]

def make_dictionary(seg_corpus):
    '''
    :param seg_corpus: 分好词的文本数据
    :return: 建立的词典
    '''
    dictionary_file = BasePath + "/data/dict.pickle"
    if os.path.exists(dictionary_file):
        dictionary = corpora.Dictionary.load(dictionary_file)
    else:
        print("do not have a previous dict")
        dictionary = corpora.Dictionary(seg_corpus)
        corpora.Dictionary.save(dictionary, dictionary_file)
    print("make dictionary finished")
    return dictionary

def corpus_tfidf(dictionary, document_list):
    '''
    :param dictionary: 语料词典
    :param document_list: 分好词的语料
    :return: 语料的tfidf值，以语料建立的tfidf模型
    '''
    corpus = [dictionary.doc2bow(text) for text in document_list]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf_value = tfidf[corpus]
    return corpus_tfidf_value,tfidf

if __name__ == "__main__":
    # opt_connect = OptOnMysql()
    # test = opt_connect.exeQuery("select * from document")
    # for i in test:
    #     print(i[1])
    file_path_list = [BasePath + "/data/judgment"+str(i)+".txt" for i in range(1,2)]
    # file_path = BasePath + "/data/judgment.txt"
    document_list = read_more_raw_document_list(file_path_list)
    print(document_list[0])
    # print(1)