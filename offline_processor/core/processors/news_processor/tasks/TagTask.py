from core.processors.news_processor import newsProcessor
from core.base.BaseTask import BaseTask
from data_access.controller.KBPostController4Mongo import KBPostController4Mongo
from services.NLPService import nlpService
from services.data_services.CommonDataService import commonDataService
from data_access.controller.KBPostController4Mongo import KBPostController4Mongo
import re


@newsProcessor.add_as_processors(order=2, stage=1,
                                 content_column="CONTENT", pubtime_column="PUBTIME",
                                 replicate_column="ISREPLICATE", title_column="TITLE",
                                 tag_column="Tag", domain_tag="DomainTag", company_tag="CompanyTag", related_company="companys", related_person="persons", job_tag="job_tag")
class TagTask(BaseTask):
    def __init__(self, content_column, pubtime_column, replicate_column, title_column, tag_column, domain_tag, company_tag, related_company, related_person, job_tag):
        self.title_column = title_column
        self.content_column = content_column
        self.pubtime_column = pubtime_column
        self.replicate_column = replicate_column
        self.tag_column = tag_column
        self.prefix_dict = KBPostController4Mongo().get_prefix_dict()
        self.domain_tag = domain_tag
        self.company_tag = company_tag
        self.related_company = related_company
        self.related_person = related_person
        self.companys = commonDataService.get_company_ai_top_50()
        self.job_tag = job_tag
        self.keyword_dict = KBPostController4Mongo().get_prefix_dict()

        self.keyword_dict['自然语言处理工程师'].remove('知识图谱')
        self.word_to_title = {}
        for job_title, keywords in self.keyword_dict.items():
            for keyword in keywords:
                if keyword in self.word_to_title.keys():
                    self.word_to_title[keyword].append(job_title)
                else:
                    self.word_to_title[keyword] = [job_title]
        self.word_to_title['知识图谱'] = ['知识图谱工程师']


    def fit(self, data):
        data[self.tag_column] = data[self.title_column].apply(lambda x: self.add_tag(x))
        data[self.domain_tag] = data[self.title_column].apply(lambda x: self.tag_domain(x))
        data[self.company_tag] = data[self.title_column].apply(lambda x:self.tag_company(x))
        data['ner'] = data[self.content_column].apply(lambda x: self.ner_recong(x))
        data[self.related_company] = data['ner'].apply(lambda x:self.ner_extract(x, 'Ni'))
        data[self.related_person] = data['ner'].apply(lambda x: self.ner_extract(x))
        data[self.job_tag] = data.apply(lambda x: self.related_position(x[self.title_column], x[self.content_column]), axis=1)
        return data

    def add_tag(self, x):
        if not isinstance(x, str):
            return []
        if x == "" or x is None:
            return []
        result = []

        for k, v in self.prefix_dict.items():
            for key_word in v:
                if key_word in x:
                    result.append(k)
        result.extend(self.label_title(x))

        return list(set(result))

    def tag_domain(self, x):
        if not isinstance(x, str):
            return []
        if x == "" or x is None:
            return []
        result = []
        if self.is_talent_news(x):
            result.append('talent')
        else:
            result.append('ai')
        return result

    def is_talent_news(self, title):
        pattern_talent = r'.*(招聘|应聘|面试|校招|社招|人才|职场|职业生涯|跳槽|简历|工作经验|薪酬|裸辞|辞职|试用期|找工作).*'
        if re.match(pattern_talent, title):
            return True
        return False

    def if_conference(self, title):
        pattern_conference = '.*(大会|论坛|峰会).*'
        if re.match(pattern_conference, title):
            return True

    def if_report(self, title):
        pattern_report = '.*(发布.+报告|白皮书).*|.*《.*报告》.*|.*发布.+报告.*|.*发布.+白皮书.*|.*报告:.*'
        if re.match(pattern_report, title):
            return True

    def if_school_news(self, title):
        school_pattern = '.*(高校|大学).*'
        if re.match(school_pattern, title):
            return True

    def if_invest_news(self, title):
        pattern_invest = r'.*(创投|创业|投资|融资).*'
        if re.match(pattern_invest, title):
            return True
        return False

    def if_hardware_news(self, title):
        pattern_hardware = r'.*(笔记本|游戏本|评测.+性能|工业机器人|扫地机器人|芯片|教育机器人|包装机器人|农业机器人|服务机器人|无人机|平衡车|特斯拉|智能手环|AR' \
                           r'眼镜|可穿戴设备|智能跑鞋|智能T恤|智能手表|语音机器人|智能手机|高端机).* '

        if re.match(pattern_hardware, title):
            return True

        return False

    def label_title(self, title):
        # title = re.escape(title)
        # title = title.replace('\\', '\\\\').replace('+','\+')
        try:
            title = str(title)
        except:
            print("title is error")
        if self.if_conference(title):
            return ['会议']  # 会议、论坛、峰会
        elif self.if_report(title):
            return ['行业白皮书']  # 行业白皮书
        elif self.if_school_news(title):
            return ['学校']  # school news
        elif self.if_invest_news(title):
            return ['新闻']  # 创投新闻
        elif self.if_hardware_news(title):
            return ['智能硬件']  # 智能硬件
        else:
            return ['行业资讯']  # 行业资讯

    def tag_company(self, title):
        for company in self.companys:
            if company in title:
                return company
        return ""

    def ner_recong(self,content):
        return nlpService.ner_recong(content)

    def related_position(self, title, content):
        for key,value in self.word_to_title.items():
            if key in title:
                return value
        score = {}
        for key, value in self.word_to_title.items():
            if key in content:
                score[key] = score.get(key, 0) + 1
        if score:
            score =sorted(score.items(),key=lambda x: x[1], reverse=True)
            return self.word_to_title[score[0][0]]
        else:
            return []

    def ner_extract(self, ners, ner_type="Nh"):
        return list(set([word for word in ners if word[1] == ner_type and len(word)>=2]))

