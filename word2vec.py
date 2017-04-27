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

def load_model():
    fv_Word2Vec = BasePath + "/word2vec_model/fv_Word2Vec"
    model = gensim.models.Word2Vec.load(fv_Word2Vec)
    return model



if __name__ == "__main__":

    filepath_list = [BasePath + "/data/judgment" + str(i) + "word_from_mysql" + ".txt" for i in range(1,8)]

    x_data,y_data = read_seg_document_list(filepath_list)

    model1 = gensim.models.Word2Vec(x_data, size=100, window=5, min_count=1, workers=20)
    fv_Word2Vec = BasePath + "/word2vec_model/fv_Word2Vec"
    print("complete train")
    model1.save(fv_Word2Vec)
    print("model reload")











