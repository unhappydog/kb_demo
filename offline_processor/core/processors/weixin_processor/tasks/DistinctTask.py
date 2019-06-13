from core.processors.weixin_processor import weixinProcessor
from core.common.tasks.DistinctTask import BaseDistinctTask


@weixinProcessor.add_as_processors(order=1, stage=1,
                                   content_column="CONTENT", pubtime_column="PUBTIME",
                                   replicate_column="ISREPLICATE",
                                   min_score=0.7, max_length=10)
class DistinctTask(BaseDistinctTask):
    pass
