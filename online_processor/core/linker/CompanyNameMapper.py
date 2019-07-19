from threading import Lock


class CompanyNameMapper:

    @classmethod
    def get_full_name(cls, company):
        name_mapper = {
            '北京明略软件系统有限公司':'北京明略软件系统有限公司',
            '明略科技集团':'北京明略软件系统有限公司',
            '明略数据':'北京明略软件系统有限公司',
            '北京明略软件系统有限公司(明略数据)':'北京明略软件系统有限公司',
            '北京明略软件技术有限公司':'北京明略软件系统有限公司'
        }
        return name_mapper.get(company, company)

