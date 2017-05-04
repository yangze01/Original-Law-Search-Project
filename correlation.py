#coding=utf8
from __future__ import print_function
from __future__ import division
from gensim import corpora, models, similarities
import os
import codecs
import collections
import numpy as np
from get_element import *
import pickle
from data_helper import *
from Segment.MySegment import *
from Segment.MyPosTag import *

class Vocab:

    def __init__(self, token2index=None, index2token=None):
        self._token2index = token2index or {}
        self._index2token = index2token or []

    def feed(self, token):
        if token not in self._token2index:
            # allocate new index for this token
            index = len(self._token2index)
            self._token2index[token] = index
            self._index2token.append(token)

        return self._token2index[token]

    @property
    def size(self):
        return len(self._token2index)

    def token(self, index):
        return self._index2token[index]

    def __getitem__(self, token):
        index = self.get(token)
        if index is None:
            raise KeyError(token)
        return index

    def get(self, token, default=None):
        return self._token2index.get(token, default)

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self._token2index, self._index2token), f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as f:
            token2index, index2token = pickle.load(f)
        # print(token2index)
        return cls(token2index, index2token)

def make_dictionary(seg_corpus):
    '''
    :param seg_corpus: 分好词的文本数据
    :return: 建立的词典
    '''
    dictionary_file = BasePath + "/data/sen_word_dict.pickle"
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

def save_seg_document(corpus_list):
    seg_dict = dict()
    filepath = BasePath + "/data/sen_word_corpus" + ".txt"
    seg_dict["content"] = corpus_list
    encode_json = json.dumps(seg_dict, ensure_ascii = False)
    with open(filepath, "w+") as f:
        f.write(encode_json)
    print("seg document saved as {}".format(filepath))

def save_bag_corpus(corpus_list):
    seg_dict = dict()
    filepath = BasePath + "/data/sen_word_corpus" + ".txt"
    seg_dict["content"] = corpus_list
    encode_json = json.dumps(seg_dict, ensure_ascii = False)
    with open(filepath, "w+") as f:
        f.write(encode_json)
    print("seg document saved as {}".format(filepath))

def load_bag_corpus():
    file_path = BasePath + "/data/sen_word_corpus" + ".txt"
    with open(file_path,"r+") as f:
        jsondata = f.read()
        jsondict = json.loads(jsondata)
    content_list = jsondict['content']
    return content_list


def load_seg_document(file_path):
    with open(file_path,"r+") as f:
        jsondata = f.read()
        jsondict = json.loads(jsondata)
    content_list = jsondict['content']
    return content_list


def save_corpus():
    # word_vocab = Vocab()
    # word_vocab.feed('|')  # <unk> is at index 0 in word vocab
    myseg = MySegment()
    opt = OptOnMysql()
    opt_on_documents = DocumentsOnMysql()
    seg_corpus = list()
    for id in range(1, 11152):
        it = opt_on_documents.getById(id)
        content_id = it[0]
        content = it[5]
        print(content_id)
        senlist = myseg.paraph2sen(content.replace('|', ''))
        # print("the length of senlist is : {} ".format(len(senlist)))#
        for sentence in senlist:
            word_set = set(myseg.sen2word(sentence.encode('utf8')))
            word_list = list(word_set)
            seg_corpus.append(word_list)
    save_seg_document(seg_corpus)

    opt.connClose()
    opt_on_documents.connClose()
    myseg.close()


if __name__ == "__main__":
    # sen_word_corpus = load_seg_document(BasePath + "/data/sen_word_corpus" + ".txt")
    # dictionary = make_dictionary(sen_word_corpus)
    # print("the len of dictionary: {}".format(len(dictionary.token2id)))
    # bag_corpus = doc2bag_corpus(dictionary, sen_word_corpus)
    # bag_corpus_re = [[word_tuple[0] for word_tuple in sen_word_list] for sen_word_list in bag_corpus]
    # len_corpus = len(bag_corpus)
    # save_bag_corpus(bag_corpus_re)
    # print(len_corpus)



    # count_word_in_sen_dict = dict()
    # bag2_corpus_re = load_bag_corpus()
    # print(len(bag2_corpus_re))
    # for i in range(0, len(bag2_corpus_re)):
    #     # print("+++++++++++++++++++++++++++")
    #     print(i)
    #     # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #     tmp_word_id_list = bag2_corpus_re[i]
    #     for word_id in tmp_word_id_list:
    #         # print(word_id)
    #         if word_id not in count_word_in_sen_dict:
    #             count_word_in_sen_dict[word_id] = [i+1]
    #         else:
    #             count_word_in_sen_dict[word_id].append(i+1)


    count_word_sen_filepath = BasePath + "/data/count_dict.txt"
    # encode_json = json.dumps(count_word_in_sen_dict, ensure_ascii=False)
    # with open(count_word_sen_filepath, "w+") as f:
    #     f.write(encode_json)
    # print("seg count_word_sen_filepath saved as {}".format(count_word_sen_filepath))

    # file_path = BasePath + "/data/sen_word_corpus" + ".txt"
    with open(count_word_sen_filepath,"r+") as f:
        jsondata = f.read()
        jsondict = json.loads(jsondata)
    print("the len of jsondict is: {}".format(len(jsondict)))
    print(jsondict['1'])
        # print(count_word_in_sen_dict)
    # encode_json = json.dumps(seg_dict, ensure_ascii=False)
    # with open(filepath, "w+") as f:
    #     f.write(encode_json)
    # print("seg document saved as {}".format(filepath))



