from threading import Lock
import re


class CompanyNameMapper:
    _lock = Lock()
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def get_full_name(cls, company):
        company = re.sub("\(.*?\)", '', company)
        name_mapper = {
            '北京明略软件系统有限公司':'北京明略软件系统有限公司',
            '明略科技集团':'北京明略软件系统有限公司',
            '北京明略集团':'北京明略软件系统有限公司',
            '明略数据':'北京明略软件系统有限公司',
            '北京明略软件系统有限公司(明略数据)':'北京明略软件系统有限公司',
            '北京明略软件技术有限公司':'北京明略软件系统有限公司',
            '百度':'北京百度网讯科技有限公司',
            '北京百度':'北京百度网讯科技有限公司',
            '北京百度网讯科技有限公司(百度)':'北京百度网讯科技有限公司'
        }
        return name_mapper.get(company, company)

    def fuzzy_match(self, company):
        choices = []

