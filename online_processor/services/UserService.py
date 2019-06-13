from core.user.UserCore import UserCore
from threading import Lock


class UserService:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self.userCore = UserCore()

    @classmethod
    def instance(cls):
        if UserService._instance is None:
            with UserService._lock:
                if UserService._instance is None:
                    UserService._instance = UserService()
        return UserService._instance

    def add_user(self,_id, followed_company=None, followed_academy=None, followed_skill=None):
        self.userCore.add_user(_id, followed_company, followed_academy, followed_skill)

    def get_user(self,_id):
        return self.userCore.get_user(_id)

    def update_add_interest(self,_id, followed_company=None, followed_academy=None, followed_skill=None):
        return self.userCore.update_add_interest(_id, followed_company, followed_academy, followed_skill)

    def update_remove_interest(self,_id, followed_company=None, followed_academy=None, followed_skill=None):
        return self.userCore.update_remove_interest(_id, followed_company, followed_academy, followed_skill)

    def get_interest_by_id(self,_id, followed_company,followed_academy, followed_skill):
        return self.userCore.get_interest_by_id(_id, followed_company, followed_academy, followed_skill)

    def is_followed(self,company_result, academy_result, terminology_result, user_id):
        return self.userCore.is_followed(company_result, academy_result, terminology_result, user_id)
