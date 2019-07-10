from core.processors.talent_processor import talentProcessor
from core.common.tasks.PreProcessTask import BasePreProcessTask
import re


@talentProcessor.add_as_processors(order=0, stage=1, key_column="_id", title_column="Name",
                                 content_column="JobDescription", pubtime_column="Startdate",
                                 brief_column="BRIEF", bad_column="ISBAD", endtime_column="Enddate",
                                   min_length=[50, 4])
class PreProcessor(BasePreProcessTask):
    def __init__(self, key_column, title_column, content_column, pubtime_column, brief_column, bad_column,
                 endtime_column, min_length):
        self.key_column = key_column
        self.title_column = title_column
        self.content_column = content_column
        self.pubtime_column = pubtime_column
        self.bad_column = bad_column
        self.brief_column = brief_column
        self.endtime_column = endtime_column
        self.min_length = min_length

    def special_process(self, data):
        data[self.endtime_column] = data[self.endtime_column].apply(lambda x: self.covert(x))
        data[self.title_column] = data[self.title_column].apply(lambda x: self.extract_name(x))
        return data

    def extract_name(self, name):
        # tricated_name = re.sub("(\(|（).+(\)|）)$", "", name)
        tricated_name = re.sub("(\(.+?\)|（.+?）)", "", name)
        if tricated_name:
            return tricated_name
        else:
            print(name)
            return name
