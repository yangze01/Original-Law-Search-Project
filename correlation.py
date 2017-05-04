#coding=utf8
from __future__ import print_function
from __future__ import division

import os
import codecs
import collections
import numpy as np
from get_element import *
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
        return cls(token2index, index2token)


if __name__ == "__main__":
    word_vocab = Vocab()
    word_vocab.feed('|')  # <unk> is at index 0 in word vocab
    myseg = MySegment()
    opt = OptOnMysql()
    opt_on_documents = DocumentsOnMysql()
    for id in range(1,10):
        it = opt_on_documents.getById(id)
        content_id = it[0]
        content = it[5]
        print(content_id)
        senlist = myseg.paraph2sen(content.replace('|',''))
        print("the length of senlist is : {} ".format(len(senlist)))#
        for sentence in senlist:
            word_set = set(myseg.sen2word(sentence.encode('utf8')))
            for word in word_set:
                word_vocab.feed(word)
                opt.exeQuery("insert into ")
            opt.exeQuery("insert into sen_index (word_list, content_id) values('{0}', '{1}')".format(' '.join(word_set), content_id))

            # print(word_set)

    opt.connClose()
    opt_on_documents.connClose()
    myseg.close()
