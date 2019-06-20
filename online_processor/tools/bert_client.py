import time
from tools.bert import BertClient
import settings

class BertTool:
    def ner(self, text):
        with BertClient(ip=settings.bert_ip, show_server_config=False, check_version=False, check_length=False, mode='NER') as bc:
            start_t = time.perf_counter()
            text = list(text)
            rst = bc.encode([text], is_tokenized=True)
            print(time.perf_counter() - start_t)
            return rst
