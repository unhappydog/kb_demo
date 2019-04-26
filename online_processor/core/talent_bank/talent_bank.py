import re
from data_access.controller.KbTalentBankController4Mongo import KBTalentBankController4Mongo


class TalentBank:
    post_prefix = [
        "研究员",
        "科学家",
        "技术专家",
        "专家",
        "资深工程师",
        "架构师",
        "资深科学家",
        "资深研究员",
        "资深架构师",
        "专家工程师",
        "首席科学家",
        "资深专员",
        "leader",
        "总监",
        "负责人",
        "资深",
        "架构",
        "算法专家",
        "技术总",
        "算法工程师"
    ]

    def __init__(self):
        self.contoller = KBTalentBankController4Mongo()

    def save(self, cv):
        data = self.contoller.get_data_by_id(_id = cv._id)
        if data:
            self.contoller.update_by_id(cv)
        else:
            self.contoller.insert_data(cv)

    def search_by_name(self, name, page, limit):
        reg_pattern = "({0})".format("|".join(self.post_prefix))
        if re.match(".+" + reg_pattern + "$", name):
            name = re.sub(reg_pattern,'', name)
        return self.contoller.get_datas_by_keyword(keyword=name, page=page, size=limit)

    def get_by_id(self, _id):
        data =self.contoller.get_data_by_id(_id)
        if data:
            return data[0]
        else:
            return None

    def delete_by_id(self, _id):
        self.contoller.delete_by_id(_id)

    def update(self, cv):
        self.contoller.update_by_id(cv)

