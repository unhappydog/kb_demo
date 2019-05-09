from core.base.BaseTask import BaseTask
from core.base.data.FixSizeDataFrame import FixSizeDataFrame
from utils.Constants import seg_suffix
from utils import Utils


#
# @newsProcessor.add_as_processors(order=1, stage=1,
#                                  content_column="CONTENT", pubtime_column="PUBTIME",
#                                  replicate_column="ISREPLICATE",
#                                  min_score=0.7, max_length=10)
class BaseDistinctTask(BaseTask):
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
        min_hash_scores = self.history.value.apply(lambda x: m.jaccard(x['min_hash']), axis=1)
        m_score = min_hash_scores.max()
        self.history.push_data(x)
        if m_score > self.min_score:
            return 1
        return 0
