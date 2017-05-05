#coding=utf8
from __future__ import print_function
from __future__ import division
from correlation import *
from itertools import combinations

# # 统计候选词对
# count_word_in_sen_dict = dict()
# bag_sen_dict = load_bag_corpus()  # 从0开始
# print(len(bag_sen_dict))
#
# candidate_dict = dict()
# for i in range(1, len(bag_sen_dict) + 1):
#     print(i)
#     comb = list(combinations(bag_sen_dict[str(i)],2))
#     # print(comb)
#     for com_tuple in comb:
#         if com_tuple not in candidate_dict:
#             candidate_dict[str(com_tuple)] = 1
#         else:
#             candidate_dict[str(com_tuple)] += 1
# print("the len of candidate is : {}".format(len(candidate_dict)))
#
# # 保存候选词对
# candidate_file_path = BasePath + "/data/candidate_word_pair.txt"
# encode_json = json.dumps(candidate_dict, ensure_ascii=False)
# with open(candidate_file_path, "w+") as f:
#     f.write(encode_json)
# print("seg countnum_word_in_sen_filepath saved as {}".format(candidate_file_path))


# 挑选高频词对，小于2的抛弃
candidate_file_path = BasePath + "/data/candidate_word_pair.txt"
with open(candidate_file_path, "r+") as f:
    jsondata = f.read()
    candidate_high_frequence_dict = json.loads(jsondata)
print("the len of worddict is: {}".format(len(candidate_high_frequence_dict)))
i = 1
for key,value in candidate_high_frequence_dict.items():
    print(i)
    i = i + 1
    if value < 2:
        del candidate_high_frequence_dict[key]

# 保存高频词对
candidate_high_freqence_file_path = BasePath + "/data/high_frequence_word_pair.txt"
encode_json = json.dumps(candidate_high_frequence_dict, ensure_ascii=False)
with open(candidate_high_freqence_file_path, "w+") as f:
    f.write(encode_json)
print("high_frequence_word_pair saved as {}".format(candidate_high_freqence_file_path))



# 对高频词对统计11 10 01
# 加载高频词对 (id1, id2) = count(11)
candidate_high_freqence_file_path = BasePath + "/data/high_frequence_word_pair.txt"
with open(candidate_file_path, "r+") as f:
    jsondata = f.read()
    candidate_high_frequence_dict = json.loads(jsondata)
print("the len of candidate_high_frequence_dict is: {}".format(len(candidate_high_frequence_dict)))
# 加载词---句子集合 w_id = [s1, s2, s3, s4 ...]
count_word_senlist_filepath = BasePath + "/data/count_word_in_sen_list.txt"
with open(count_word_sen_filepath, "r+") as f:
    jsondata = f.read()
    word_in_sen_dict = json.loads(jsondata)
print("the len of word_in_sen_dict is: {}".format(len(word_in_sen_dict)))
# 统计高频词的相关统计量，并转换为 (w1, w2) = [count(11), count(10), count(01)]
sen_size = 247744
for key,value in candidate_high_frequence_dict:
    id_list = key[1:-1].split(', ')
    l2 = set(word_in_sen_dict[str(id_list[0])]) - set(word_in_sen_dict[str(id_list[1])])
    l3 = set(word_in_sen_dict[str(id_list[1])]) - set(word_in_sen_dict[str(id_list[0])])
    candidate_high_frequence_dict[key] = [value, len(l2), len(l3)]
# 保存高频词统计量
candidate_high_freqence_count_file_path = BasePath + "/data/high_frequence_word_count_pair.txt"
encode_json = json.dumps(candidate_high_frequence_dict, ensure_ascii=False)
with open(candidate_high_freqence_count_file_path, "w+") as f:
    f.write(encode_json)
print("high_frequence_word_pair saved as {}".format(candidate_high_freqence_count_file_path))





















