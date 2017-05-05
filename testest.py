#coding=utf8
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


# 挑选高频词对，小于1的抛弃
candidate_file_path = BasePath + "/data/candidate_word_pair.txt"
with open(candidate_file_path, "r+") as f:
    jsondata = f.read()
    candidate_dict = json.loads(jsondata)
print("the len of worddict is: {}".format(len(candidate_dict)))
i = 1
for key,value in candidate_dict.items():
    print(i)
    i = i + 1
    if value < 2:
        del candidate_dict[key]

# 保存高频词对
candidate_file_path = BasePath + "/data/high_frequence_word_pair.txt"
encode_json = json.dumps(candidate_dict, ensure_ascii=False)
with open(candidate_file_path, "w+") as f:
    f.write(encode_json)
print("high_frequence_word_pair saved as {}".format(candidate_file_path))


#
