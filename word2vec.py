# coding=utf-8
import logging
import re
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import json
import gensim
from numpy import *
from data_helper import *
import sys
reload(sys)
BasePath = sys.path[0]
sys.setdefaultencoding('utf8')

def load_model1():
    fv_Word2Vec = BasePath + "/word2vec_model/fv_Word2Vec_test_min_count5"
    model = gensim.models.Word2Vec.load(fv_Word2Vec)
    return model

def load_model2():
    fv_Word2Vec = BasePath + "/word2vec_model/fv_Word2Vec"
    model = gensim.models.Word2Vec.load(fv_Word2Vec)
    return model

# def get_w2v_key(word):
#     word_tuple_list = w2v_model_min_count5.most_similar(word.decode('utf8'), topn=5)
#     ret_dict = {word:[], 'value':[]}

if __name__ == "__main__":
    # filepath_list = [BasePath + "/data/judgmentfull_finance_" + str(i) + "_wordforword2vec" + ".txt" for i in range(0,8)]
    # x_data,y_data = read_seg_document_list(filepath_list)
    # model1 = load_model1()
    # print("model1 reload")
    # model1.train(x_data)
    # add_finance_word2vec = BasePath + "/word2vec_model/fv_Word2Vec_add_finance"
    # model1.save(add_finance_word2vec)


    # model2 = load_model2()
    # print("model2 reload")
    # model2.train(x_data)
    add_finance_word2vec2 = BasePath + "/word2vec_model/fv_Word2Vec_add_finance_min_count_5"
    # model2.save(add_finance_word2vec2)




    # filepath_list = [BasePath + "/data/judgment" + str(i) + "word_from_mysql" + ".txt" for i in range(1,8)]
    ## filepath_list = [BasePath + "/data/judgment" + str(i) + "wordforword2vec" + ".txt" for i in range(1,8)]

    # x_data,y_data = read_seg_document_list(filepath_list)

    # model1 = gensim.models.Word2Vec(x_data, size=100, window=20, min_count=5, workers=20)

    # model2 = gensim.models.Word2Vec(title_sentences, size=300, window=5, min_count=1, workers=20)

    # fv_Word2Vec = BasePath + "/word2vec_model/fv_Word2Vec_test_min_count5"
    # print("complete train")
    # model1.save(fv_Word2Vec)
    #
    # model2 = load_model()

    # print("model reload")
    # model2.train()

    # from optOnMysql.DocumentsOnMysql import *
    # optDocument = DocumentsOnMysql()
    # document = optDocument.getById(5)[5].encode('utf8')
    # from Segment.MySegment import *
    # import jieba.analyse
    # myseg = MySegment()
    # sentence = "张某酒后驾车，撞死行人，之后逃逸，最后被警察逮捕。"
    # word_list = myseg.sen2word(document)
    # key_word = jieba.analyse.textrank(document, topK = 10, withWeight = False)
    # print(' '.join(word_list))
    # print(' '.join(key_word))
    model2 = gensim.models.Word2Vec.load(add_finance_word2vec2)
    word = '逃逸'
    result = model2.most_similar(word.decode('utf8'),topn = 5)
    ret_word = [wordtuple[0] for wordtuple in result]
    print(' '.join(ret_word))
    # ret_key = [wordtuple[1] for wordtuple in result]
    # ret_dict = {word.decode('utf8'):[wordtuple[0] for wordtuple in result],'value':[wordtuple[1] for wordtuple in result]}
    # print(ret_dict)
    # print(ret_dict[word.decode('utf8')])
    # print(result)
    # print(type(result))

    # for i in result:
    #     print(i[0])











