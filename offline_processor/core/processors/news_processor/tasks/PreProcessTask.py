from core.processors.news_processor import newsProcessor
from core.common.tasks.PreProcessTask import BasePreProcessTask


@newsProcessor.add_as_processors(order=0, stage=1, key_column="_id", title_column="TITLE",
                                 content_column="CONTENT", pubtime_column="PUBTIME",
                                 brief_column="BRIEF", bad_column="ISBAD")
class PreProcessTask(BasePreProcessTask):
    pass
    # def __init__(self, key_column, title_column, content_column, pubtime_column, brief_column, bad_column):
    #     self.key_column = key_column
    #     self.title_column = title_column
    #     self.content_column = content_column
    #     self.pubtime_column = pubtime_column
    #     self.bad_column = bad_column
    #     self.brief_column = brief_column
    #
    # def fit(self, data):
    #     logging.info("starting processing data")
    #     # abuse bad data
    #     abuse_ids = Common.compute_abuse_id(data, [self.content_column, self.title_column], self.key_column,
    #                                         min_length_list=[50, 10], detect_messy_list=[False, True])
    #     # data = data[data[self.key_column].apply(lambda x: x not in abuse_ids)]
    #     data[self.bad_column] = data[self.key_column].apply(lambda x: 0 if x not in abuse_ids else 1)
    #
    #     # processed content
    #     content_processed = self.content_column + processed_suffix
    #     content_seg = self.content_column + seg_suffix
    #     data[content_processed], data[content_seg] = Common.process_content(data, self.content_column, content_processed, content_seg)
    #
    #     # process title
    #     title_processed = self.title_column + processed_suffix
    #     data[title_processed] = Common.process_title(data, self.title_column, title_processed)
    #
    #     data[self.pubtime_column] = data[self.pubtime_column].apply(lambda x: self.covert(x))
    #     return data
    #
    # def covert(self, time):
    #     if isinstance(time, datetime.datetime):
    #         return time
    #     elif isinstance(time, str):
    #         if re.match('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$', time):
    #             return datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    #         elif re.match('[0-9]{4}年[0-9]{2}月[0-9]{2}日 [0-9]{2}:[0-9]{2}$', time):
    #             return datetime.datetime.strptime(time, '%Y年%m月%d日 %H:%M')
    #         elif re.match('[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$', time):
    #             return datetime.datetime.strptime(time, '%Y/%m/%d %H:%M:%S')
    #         elif re.match('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}$', time):
    #             return datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    #         elif re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}$', time):
    #             return datetime.datetime.strptime(time, '%Y-%m-%d')
    #         elif re.match('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]$', time):
    #             return datetime.datetime.strptime(time.rsplit('.', 1)[0], '%Y-%m-%d %H:%M:%S')
    #         else:
    #             logging.error("unrecongnized date {0}".format(time))
    #             return ""
    #     elif isinstance(time, datetime.date):
    #         return time
    #     else:
    #         return None

