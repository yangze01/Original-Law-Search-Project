
#coding=utf8
from gensim import corpora, models, similarities
from data_helper import *
import logging
import gensim
import datetime
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import sys
BasePath = sys.path[0]

def make_dictionary(seg_corpus):
    '''
    :param seg_corpus: 分好词的文本数据
    :return:
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
    print("lda using time: %d seconds" % (endtime - starttime).seconds)
    # print((endtime - starttime).seconds)
    return lda_model

def corpus_tfidf(dictionary, document_list):
    corpus = [dictionary.doc2bow(text) for text in document_list]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf_value = tfidf[corpus]
    return corpus_tfidf_value,tfidf

def sim_D2N(lda_model, dictionary, test_content, tfidf_model, corpus_tfidf_value):

    # lda_model = models.LdaModel(corpus_tfidf_value, id2word=dictionary, num_topics=100)
    # lda.print_topics(2)
    test_content_vec = dictionary.doc2bow(test_content)
    test_content_tfidf_vec = tfidf_model[test_content_vec]
    index = similarities.MatrixSimilarity(lda_model[corpus_tfidf_value])
    sims = index[lda_model[test_content_tfidf_vec]]
    sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return sort_sims




if __name__ == "__main__":
    print(1)