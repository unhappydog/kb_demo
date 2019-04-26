from utils.Tags import Singleton
from core.talent_bank.talent_bank import TalentBank


@Singleton
class TalentBankService:
    def __init__(self):
        self.talent_bank = TalentBank()

    def save(self, cv):
        self.talent_bank.save(cv)

    def search_by_name(self, name, page, size):
        return self.talent_bank.search_by_name(name, page,size)

    def get_by_id(self, id):
        return self.talent_bank.get_by_id(id)

    def delete_by_id(self, id):
        self.talent_bank.delete_by_id(id)

    def update(self, cv):
        self.talent_bank.update(cv)

tbService = TalentBankService()