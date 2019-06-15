from data_access.controller.UserController4Mongo import UserController4Mongo
from data_access.models.User import User
from utils.Logger import logging


class UserCore:
    def __init__(self):
        self.controller = UserController4Mongo()

    def add_user(self,_id, followed_company=None, followed_academy=None, followed_skill=None):
        user = User(_id=_id)
        if followed_skill:
            user.followed_skill = followed_skill if type(followed_skill) == list else [followed_skill]

        if followed_company:
            user.followed_company = followed_company if type(followed_company) == list else [followed_company]

        if followed_academy:
            user.followed_academy = followed_academy if type(followed_academy) == list else [followed_academy]

        if self.controller.get_data_by_id(_id=_id):
            logging.error("user {0} has already exists".format(_id))
            return False
        else:
            self.controller.insert_data(user)
            return True

    def get_user(self,_id):
        users = self.controller.get_data_by_id(_id=_id)
        if users:
            return users[0]
        else:
            return None

    def update_add_interest(self,_id, followed_company=None, followed_academy=None, followed_skill=None, max_number=5):
        interests = self.get_interest_by_id(_id)
        result = {}
        # import pdb; pdb.set_trace()

        if followed_company:
            companies = interests['followed_company']
            if len(companies) >= max_number:
                result = {"result":"failed", "log":">5"}
                followed_company = None
            elif followed_company in companies:
                result = {'result':'failed', 'log':'already followed'}
                followed_company = None
            else:
                result = {'result':'success'}

        if followed_academy:
            academies = interests['followed_academy']
            if len(academies) >= max_number:
                result = {"result":"failed", "log":">5"}
                followed_academy = None
            elif followed_academy in academies:
                result = {'result':'failed', 'log':'already followed'}
                followed_academy = None
            else:
                result = {'result':'success'}

        if followed_skill:
            skills = interests['followed_skill']
            if len(skills) >= max_number:
                result = {"result":"failed", "log":">5"}
                followed_skill = None
            elif followed_skill in skills:
                result = {'result':'failed', 'log':'already followed'}
                followed_skill = None
            else:
                result = {'result':'success'}

        # import pdb; pdb.set_trace()
        try:
            if followed_skill or followed_company or followed_academy:
                self.controller.update_add_interest(_id, followed_company, followed_academy, followed_skill)
        except Exception as e:
            result = {'result':'failed', 'log':'unhandle exception'}
        return result

    def update_remove_interest(self,_id, followed_company=None, followed_academy=None, followed_skill=None):
        self.controller.update_remove_interest(_id, followed_company, followed_academy, followed_skill)

    def get_interest_by_id(self,_id,followed_company=True, followed_academy=True, followed_skill=True):
        return self.controller.get_interest_by_id(_id, followed_company, followed_academy, followed_skill)

    def is_followed(self,company_result, academy_result, terminology_result, user_id):
        interests = self.get_interest_by_id(user_id)
        result = {}
        # import pdb; pdb.set_trace()
        if company_result:
            followed_company = interests['followed_company']
            for k,v in company_result.items():
                if k in followed_company:
                    v['is_followed'] = True
                else:
                    v['is_followed'] = False
            result['companies'] = company_result
        else:
            result['companies'] = {}
        if academy_result:
            followed_academy = interests['followed_academy']
            for k,v in academy_result.items():
                if k in followed_academy:
                    v['is_followed'] = True
                else:
                    v['is_followed'] = False
            result['academies'] = academy_result
        else:
            result['academies'] = {}

        if terminology_result:
            followed_skill = interests['followed_skill']
            terminology = self._is_termnolgoy_followed(terminology_result, followed_skill)
            result['terminologys'] = terminology_result
        else:
            result['terminologys'] = {}

        return result

    def _is_termnolgoy_followed(self, terminology_result, followed_skill):
        for k, v in terminology_result.items():
            if k == 'terminology_detail':
                if v['name'] in followed_skill:
                    v['is_followed'] = True
                else:
                    v['is_followed'] = False
            elif type(v) == list:
                for item in v:
                    self._is_termnolgoy_followed(item, followed_skill)
            elif type(v) == dict:
                self._is_termnolgoy_followed(v, followed_skill)
        return terminology_result
