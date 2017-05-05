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
# from __future__ import division

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

def load_seg_document(file_path):
    with open(file_path,"r+") as f:
        jsondata = f.read()
        jsondict = json.loads(jsondata)
    content_list = jsondict['content']
    return content_list

def save_bag_corpus(bag_corpus_dict):
    # seg_dict = dict()
    filepath = BasePath + "/data/sen_bag_word_corpus" + ".txt"
    # seg_dict["content"] = corpus_list
    encode_json = json.dumps(bag_corpus_dict, ensure_ascii = False)
    with open(filepath, "w+") as f:
        f.write(encode_json)
    print("bag_corpus_dict saved as {}".format(filepath))

def load_bag_corpus():
    '''
        将词袋表示的句子重新加载
    :return:
    '''
    file_path = BasePath + "/data/sen_bag_word_corpus" + ".txt"
    with open(file_path,"r+") as f:
        jsondata = f.read()
        jsondict = json.loads(jsondata)
    # content_list = jsondict['content']
    return jsondict




def save_corpus():
    '''
        将语料分割为以句子为单位的行
    :return: 将数据保存为sen_word_corpus
    '''
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
    # save_corpus()

    # 将数据保存为词袋模型
    # sen_word_corpus = load_seg_document(BasePath + "/data/sen_word_corpus" + ".txt")
    # dictionary = make_dictionary(sen_word_corpus)
    # print("the dictionary len is : {}".format(len(dictionary)))
    # print(dictionary.id2token)
    # id2token = {value: key for key, value in dictionary.token2id.items()}

    # print("the len of dictionary: {}".format(len(dictionary.token2id)))
    # bag_corpus = doc2bag_corpus(dictionary, sen_word_corpus)
    # print("the len of bag_corpus is : {}".format(len(bag_corpus)))
    # bag_sen_dict = dict()
    # for i in range(0, len(bag_corpus)):
    #     print(i)
    #     tmp_sen = bag_corpus[i]
    #     bag_sen = [word_tuple[0] for word_tuple in tmp_sen]
    #     # print(tmp_sen)
    #     # print(bag_sen)
    #     bag_sen_dict[i+1] = bag_sen
    # print("the len of bag_sen_dict is : {}".format(len(bag_sen_dict)))
    # save_bag_corpus(bag_sen_dict)



   # # 统计每个单词出现的句子
   #  count_word_in_sen_dict = dict()
   #  bag_sen_dict = load_bag_corpus() #从0开始
   #  print(len(bag_sen_dict))
   #
   #  for i in range(1, len(bag_sen_dict)+1):
   #      # print("+++++++++++++++++++++++++++")
   #      # print(i)
   #      # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
   #      tmp_word_id_list = bag_sen_dict[str(i)]
   #      for word_id in tmp_word_id_list:
   #          # print(word_id)
   #          if(word_id == 0):
   #              print(tmp_word_id_list)
   #          if word_id not in count_word_in_sen_dict:
   #              count_word_in_sen_dict[word_id] = [i]
   #          else:
   #              count_word_in_sen_dict[word_id].append(i)
   #
    # count_word_sen_filepath = BasePath + "/data/count_word_in_sen_list.txt"
   #  encode_json = json.dumps(count_word_in_sen_dict, ensure_ascii=False)
   #  with open(count_word_sen_filepath, "w+") as f:
   #      f.write(encode_json)
   #  print("seg count_word_sen_filepath saved as {}".format(count_word_sen_filepath))


    # 统计词对出现的次数
    count_word_sen_filepath = BasePath + "/data/count_word_in_sen_list.txt"
    with open(count_word_sen_filepath,"r+") as f:
        jsondata = f.read()
        word_in_sen_dict = json.loads(jsondata)
    print("the len of worddict is: {}".format(len(word_in_sen_dict)))

    word_pair = dict()

    for id1 in range(0, len(word_in_sen_dict)):
        for id2 in range(id1+1, len(word_in_sen_dict)):
            print(id1, id2)
            l1 = set(word_in_sen_dict[str(id1)]) & set(word_in_sen_dict[str(id2)])
            # print(len(l1))
            if(len(l1) < 1):
                continue
            l2 = set(word_in_sen_dict[str(id1)]) - set(word_in_sen_dict[str(id2)])
            l3 = set(word_in_sen_dict[str(id2)]) - set(word_in_sen_dict[str(id1)])
            word_pair[(id1, id2)] = [len(l1), len(l2), len(l3)]

    # 保存词对统计
    countnum_word_in_sen_filepath = BasePath + "/data/countnum_word_in_sen.txt"
    # count_word_sen_filepath = BasePath + "/data/count_word_in_sen_list.txt"
    encode_json = json.dumps(word_pair, ensure_ascii=False)
    with open(countnum_word_in_sen_filepath, "w+") as f:
     f.write(encode_json)
    print("seg countnum_word_in_sen_filepath saved as {}".format(count_word_sen_filepath))




