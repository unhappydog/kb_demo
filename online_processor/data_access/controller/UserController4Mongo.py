from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from utils.Logger import logging
from data_access.base.BaseMongoController import BaseMongoController
from data_access.models.User import User
from bson.objectid import ObjectId
from services.tool_services.MongoService import mgService
import settings

@DataMap(_schema=settings.mongo_db, _table="kb_user")
class UserController4Mongo(BaseMongoController):
    @return_type(User)
    def get_data_by_id(self, _id=None):
        spec = {"_id":_id}
        return mgService.query(spec,
                               self._schema,
                               self._table)

    def update_add_interest(self,_id, followed_company=None, followed_academy=None, followed_skill=None):
        spec = {"_id":_id}
        doc = {'$push':{}}
        if followed_company:
            if type(followed_company) == list:
                # doc = {'$push':{
                #     'followed_company': {'$each': followed_company}
                # }}
                doc['$push']['followed_company'] ={'$each': followed_company}
            else:
                # doc = {'$push':{
                #     'followed_company':followed_company
                # }}
                doc['$push']['followed_company'] =followed_company


        if followed_academy:
            if type(followed_academy) == list:
                # doc = {'$push':{
                #     'followed_academy': {'$each': followed_academy}
                # }}
                doc['$push']['followed_academy']={'$each': followed_academy}
            else:
                # doc = {'$push':{
                #     'followed_academy':followed_academy
                # }}
                doc['$push']['followed_academy']= followed_academy
        if followed_skill:
            if type(followed_skill) == list:
                doc['$push']['followed_skill'] = {'$each': followed_skill}
                # doc = {'$push':{
                #     'followed_skill':{'$each': followed_skill}
                # }}
            else:
                doc['$push']['followed_skill'] = followed_skill
                # doc = {'$push':{
                #     'followed_skill':followed_skill
                # }}
        mgService.update_without_set(spec, doc, self._schema, self._table)
        return True

    def update_remove_interest(self, _id, followed_company=None, followed_academy=None, followed_skill=None):
        spec = {"_id":_id}
        doc = {'$pull':{}}
        if followed_company:
            if type(followed_company) == list:
                # doc = {'$pull':{
                #     'followed_company': {'$each': followed_company}
                # }}
                doc['$pull']['followed_company'] ={'$each': followed_company}
            else:
                # doc = {'$pull':{
                #     'followed_company':followed_company
                # }}
                doc['$pull']['followed_company'] =followed_company


        if followed_academy:
            if type(followed_academy) == list:
                # doc = {'$pull':{
                #     'followed_academy': {'$each': followed_academy}
                # }}
                doc['$pull']['followed_academy']={'$each': followed_academy}
            else:
                # doc = {'$pull':{
                #     'followed_academy':followed_academy
                # }}
                doc['$pull']['followed_academy']= followed_academy
        if followed_skill:
            if type(followed_skill) == list:
                doc['$pull']['followed_skill'] = {'$each': followed_skill}
                # doc = {'$pull':{
                #     'followed_skill':{'$each': followed_skill}
                # }}
            else:
                doc['$pull']['followed_skill'] = followed_skill
                # doc = {'$pull':{
                #     'followed_skill':followed_skill
                # }}
        mgService.update_without_set(spec, doc, self._schema, self._table)
        return True

    def get_interest_by_id(self, _id,followed_company=True, followed_academy=True, followed_skill=True):
        user = self.get_data_by_id(_id)
        if user:
            user = user[0]
        else:
            return {}
        result = {}
        if followed_company:
            result['followed_company'] = user['followed_company']
        if followed_academy:
            result['followed_academy'] = user['followed_academy']
        if followed_skill:
            result['followed_skill'] = user['followed_skill']
        return result
