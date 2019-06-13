from core.processors.talent_processor import talentProcessor
from core.common.tasks.DistinctTask import BaseDistinctTask


@talentProcessor.add_as_processors(order=1, stage=1,
                                   content_column="JobDescription", pubtime_column="Startdate",
                                   replicate_column="ISREPLICATE",
                                   min_score=0.7, max_length=10)
class DistinctTask(BaseDistinctTask):
    pass
