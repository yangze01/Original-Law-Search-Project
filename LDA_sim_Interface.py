
#coding=utf8
from gensim import corpora, models, similarities
from data_helper import *
import logging
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
    '''
    :param dictionary: 语料词典
    :param document_list: 分好词的语料
    :return: 语料的tfidf值，以语料建立的tfidf模型
    '''
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

def get_top10_sim_intersection(content_sims, result_sims):
    final_top10_sim = list()
    for tuple1 in content_sims:
        for tuple2 in result_sims:

            if(tuple1[0] == tuple2[0]):
                sum = 0.4 * tuple1[1] + 0.6 * tuple2[1]
                final_top10_sim.append((tuple1[0],sum))

    if(final_top10_sim == []):
        print("no intersection")
        return content_sims
    else:
        return sorted(final_top10_sim, key=lambda t: t[1], reverse=True)

def get_sim_seg_sentence(seg_sentence, use_content): #
    content_dictionary = make_dictionary(use_content)
    content_corpus_tfidf, tfidf_content = corpus_tfidf(content_dictionary, use_content)
    content_lda_model = make_lda(content_corpus_tfidf, content_dictionary, _nums_topic = 100)
    print("----------------------- 数据加载完毕 -----------------------")
    test_content = seg_sentence.decode('utf8').split()
    content_sims = sim_D2N(content_lda_model, content_dictionary, test_content, tfidf_content, content_corpus_tfidf)
    top10_sort_sim_content = content_sims[0:10]

    j = 1
    document_index_list = [result_tuple[0] for result_tuple in top10_sort_sim_content]
    # for result_tuple in top10_sort_sim_content:
        # print("----------------------- 第" + str(j) + "名匹配文档： -----------------------")
        # print(document_list[result_tuple[0]])
    return document_index_list

def get_sim_sentence(sentence, use_content):
    '''
    :param sentence:#df_model, corpus_tfidf_value):
    :param use_content:
    :return:
    '''
    myseg = MySegment()
    content_dictionary = make_dictionary(use_content)
    content_corpus_tfidf, tfidf_content = corpus_tfidf(content_dictionary, use_content)
    content_lda_model = make_lda(content_corpus_tfidf, content_dictionary, _nums_topic = 100)
    print("----------------------- 数据加载完毕 -----------------------")
    test_content = ' '.join(myseg.sen2word(sentence)).decode('utf8').split()
    myseg.close()
    content_sims = sim_D2N(content_lda_model, content_dictionary, test_content, tfidf_content, content_corpus_tfidf)
    top10_sort_sim_content = content_sims[0:10]
    document_index_list = [result_tuple[0] for result_tuple in top10_sort_sim_content]
    return document_index_list




if __name__ == "__main__":
    file_path = BasePath + "/data/judgment.txt"
    print("----------------------- 加载数据中，请等待..... -----------------------")
    opt_Document = DocumentsOnMysql()
    document_all_id_list, document_list = get_criminal_data(opt_Document, u'交通肇事罪')

    content_all_list, result_all_list = fetch_all_content_result(document_list)
    # test_content = content_all_list[-1]
    use_content = content_all_list # [:-1]
    print(1)
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





































