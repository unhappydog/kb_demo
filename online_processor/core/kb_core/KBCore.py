import sys
sys.path.append(".")
from services.tool_services.neo_service import NeoService


class KBCore:
    def __init__(self):
        self.neoService = NeoService.instance()

    def distinct_list(self, some_list):
        temp = set()
        result = []
        for item in some_list:
            if item['_id'] in temp:
                continue
            else:
                temp.add(item['_id'])
                result.append(item)
        return result

    def lower_dict_key(self, some_dict):
        new_dict = dict()
        for  key, value in some_dict.items():
            new_dict[key.lower()] = value
        return new_dict

    def find_entity(self, entity_label, entity_name=None, entity_id=None, limit=10):
        query = []
        if entity_name is not None:
            query.append("n.name = \"{0}\"".format(entity_name))

        if entity_id is not None:
            query.append("n._id = \"{0}\"".format(entity_id))

        if not query:
            return
        # sql = "match (n:{0})-[r]-(n2) where {1} return n,r,n2 limit {2}"
        sql = "match p1=(n:{0})-[r1]-(n1), p2=(n)-[r2]-(n2) where {1} optional match p3=(n1)-[r3]-(n2) return p1,p2,p3 limit {2}"
        # sql = "match (n:{0})-[r]-(n2) with count(n2) as b, n return n order by b desc limit {2}"
        datas = self.neoService.exec(sql.format(entity_label, " and ".join(query), limit)).data()
        # return self._parse_neo4j_nodes(datas,['n','n1','n2'], ['r1', 'r2', 'r3'])
        nodes, links = self._parse_data_from_p(datas, p_names=['p1','p2','p3'])
        is_expandable = self.check_expandable_method(nodes, links)
        for node in nodes:
            node['expandable'] = is_expandable(node)
        return nodes, links


    def _parse_neo4j_nodes(self, datas, node_names, link_names):
        nodes = []
        links = []
        _ids = set()
        for data in datas:
            for name in node_names:
                node = dict(data[name])
                node['_label'] = str(data[name].labels)[1:]
                node = self.lower_dict_key(node)
                nodes.append(node)
                _ids.add(node['_id'])

            for link_name in link_names:
                if data[link_name] is not None:
                    links.append(data[link_name])

        nodes = self.distinct_list(nodes)
        for link in links:
            link['source'] = link['from_id']
            link['target'] = link['to_id']
        links = [link for link in links if link['target'] in _ids and link['source'] in _ids]
        if_not_dual = self.check_dual_method()
        links = [link for link in links if if_not_dual(link)]

        is_expandable = self.check_expandable_method(nodes, links)
        for node in nodes:
            node['expandable'] = is_expandable(node)
        return nodes, links

    def check_dual_method(self):
        """return a method to distinct links
        """
        distinct_link = set()
        def if_not_dual(link):
            _code = "{0}_{1}".format(link['source'], link['target'])
            if _code in distinct_link:
                return False
            else:
                distinct_link.add(_code)
                return True
        return if_not_dual

    def check_expandable_method(self, nodes, links):
        """return a method to check if a node is expandable,
        this is done by query neigbor nodes of each node"""
        sql = "match (n:{0})-[r]-(n2) where {1} with count(r) as b return b"
        node_count = {node['_id']:0 for node in nodes}

        for link in links:
            node_count[link['source']] = node_count[link['source']] + 1
            node_count[link['target']] = node_count[link['target']] + 1
        def is_expandable(node):
            label = node['_label']
            count = self.neoService.exec(sql.format(label, "n._id=\"{0}\"".format(node['_id']))).data()[0]['b']
            count = int(count)
            if count> node_count[node['_id']]:
                return True
            else:
                return False
        return is_expandable

    def demo_entity(self, company=True, job=True, candidate=True, skill=True, limit=10):
        data = {}
        if company:
            data['company'] = [
            {
                "name": "华为技术有限公司",
                "_id": "5d265734944f70a97795adb2"
            },
            {'name':'明略数据',
             '_id':'5d26e787944f70a97795c570'},
            {
                "name": "北京百度网讯科技有限公司",
                "_id": "5d2480ee260311fc302234eb"
            }]

        if job:
            data['job'] = [
                {
                    "name":"机器学习工程师",
                    "_id":"机器学习工程师"
                },
                {
                "name": "数据分析师",
                "_id": "数据分析师"
            },
            {
                "name": "大数据开发工程师",
                "_id": "大数据开发工程师"
            },
            {
                "name": "数据挖掘工程师",
                "_id": "数据挖掘工程师"
            },
            {
                "name": "算法工程师",
                "_id": "算法工程师"
            },
            {
                "name": "软件工程师",
                "_id": "软件工程师"
            },
            {
                "name": "数据库开发工程师",
                "_id": "数据库开发工程师"
            },
            {
                "name": "产品经理",
                "_id": "产品经理"
            },
            {
                "name": "项目经理",
                "_id": "项目经理"
            }]

        if candidate:
            data['candidate'] = [
            {'name':'麻先生',
                 '_id':'MI27c5m8wg2OrYKUoDC(WA'},
            {
                "name": "章先生",
                "_id": "5l7Ba5gBv)(OrYKUoDC(WA"
            },
            {
                "name": "金先生",
                "_id": "f(ue4mVLgICOrYKUoDC(WA"
            },
            {
                "name": "王先生",
                "_id": "BjPv4ZffA0)cHaV24piZ(w"
            },
            {
                "name": "周先生",
                "_id": "4xsFZgsszZOOrYKUoDC(WA"
            },
            {
                "name": "付先生",
                "_id": "p8DY9uLGWxPcHaV24piZ(w"
            },
            {
                "name": "周先生",
                "_id": "rMoAzmP8Xc2OrYKUoDC(WA"
            },
            {
                "name": "郭先生",
                "_id": "cZIxVcZ7CLrz5z5n6Imc2g"
            },
            {
                "name": "刘女士",
                "_id": "r9hH5()H(euOrYKUoDC(WA"
            },
            {
                "name": "范先生",
                "_id": "ebs8ApMZwqqOrYKUoDC(WA"
            }]
        if skill:
            data['skill'] = [{
                "name": "spring",
                "_id": "5cc6dc7e1228a32f988e1c2b"
            },
            {
                "name": "Hadoop",
                "_id": "5cc6dc7d1228a32f988e1af8"
            },
            {
                "name": "hive",
                "_id": "5cc6dc7b1228a32f988e19b2"
            },
            {
                "name": "人工智能",
                "_id": "5cc6dc7c1228a32f988e19e8"
            },
            {
                "name": "图像处理",
                "_id": "5cc6dc7a1228a32f988e18ce"
            },
            {
                "name": "数据仓库",
                "_id": "5cc6dc7b1228a32f988e192d"
            },
            {
                "name": "模式识别",
                "_id": "5cc6dc7a1228a32f988e18df"
            },
            {
                "name": "shell",
                "_id": "5cc6dc7a1228a32f988e1879"
            },
            {
                "name": "神经网络",
                "_id": "5cc6dc7b1228a32f988e1965"
            },
            {
                "name": "聚类",
                "_id": "5cc6dc7b1228a32f988e1933"
            }]

        if company:
            nodes, links = self.find_entity('company', entity_name=data['company'][0]['name'])
            data['company_graph'] = {}
            data['company_graph']['nodes'] = nodes
            data['company_graph']['links'] = links

        if job:
            nodes, links = self.find_entity('job', entity_name=data['job'][0]['name'])
            data['job_graph'] = {}
            data['job_graph']['nodes'] = nodes
            data['job_graph']['links'] = links

        if candidate:
            nodes, links = self.find_entity('candidate', entity_name=data['candidate'][0]['name'])
            data['candidate_graph'] = {}
            data['candidate_graph']['nodes'] = nodes
            data['candidate_graph']['links'] = links

        if skill:
            nodes, links = self.find_entity('skill', entity_name=data['skill'][0]['name'])
            data['skill_graph'] = {}
            data['skill_graph']['nodes'] = nodes
            data['skill_graph']['links'] = links

        return data

    def demo_entity_old(self, company=True, job=True, candidate=True, skill=True, limit=10):
        sql = "match (n:{0})-[r]-(n2) with count(n2) as b, n return n order by b desc limit {1}"
        data = {}
        if company:
            companys = self.neoService.exec(sql.format("company", limit)).data()
            companys = [company['n'] for company in companys]
            data['company'] = [{'name':company['name'], '_id':company['_id']} for company in companys]
            nodes, links = self.find_entity('company', entity_name=data['company'][0]['name'])
            data['company_graph'] = {}
            data['company_graph']['nodes'] = nodes
            data['company_graph']['links'] = links

        if job:
            jobs = self.neoService.exec(sql.format("job", limit)).data()
            jobs = [job['n'] for job in jobs]
            data['job'] = [{'name':job['name'], '_id':job['_id']} for job in jobs]
            nodes, links = self.find_entity('job', entity_name=data['job'][0]['name'])
            data['job_graph'] = {}
            data['job_graph']['nodes'] = nodes
            data['job_graph']['links'] = links

        if candidate:
            candidates = self.neoService.exec(sql.format('candidate', limit)).data()
            candidates = [candidate['n'] for candidate in candidates]
            data['candidate'] = [{'name':candidate['name'],'_id':candidate['_id']} for candidate in candidates]
            nodes, links = self.find_entity('candidate', entity_name=data['candidate'][0]['name'])
            data['candidate_graph'] = {}
            data['candidate_graph']['nodes'] = nodes
            data['candidate_graph']['links'] = links

        if skill:
            skills = self.neoService.exec(sql.format('skill', limit)).data()
            skills = [skill['n'] for skill in skills]
            data['skill'] = [{'name':skill['name'],'_id':skill['_id']} for skill in skills]
            nodes, links = self.find_entity('skill', entity_name=data['skill'][0]['name'])
            data['skill_graph'] = {}
            data['skill_graph']['nodes'] = nodes
            data['skill_graph']['links'] = links

        return data

    def find_entity_by_name(self, name, label):
        sql = "match(n:{0}) where n.name=~\".*{1}.*\" return n".format(label, name)
        datas = self.neoService.exec(sql).data()
        if datas:
            datas = [dict(data['n']) for data in datas]
            return datas

    def paths_between_nodes(self, first_id, second_id, limit):
        sql = "match p=(n1)-[r*1..4]-(n2) where n1._id=\"{0}\" and n2._id=\"{1}\" return p limit {2}".format(first_id, second_id, limit)
        datas = self.neoService.exec(sql).data()
        return self._parse_data_from_p(datas)

    def _parse_data_from_p(self, datas, p_names = ['p']):
        nodes = []
        links = []
        _ids = set()
        for data in datas:
            for p_name in p_names:
                p_data = data[p_name]
                if not p_data:
                    continue
                for node in p_data.nodes:
                    _label = str(node.labels)[1:]
                    node = dict(node)
                    node['_label'] = _label
                    node = self.lower_dict_key(node)
                    nodes.append(node)
                    _ids.add(node['_id'])
                    relations = p_data.relationships
                    links.extend([dict(link) for link in relations])
        nodes = self.distinct_list(nodes)
        for link in links:
            link['source'] = link['from_id']
            link['target'] = link['to_id']
        links = [link for link in links if link['target'] in _ids and link['source'] in _ids]
        if_not_dual = self.check_dual_method()
        links = [link for link in links if if_not_dual(link)]
        return nodes, links

if __name__ == '__main__':
    kbcore = KBCore()
    a = kbcore.find_entity('job', '数据挖掘工程师')
    # a = kbcore.paths_between_nodes('cMu8HV4XIRvcHaV24piZ(w','MI27c5m8wg2OrYKUoDC(WA',200)

    print(a)
