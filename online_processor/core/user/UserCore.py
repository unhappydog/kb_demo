from data_access.controller.UserController4Mongo import UserController4Mongo
from data_access.models.User import User
from utils.Logger import logging


class UserCore:
    def __init__():
        self.controller = UserController4Mongo()

    def add_user(_id, followed_company=None, followed_academy=None, followed_skill=None):
        user = User()
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

    def get_user(_id):
        users = sef.controller.get_data_by_id(_id=_id)
        if users:
            return users[0]
        else:
            return None

