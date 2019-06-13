from core.base.BaseTask import BaseTask
from utils.Utils import parse_segged_word
from utils.Constants import REGEX_CN
from services.LinkerService import linkService
import re
from zhon import hanzi
import string


class BaseTermnologyLinkTask(BaseTask):
    """
    recongnize termnology in data
    """

    def __init__(self, link_en_column, seg_column, termnology_tag):

        self.link_en_column = link_en_column
        self.seg_column = seg_column
        self.termnology_tag = termnology_tag
        pass

    def fit(self, data):
        data[self.termnology_tag] = data.apply(lambda x:self.link(x), axis=1)
        return data
        pass

    def link(self, x):
        stop_words = ['', '\uf06c']
        en_data = x[self.link_en_column]
        cn_data = parse_segged_word(x[self.seg_column])
        text_en = en_data.lower()
        text_en = "".join(text_en.split())
        text_en_pure = re.sub(r"[%s]+" % (hanzi.punctuation + re.sub('(\.|#)', '', string.punctuation)), "__", text_en)
        text_en_pure = re.sub(REGEX_CN, '__', text_en_pure)
        en_word_list = text_en_pure.split('__')
        en_word_list = [word for word in en_word_list if word not in stop_words]
        cn_word_list = cn_data
        en_skill_words = linkService.link_terminology(en_word_list, 'en')
        cn_skill_words = linkService.link_terminology(cn_word_list, 'cn')
        return list(set(en_skill_words+cn_skill_words))


