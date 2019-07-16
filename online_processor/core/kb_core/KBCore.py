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
        sql = "match (n:{0})-[r1]-(n1), (n)-[r2]-(n2) where {1} optional match (n1)-[r3]-(n2) return r1,r2,r3,n,n1,n2 limit {2}"
        # sql = "match (n:{0})-[r]-(n2) with count(n2) as b, n return n order by b desc limit {2}"
        datas = self.neoService.exec(sql.format(entity_label, " and ".join(query), limit)).data()
        nodes = []
        links = []
        _ids = set()
        for data in datas:
            node = dict(data['n'])
            node['_label'] = str(data['n'].labels)[1:]
            node = self.lower_dict_key(node)
            nodes.append(node)
            _ids.add(node['_id'])

            node_2 = dict(data['n2'])
            node_2['_label'] = str(data['n2'].labels)[1:]
            node_2 = self.lower_dict_key(node_2)
            nodes.append(node_2)
            _ids.add(node_2['_id'])

            node_3 = dict(data['n1'])
            node_3['_label'] = str(data['n1'].labels)[1:]
            node_3 = self.lower_dict_key(node_3)
            nodes.append(node_3)
            _ids.add(node_3['_id'])

            links.append(data['r1'])
            links.append(data['r2'])
            if data['r3'] is not None:
                links.append(data['r3'])
        nodes = self.distinct_list(nodes)
        for link in links:
            link['source'] = link['from_id']
            link['target'] = link['to_id']
        links = [link for link in links if link['target'] in _ids and link['source'] in _ids]
        return nodes, links

    def demo_entity(self, company=True, job=True, candidate=True, skill=True, limit=10):
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



if __name__ == '__main__':
    kbcore = KBCore()
    a = kbcore.find_entity('job', '数据挖掘工程师')
    print(a)
