from utils.Tags import Singleton
from core.talent_bank.talent_bank import TalentBank


@Singleton
class TalentBankService:
    def __init__(self):
        self.talent_bank = TalentBank()

    def save(self, cv):
        self.talent_bank.save(cv)

    def search_by_name(self, name, page, size, mode):
        return self.talent_bank.search_by_name(name, page, size, mode)

    def search_by_education(self, education, page, size, mode):
        return self.talent_bank.search_by_education(education, page, size, mode)

    def search_by_source(self, source, page, size, mode):
        return self.talent_bank.search_by_source(source, page, size, mode)

    def get_by_id(self, id):
        return self.talent_bank.get_by_id(id)

    def delete_by_id(self, id):
        self.talent_bank.delete_by_id(id)

    def update(self, cv):
        self.talent_bank.update(cv)

    def get_datas(self, page, size, mode):
        return self.talent_bank.get_datas(page, size, mode)

    def count_all_data(self):
        return self.talent_bank.count_datas({})

    def count_data_after(self,time):
        return self.talent_bank.count_datas_update_after(time)

    def count_tags(self):
        return self.talent_bank.count_tags()


tbService = TalentBankService()
