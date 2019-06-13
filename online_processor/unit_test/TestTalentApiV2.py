import sys
sys.path.append(".")
import unittest
import requests
from rest_apps import create_app
import json
import os
from settings import BASE_DIR


# host = "rembern.com"


host = "localhost"
location = ["北京-北京", '上海-上海', "深圳-深圳"]
source_methods = ['upload', 'zhilian_upload', 'zhilian_search']
job_titles = ['数据挖掘工程师', '机器学习工程师', '自然语言处理工程师']
education = ['硕士', '学士', '博士']
experience= ['0-3', '3-5','5-100']


class TestRestApi(unittest.TestCase):

    def test_sourceing_v2(self):
        print("testing sourcing")
        for l,s,e1,e2 in zip(location, source_methods, education, experience):
            result = requests.get("http://{0}:18082/online/sourcing/search_talent_bank/{1}/{2}/{3}/{4}/{5}/{6}/{7}".format(host, "数据挖掘工程师",l,e2,e1,"1",1,10))
            # import pdb; pdb.set_trace()
            print(result.json())  

    def test_move_to_talent_bak(self):
        print("testing moving")
        with open(os.path.join(BASE_DIR, "resources", "one_cv.json"), 'r', encoding='utf8') as f:
            self.json_str = f.read()
        result = requests.post('http://{0}:18082/online/sourcing/move_to_talent_bank/{1}/{2}/{3}/{4}'.format(host, '机器学习', 'upload', 'up','123'), data={'json': self.json_str})
        print(result.text)
        # print(result.json())

    def test_upload_data(self):
        print("testing upload")
        files = {
            "file": open(os.path.join(BASE_DIR,'resources','智联招聘_常先生_中文_20190415_1555294995349.pdf'), 'rb')
        }
        result = requests.post("http://{0}:18082/online/talent_bank/upload/123".format(host), files=files)
        # print(result.text)

    def test_get_talent_by(self):
        print("testing get")
        for l,s,e1,e2 in zip(location, source_methods, education, experience):
            result = requests.get("http://{0}:18082/online/talent_bank/get_talent_by/{1}/{2}/{3}/{4}/{5}/{6}/{7}/{8}/{9}".format(host, 100, e2,e1,'zhilian','none',s,"1",1,10))
            # print(result.json())
        for l,j,s,e1,e2 in zip(location, job_titles,source_methods, education, experience):
            result = requests.get("http://{0}:18082/online/talent_bank/get_talent_by/{1}/{2}/{3}/{4}/{5}/{6}/{7}/{8}/{9}".format(host, 100, e2,e1,'zhilian',j,s,"1",1,10))

    def test_search_talent_by_keyword(self):
        print("testing get")
        for l,s,e1,e2 in zip(location, source_methods, education, experience):
            result = requests.get("http://{0}:18082/online/talent_bank/search_by_keyword/{10}/{1}/{2}/{3}/{4}/{5}/{6}/{7}/{8}/{9}".format(host, 100, e2,e1,'zhilian','none',s,"1",1,10,'数据挖掘工程师'))
            # print(result.json())
        for l,j,s,e1,e2 in zip(location, job_titles,source_methods, education, experience):
            result = requests.get("http://{0}:18082/online/talent_bank/search_by_keyword/{10}/{1}/{2}/{3}/{4}/{5}/{6}/{7}/{8}/{9}".format(host, 100, e2,e1,'zhilian',j,s,"1",1,10,'华为'))

    def test_add_to_favorite(self):
        print("testing add favorite")
        result = requests.get("http://{0}:18082/online/talent_bank/add_to_favorite/{1}/{2}/{3}".format(host,"b)1WTj5QHXTcHaV24piZ(w1",'weijing','admin'))
        print(result.text)

    def test_get_favorite(self):
        print("testing get favorite")
        result = requests.get("http://{0}:18082/online/talent_bank/get_favorite/{1}/{2}/{3}/{4}/{5}/{6}/{7}/{8}/{9}".format(host,"admin",'none','none','none','zhilian','None','weijing','1','10'))
        print(result.json())

    def test_remove_from_favorite(self):
        print("remove from favorite")
        result = requests.get("http://{0}:18082/online/talent_bank/remove_from_favorite/{1}/{2}/{3}".format(host,"b)1WTj5QHXTcHaV24piZ(w1",'weijing','admin'))
        print(result.text)

    def test_remove_from_favorite_v2(self):
        print("testing remove from favorite v2")
        str_data = json.dumps({"cv_list":['1','2']}, ensure_ascii=False)
        print(str_data)
        print(type(str_data))
        result = requests.post("http://{0}:18082/online/talent_bank/remove_from_favorite_v2/{1}/{2}".format(host, '1','2'), data={"json":str_data})
        print(result.text)

    def test_count_column(self):
        print("testing count column")
        result = requests.get("http://{0}:18082/online/talent_bank/count_talent_bank/{1}".format(host,'1'))
        print(result.json())

    def test_talent_map(self):
        print("testing talent map")
        result = requests.get("http://{0}:18082/online/talent_bank/gen_talent_map/{1}".format(host, "华为"))
        print(result.text)



if __name__ == '__main__':
    unittest.main()
