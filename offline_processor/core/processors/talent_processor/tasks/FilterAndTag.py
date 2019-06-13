from core.processors.talent_processor import talentProcessor
from data_access.controller.KBPostController4Mongo import KBPostController4Mongo


@talentProcessor.add_as_processors(order=1, stage=1, name_column="Name", des_column="JobDescription",
                                   is_bad="ISBAD", tag_column="JobTitle")
class FilterAndTag:
    def __init__(self, name_column, des_column, is_bad, tag_column):
        self.name_column = name_column
        self.des_column = des_column
        self.is_bad = is_bad
        self.controller = KBPostController4Mongo()
        # self.names = self.controller.get_postnames()
        self.keyword_dict = self.controller.get_prefix_dict()
        self.tag_column = tag_column
        pass

    def fit(self, data):
        data = data[data[self.is_bad] == 0]
        data[self.tag_column] = data[self.name_column].apply(lambda x: self.tag_data(x))
        data[self.is_bad] = data[self.tag_column].apply(lambda x: 0 if x else 1)
        return data

    def tag_data(self, name):
        result = []
        for k,v in self.keyword_dict.items():
            for keyword in v:
                if keyword in name:
                    result.append(k)
        return result
