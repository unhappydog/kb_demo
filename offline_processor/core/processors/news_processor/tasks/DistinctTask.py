from core.processors.BaseTask import BaseTask
from core.processors.news_processor import newsProcessor
from core.base.data.FixSizeDataFrame import FixSizeDataFrame
from utils.Logger import logging
from core.common import Common
from utils.Constants import processed_suffix, seg_suffix
from datasketch import MinHash
from utils import Utils


@newsProcessor.add_as_processors(order=1, stage=1,
                                 content_column="CONTENT", pubtime_column="PUBTIME",
                                 replicate_column="ISREPLICATE",
                                 min_score=0.7, max_length=1000)
class DistinctTask(BaseTask):
    def __init__(self, content_column, pubtime_column,
                 replicate_column, min_score, max_length):
        self.content_column = content_column
        self.pubtime_column = pubtime_column
        self.replicate_column = replicate_column
        self.min_score = min_score
        self.max_length = max_length
        self.history = FixSizeDataFrame(None, max_length=self.max_length, sort_by=self.pubtime_column)

    def fit(self, data):
        data[self.replicate_column] = data.apply(lambda x: self.if_replicate(x), axis=1)
        return data

    def if_replicate(self, x):
        if x is None:
            return 1

        if x[self.content_column] is None:
            return 1

        m = Utils.compute_min_hash(Utils.parse_segged_word(x[self.content_column + seg_suffix]))
        x['min_hash'] = m

        for index, item in self.history.value.iterrows():
            m_score = m.jaccard(item['min_hash'])
            if m_score > self.min_score:
                self.history.push_data(x)
                return 1

        self.history.push_data(x)
        return 0
