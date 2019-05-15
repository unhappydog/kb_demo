from utils.Tags import Singleton
from data_access.controller.CVController4Mongo import CVController4Mongo
from data_access.controller.KBTalentController4Mongo import KBTalentController4Mongo
from data_access.controller.ExperienceController4Mongo import ProjectExperienceController4Mongo
from data_access.controller.JDCompanyController4Mongo import JDCompanyController4Mongo
from services.tool_services.MongoService import mgService
from data_access.controller.NewController4Mongo import NewController4Mongo


@Singleton
class DataService:
    def __init__(self):
        self.cv_controller = CVController4Mongo()
        self.jd_controller = KBTalentController4Mongo()
        self.experienc_contorller = ProjectExperienceController4Mongo()
        self.jd_company_controller = JDCompanyController4Mongo()
        self.news_controller = NewController4Mongo()

    def save(self, cv):
        if self.cv_controller.get_data_by_id(_id=cv._id):
            self.cv_controller.update_by_id(cv)
        else:
            self.cv_controller.insert_data(cv)

    def get(self, id):
        data = self.cv_controller.get_data_by_id(_id=id)
        if data:
            return data[0]
        else:
            return None

    def delete(self, id):
        return self.cv_controller.delete_by_id(_id=id)

    def get_jd_by_name(self, name, page, limit):
        return self.jd_controller.get_talent_by_name_order_by_date(name, page, limit)

    def get_project_experience_by_name(self, name, page, limit):
        return self.experienc_contorller.get_datas_by_name(name, page=page, size=limit)

    def get_company_by_jd(self, name, page, limit):
        return self.jd_company_controller.get_data_by_job_title(name, page, limit)

    def get_news_by_tag(self, tag, page, limit):
        return self.news_controller.get_news_by_tag(tag, page=page, limit=limit)

    def get_news(self, page, limit):
        return self.news_controller.get_news(page=page, limit=limit)

    def get_news_by_domain(self, domain, page, limit):
        return self.news_controller.get_news_by_domain(domain, page=page, limit=limit)


dataService = DataService()
