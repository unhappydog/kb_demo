import string
import re
from zhon import hanzi
from utils.Logger import logging
from services.NLPService import nlpService


def compute_abuse_id(data, column_list, id_column, min_length_list, detect_messy_list):
    abuse_datas = []
    abuse_df = []
    columns_lengths_ifmessys = zip(column_list, min_length_list, detect_messy_list)
    for column, min_length, detect_messy in columns_lengths_ifmessys:
        if detect_messy:
            abuse_df.append(data[data[column].apply(
                lambda x: x is None or type(x) != str or len(x) <= min_length or x == "" or detect_messy_cod(x) < 2)])
        else:
            abuse_df.append(data[data[column].apply(
                lambda x: x is None or type(x) != str or len(x) <= min_length or x == "")])
        try:
            for df in abuse_df:
                abuse_datas.extend(df[id_column].tolist())
        except KeyError as e:
            # Logger.error("data is empty", e)
            # logging.error("data is empty")
            logging.exception("data is empty")
    return list(set(abuse_datas))


def process_content(data, content_column, processed_column, seg_column):
    def process(doc):
        words = nlpService.seg_words(doc)
        tags = nlpService.tag_words(words)
        word_tags = zip(words, tags)
        return ["{0}:{1}".format(word, tag) for word, tag in word_tags if word not in nlpService.stop_words['cn']]
    data[processed_column] = data[content_column].apply(
        lambda x: ";".join(nlpService.sentencesize(x))
    )
    data[seg_column] = data[content_column].apply(
        lambda x: ";".join([",".join(process(doc)) for doc in nlpService.sentencesize(x)])
    )

    return data[processed_column], data[seg_column]


def process_title(data, content_column, processed_column):
    data[processed_column] = data[content_column].apply(
        lambda x: re.sub(r"[%s]+" % (hanzi.punctuation + string.punctuation), "", x))
    return data[processed_column]


# 检测乱码， 小于1.2认为是乱码
def detect_messy_cod(doc):
    def new_len(iterable):
        try:
            return iterable.__len__()
        except AttributeError:
            return sum(1 for _ in iterable)

    # seg_list = jieba.cut(doc)
    # seg_list = ltpService.segment(doc)
    seg_list = nlpService.seg_words(doc)
    return len(doc) / new_len(seg_list)

def detect_messy_cod_v2(doc, min_code=20):
    messy_code = b"\xef\xbf\xbd"
    doc_str = doc
    count = doc_str.count(messy_code.decode(), 0, len(doc_str))
    if count >= min_code:
        return True
    else:
        return False
