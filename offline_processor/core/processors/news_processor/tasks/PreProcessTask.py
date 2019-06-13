from core.processors.news_processor import newsProcessor
from core.common.tasks.PreProcessTask import BasePreProcessTask


@newsProcessor.add_as_processors(order=0, stage=1, key_column="_id", title_column="TITLE",
                                 content_column="CONTENT", pubtime_column="PUBTIME",
                                 brief_column="BRIEF", bad_column="ISBAD")
class PreProcessTask(BasePreProcessTask):
    def fit(self, data):
        data = super().fit(data)
        data['IMG_URL'] = data['IMG_URL'].apply(lambda x: self.process_img(x) if x else "")
        # data['IMG_URL'] = data['IMG_URL'].apply(lambda x: "" if x == "[]" else x)
        return data

    def process_img(self, images):
        # if images == "[]":
        #     # print("finded a []")
        #     return ""
        images = images.strip('[').strip(']')
        images = ";".join(image.strip('\'') for image in images.split(','))
        return images
