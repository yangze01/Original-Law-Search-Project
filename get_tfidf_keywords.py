#coding=utf8
from gensim import corpora, models, similarities
from data_helper import *
from Segment.MyPosTag import *
from get_element import *
import logging
from optOnMysql.DocumentsOnMysql import *
import gensim
import datetime
from optOnMysql.DocumentsOnMysql import *
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import sys
BasePath = sys.path[0]
import jieba.analyse
def make_dictionary(seg_corpus,index):
    '''
    :param seg_corpus: 分好词的文本数据
    :return: 建立的词典
    '''
    dictionary_file = BasePath + "/data/dict_tfidf" + str(index+1) + ".pickle"
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

def save_seg_document(content_list, result_list, i):
    seg_dict = dict()
    filepath = BasePath + "/data/judgment" + str(i) + "wordforword2vec" ".txt"
    seg_dict["content"] = content_list
    seg_dict["result"] = result_list
    encode_json = json.dumps(seg_dict, ensure_ascii = False)
    with open(filepath, "w+") as f:
        f.write(encode_json)
    print("seg document saved as {}".format(filepath))

def save_tfidf_seg_document(document_id_list, seg_document_list, i):
    seg_dict = dict()
    filepath = BasePath + "/data/judgment_tfcorpus" + str(i) + ".txt"
    seg_dict["content"] = seg_document_list
    seg_dict["id_list"] = document_id_list
    encode_json = json.dumps(seg_dict, ensure_ascii = False)

    with open(filepath, "w+") as f:
        f.write(encode_json)
    print("seg document saved as {}".format(filepath))

def read_tfidf_seg_document(i):
    filepath = BasePath + "/data/judgment_tfcorpus" + str(i) + ".txt"
    decode_data = open(filepath)
    decode_json = json.load(decode_data)
    print("the document_len is : {}".format(len(decode_json['content'])))
    return decode_json["id_list"], decode_json['content']

def make_tf_seg_document():
    opt = DocumentsOnMysql()
    criminal_list = [u"交通肇事罪",
                     u"过失致人死亡罪",
                     u"故意杀人罪",
                     u"故意伤害罪",
                     u"抢劫罪",
                     u"电信诈骗罪",
                     u"拐卖妇女儿童罪"]
    myseg = MySegment()
    mypos = MyPostagger()
    index = 0
    document_id_list, document_list = get_criminal_data(opt, criminal_list[index])
    i = 1
    seg_document_list = list()
    for document in document_list:
        print(i)
        i += 1
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        seg_document = myseg.paraph2word(get_details(''.join(document.split('|'))))
        # print(' '.join(seg_document))
        pos_wordlist = mypos.words2pos(seg_document, ['n', 'nl', 'ns', 'v'])
        seg_document_list.append(pos_wordlist)
        # print(' '.join(pos_wordlist))
    mypos.close()
    myseg.close()
    save_tfidf_seg_document(document_id_list, seg_document_list, index + 1)

def save_tfidf_words2mysql():
    print("test optOnMysql")
    opt_connect = OptOnMysql()

    index = 7
    document_id_list, seg_document = read_tfidf_seg_document(index)
    print(document_id_list)
    print("document_id_list len is ： {}".format(len(document_id_list)))
    print("document_id_list len is ： {}".format(len(seg_document)))

    corpus_dictionary = make_dictionary(seg_document, index)
    corpus_token2id = corpus_dictionary.token2id
    corpus_id2token = {value: key for key, value in corpus_token2id.items()}
    print(corpus_token2id)

    corpus_tfidf_value, tf_idf_model = corpus_tfidf(corpus_dictionary, seg_document)

    for i in range(len(document_id_list)):
        document_id = document_id_list[i]

        doc_tfidf = corpus_tfidf_value[i]
        sorted_doc_tfidf = sorted(doc_tfidf, key=lambda t: t[1], reverse=True)

        if(sorted_doc_tfidf == []):
            word_str = ""
        else:
            word_list = list()
            for j in sorted_doc_tfidf[0:10]:
                word_list.append(corpus_id2token[j[0]])
            word_str = "," + ','.join(word_list) + ","
        print(word_str)
        print(document_id)
        opt_connect.exeUpdate("update document set keywords = '{0}' where _id = '{1}'".format(word_str, document_id))

    opt_connect.connClose()

if __name__ == "__main__":
    # make_tf_seg_document()

    # opt_connect = OptOnMysql()
    # test = opt_connect.exeQuery("select * from document")
    # opt_connect.connClose()
    print("test optOnMysql")
    opt_connect = OptOnMysql()
    opt_document = DocumentsOnMysql()
    # index = 7
    # document_id_list, seg_document = read_tfidf_seg_document(index)
    # print(document_id_list)
    # print("document_id_list len is ： {}".format(len(document_id_list)))
    # print("document_id_list len is ： {}".format(len(seg_document)))

    for id in range(1,515):
        print(id)
        it = opt_document.getById(id)
        # print(it[21])
        key_word_tfidf = jieba.analyse.extract_tags(it[21], topK=10, withWeight=False,
                                                    allowPOS=('ns', 'n', 'vn', 'v'))
        key_words = ',' + ','.join(key_word_tfidf) + ','
        # content = ' '.join(it[5].split('|'))
        # abstract = content[content.find('。')+1:content.find('。',content.find('。')+200)+1]
        # print(abstract)
        opt_connect.exeUpdate("update document set keywords = '{0}' where _id = '{1}'".format(key_words, id))
    opt_document.connClose()

    # corpus_dictionary = make_dictionary(seg_document, index)
    # corpus_token2id = corpus_dictionary.token2id
    # corpus_id2token = {value: key for key, value in corpus_token2id.items()}
    # print(corpus_token2id)
    #
    # corpus_tfidf_value, tf_idf_model = corpus_tfidf(corpus_dictionary, seg_document)
    #
    # for i in range(len(document_id_list)):
    #     document_id = document_id_list[i]
    #
    #     doc_tfidf = corpus_tfidf_value[i]
    #     sorted_doc_tfidf = sorted(doc_tfidf, key=lambda t: t[1], reverse=True)
    #
    #     if(sorted_doc_tfidf == []):
    #         word_str = ""
    #     else:
    #         word_list = list()
    #         for j in sorted_doc_tfidf[0:10]:
    #             word_list.append(corpus_id2token[j[0]])
    #         word_str = "," + ','.join(word_list) + ","
    #     print(word_str)
    #     print(document_id)
    #     opt_connect.exeUpdate("update document set keywords = '{0}' where _id = '{1}'".format(word_str, document_id))

    opt_connect.connClose()
