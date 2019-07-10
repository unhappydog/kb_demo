from utils.Tags import Singleton
import aiml
from aiml.constants import *
from utils.Utils import update_add_dict
from settings import BASE_DIR
import os
import json
import re


@Singleton
class AimlService:
    def __init__(self):
        aiml_path = os.path.join(BASE_DIR, "resources", "aiml")
        self.kernal = aiml.Kernel()
        self.kernal.learn(os.path.join(aiml_path, "cn-talent.aiml"))
        # self.kernal.learn(os.path.join(aiml_path,"cn-test.aiml"))
        self.kernal.respond("load aiml cn")

    def parse_info(self, text):
        result = self.kernal.respond(text)

        try:
            if result == "":
                result = {}
            else:
                # result = result.replace("} {", "}____{")
                result = re.sub("} *{", "}____{", result)
                temp_result = result.split("____")
                if len(temp_result) >= 2:
                    temp = {}
                    for result_item in temp_result:
                        print(result_item)
                        # temp.update(json.loads(result_item))
                        temp = update_add_dict(temp, json.loads(result_item))
                    result = temp
                else:
                    result = json.loads(result)
            result = self._conver_dict(result)
        except Exception as e:
            print(e)
            return {}
        return result

    def _conver_dict(self, a):
        temp = {}
        for k,v in a.items():
            if type(v) == dict:
                temp[k.strip()] = self._conver_dict(v)
            elif type(v) == str:
                if len(v) >= 8:
                    # print("{0}___________________may error".format(v))
                    v = re.split("、|，|,|；|;", v.strip())
                else:
                    v = v.strip()
                temp[k.strip()] = v
            else:
                temp[k.strip()] = v
        return temp

aimlService = AimlService()

if __name__ == '__main__':
    while True:
        print(aimlService.parse_info(input(">")))
