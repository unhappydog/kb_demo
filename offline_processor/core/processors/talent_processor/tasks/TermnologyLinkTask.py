from core.common.tasks.TermnologyLinkTask import BaseTermnologyLinkTask
from core.processors.talent_processor import talentProcessor


@talentProcessor.add_as_processors(stage=1, order=1, link_en_column="JobDescription", seg_column="JobDescription_seg",
                                   termnology_tag="skills")
class TermnologyLinkTask(BaseTermnologyLinkTask):
    pass