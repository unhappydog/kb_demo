from core.processors.news_processor import newsProcessor
from core.common.tasks.DistinctTask import BaseDistinctTask


@newsProcessor.add_as_processors(order=1, stage=1,
                                 content_column="CONTENT", pubtime_column="PUBTIME",
                                 replicate_column="ISREPLICATE",
                                 min_score=0.7, max_length=1000)
class DistinctTask(BaseDistinctTask):
    pass
