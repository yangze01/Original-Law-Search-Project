#coding=utf8
import csv
import sys
import random
from random import choice
# reload(sys)
# sys.setdefaultencoding('utf8')
BasePath = sys.path[0]
class Vocab(object):
    def __init__(self, vocab_file, min_frequence = 10000):
        self._word_to_id = {}
        self._id_to_word = {}
        self._count = 0
        with open(vocab_file, 'r') as vocab_f:
            next(vocab_f)
            for line in vocab_f:
                pieces = line.split(',')
                if len(pieces) != 2:
                    print('Warning: incorrectly formatted line in vocabulary file: %s\n'%line)
                    continue
                w = pieces[0]
                count = pieces[1]
                if w in self._word_to_id:
                    raise Exception('Duplicated word in vocabulary file: %s' % w)
                self._word_to_id[w] = int(count)
                self._id_to_word[int(count)] = w
    def word2id(self, word):
        return self._word_to_id[word]

    def id2word(self, word_id):
        if word_id not in self._id_to_word:
            raise ValueError('Id not found in vocab: %d' % word_id)
        else:
            return self._id_to_word[word_id]

def map_word(tuple_file):
    map_dict = dict()
    number_list = list()
    csv_reader = csv.reader(open(tuple_file))
    next(csv_reader)
    for row in csv_reader:
        number = map(int, row[0:3]) + map(float, row[3:])
        number_list.append(number)
    return number_list

def search(id,number_list):
    result_list = list()
    for i in number_list:
        if i[0] == id:
            result_list.append((i[1], i[2], i[3]))
        if i[1] == id:
            result_list.append((i[0], i[2], i[3]))
    # print(result_list)
    sorted_result_list = sorted(result_list, key = lambda key:key[2], reverse=True)
    return sorted_result_list

if __name__ == "__main__":
    dict_filepath = BasePath + "/csv_dict_pos_select.csv"
    tuple_filepath = BasePath + "/csv_tuple_pos_select.csv"
    vocab = Vocab(dict_filepath)
    number_list = map_word(tuple_filepath)
    word_list = vocab._word_to_id.keys()
    slice = random.sample(word_list, 100)
    id = 1
    while True:
        try:
            x = raw_input("请输入检索词: ")
            # for x in slice:
            print("第{0}个检索词：{1}".format(id, x))
            id += 1
            search_key = vocab.word2id(x)
            sorted_result_list = search(search_key, number_list)
            if(len(sorted_result_list) > 5):
                for i in sorted_result_list[0:5]:
                    # print(i)
                    print("word:{0}, count:{1}, relation:{2}".format(vocab.id2word(i[0]), i[1], i[2]))
            else:
                for i in sorted_result_list:
                    # print(i)
                    print("word:{0}, count:{1}, relation:{2}".format(vocab.id2word(i[0]), i[1], i[2]))

        except:
            print("字典中不存在该词！")
            # continue
























