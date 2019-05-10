import re
from data_access.controller.KbTalentBankController4Mongo import KBTalentBankController4Mongo
import datetime


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
        "算法工程师",
        "研发工程师",
        "工程师",
        "初级工程师",
        "高级工程师",
        "中级工程师",
        "技术专员",
        "开发工程师",
        "工程师",
        "开发",
        "专员",
        "高级算法工程师",
        "研究员",
        "高级",
        "算法研发",
        "算法",
        "研发",
        "主管",
        "工程师",
        "助理工程师"
    ]

    def __init__(self):
        self.contoller = KBTalentBankController4Mongo()

    def save(self, cv):
        data = self.contoller.get_data_by_id(_id = cv._id)
        if data:
            self.contoller.update_by_id(cv)
        else:
            self.contoller.insert_data(cv)

    def search_by_name(self, name, page, limit, mode):
        # reg_pattern = "({0})".format("|".join(self.post_prefix))
        # if re.match(".+" + reg_pattern + "$", name):
        #     name = re.sub(reg_pattern,'', name)
        return self.contoller.get_datas_by_name(keyword=name, page=page, size=limit, mode=mode)

    def search_by_education(self, education, page, limit, mode):
        # return self.
        return self.contoller.get_datas_by_education(education,page=page, size=limit,mode=mode)
        pass

    def search_by_source(self, source, page, limit, mode):
        return self.contoller.get_datas_by_source(source=source, page=page, size=limit, mode=mode)

    def search_by_keyword(self, keyword, page, limit):
        return self.contoller.search_datas_by_keyword(keyword=keyword, page=page, size=limit)

    def get_by_id(self, _id):
        data =self.contoller.get_data_by_id(_id=_id)
        if data:
            return data[0]
        else:
            return None

    def delete_by_id(self, _id):
        self.contoller.delete_by_id(_id)

    def update(self, cv):
        # cv.updateTime = datetime.datetime.now()
        self.contoller.update_by_id(cv)

    def get_datas(self, page, limit, mode):
        return self.contoller.get_datas_order_by(page=page, size=limit,mode=mode)

    def count_datas(self, cond):
        return self.contoller.count_datas(cond)

    def count_datas_update_after(self, time):
        return self.contoller.count_datas(cond={"updateTime":{"$gt":time}})

    def count_tags(self):
        return self.contoller.count_tags()

