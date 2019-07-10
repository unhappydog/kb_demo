from utils.Logger import logging
from services.tool_services.neo_service import NeoService
import pandas as pd

class Neo4jMixin:

    def save_to_neo4j(self, label, x):
        if type(x) == pd.Series:
            x = x.to_dict()
        self.neoService.create(label, **x)

    def if_exists(self, label, _id):
        try:
            data = self.neoService.exec("match (n:{0}) where n._id=\"{1}\" return n".format(label, _id)).data()
        except Exception as e:
            logging.exception("error occured when checking if exists")
            return True

        if data:
            return True
        else:
            return False

    def save_relation(self, relation):
        relation_str = [ "{0}:\"{1}\"".format(k,v) for k,v in relation.items()]
        relation_str = "{" +",".join(relation_str) + "}"

        try:
            data = self.neoService.exec("match (n1:{0})-[r:{4}]-(n2:{1}) where n1._id =\"{2}\" and n2._id =\"{3}\" return r".format(
            relation['from_type'],
            relation['to_type'],
            relation['from_id'],
            relation['to_id'],
            relation['name'])).data()
            if data:
                return

        except Exception as e:
            logging.exception("check duplicate error")

        sql = "match (n1:{0}), (n2:{1}) where n1._id =\"{2}\" and n2._id =\"{3}\" create (n1)-[r:{4} {5}]->(n2)".format(
            relation['from_type'],
            relation['to_type'],
            relation['from_id'],
            relation['to_id'],
            relation['name'],
            relation_str)
        try:
            self.neoService.exec(sql)
        except Exception as e:
            logging.error("create relation error")
            logging.exception("save relation error")
