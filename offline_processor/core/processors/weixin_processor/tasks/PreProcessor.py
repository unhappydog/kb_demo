from core.processors.weixin_processor import weixinProcessor
from core.common.tasks.PreProcessTask import BasePreProcessTask


@weixinProcessor.add_as_processors(order=0, stage=1, key_column="_id", title_column="TITLE",
                                 content_column="CONTENT", pubtime_column="PUBTIME",
                                 brief_column="BRIEF", bad_column="ISBAD")
class PreProcessor(BasePreProcessTask):
    pass