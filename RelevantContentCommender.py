from DBManager import DBManager
import random

sentence_list = DBManager.select_all_titles()
random_sentence = random.choice(sentence_list)
print("> ", random_sentence)
# random_datum = DBManager.selectDatumBy(random_sentence)

n_number = 2
data_list = []


class RecommendDatum():
    def __init__(cls, sentence, similarity):
        cls.subject_line = sentence
        cls.similarity = similarity


object_sentence = None


def compare_with(sentence):
    object_sentence = sentence
    object_split_list = get_spilt_list_of(object_sentence)
    for subject_index, subject_sentence in enumerate(sentence_list):
        if subject_sentence != object_sentence :
            subject_split_list = get_spilt_list_of(subject_sentence)
            count = 0
            for i in object_split_list:
                for j in subject_split_list:
                    if i == j:
                        count += 1
            datum = RecommendDatum(subject_sentence, count / len(object_split_list))
            data_list.append(datum)


def get_spilt_list_of(sentence):
    split_list = []
    sentence_length = len(sentence) - n_number + 1
    for i in range(sentence_length):
        split_part = sentence[i:i + n_number]
        split_list.append(split_part)
    return split_list


def print_all_subject_data():
    for record in data_list:
        if record.similarity >= 0.5:
            print("comparing title list: ", record.subject_line,
                  "\nsimilarity: ", record.similarity)


def get_max():
    sorted_list = sorted(data_list, key=lambda item: item.similarity, reverse=True)
    response = filter(sorted_list)
    for record in response:
        print("comparing title list: ", record.subject_line, "\nsimilarity: ", record.similarity)


def filter(sorted_list):
    max_data =[]
    for datum in sorted_list:
        for operand in max_data:
            if operand.subject_line == datum.subject_line:
                break
        if max_data.__len__() < n_number:
            max_data.append(datum)
        else:
            break
    return max_data


compare_with(random_sentence)
print("Max> ")
get_max()
