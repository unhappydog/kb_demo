from core.processors.news_processor import newsProcessor
from core.common.tasks.DistinctTask import BaseDistinctTask


@newsProcessor.add_as_processors(order=1, stage=1,
                                 content_column="CONTENT", pubtime_column="PUBTIME",
                                 replicate_column="ISREPLICATE",
                                 min_score=0.7, max_length=1000)
class DistinctTask(BaseDistinctTask):
    # def fit(self, data):
    #     data = super().fit(data)
    #     # data[self.replicate_column] = data.apply(lambda x:self.dt_if_replicate(x), axis=1)
    #
    # def dt_if_replicate(self, x):
    #     if x[self.replicate_column] == 1:
    #         return 1
    pass
    # def __init__(self, content_column, pubtime_column,
    #              replicate_column, min_score, max_length):
    #     self.content_column = content_column
    #     self.pubtime_column = pubtime_column
    #     self.replicate_column = replicate_column
    #     self.min_score = min_score
    #     self.max_length = max_length
    #     self.history = FixSizeDataFrame(None, max_length=self.max_length, sort_by=self.pubtime_column)

    # def fit(self, data):
    #     data[self.replicate_column] = data.apply(lambda x: self.if_replicate(x), axis=1)
    #     return data
    #
    # def if_replicate(self, x):
    #     if x is None:
    #         return 1
    #
    #     if x[self.content_column] is None:
    #         return 1
    #
    #     m = Utils.compute_min_hash(Utils.parse_segged_word(x[self.content_column + seg_suffix]))
    #     x['min_hash'] = m
    #     time_1 = time.time()
    #
    #     min_hash_scores = self.history.value.apply(lambda x: m.jaccard(x['min_hash']), axis=1)
    #     time_2 = time.time()
    #     # min_hash_scores.apply()
    #     m_score = min_hash_scores.max()
    #
    #     # logging.info("compute minhash cost {0}s".format(time_2 - time_1))
    #     self.history.push_data(x)
    #     # print(len(self.history.value))
    #     time_3 = time.time()
    #     # logging.info("pushing data cost{0}s".format(time_3 - time_2))
    #     if m_score > self.min_score:
    #         return 1
    #
    #     # time_1 = time.time()
    #     # for index, item in self.history.value.iterrows():
    #     #     m_score = m.jaccard(item['min_hash'])
    #     #     if m_score > self.min_score:
    #     #         # time_1 =time.time()
    #     #         self.history.push_data(x)
    #     #         time_2 = time.time()
    #     #         print(time_2 - time_1)
    #     #         return 1
    #
    #
    #     return 0
