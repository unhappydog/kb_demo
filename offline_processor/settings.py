import os
from logging import WARN, ERROR, FATAL, CRITICAL, DEBUG, INFO

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

neo_host = "rembern.com"
neo_port = 32475

mysql_host = "rembern.com"
mysql_port = 32306
mysql_user = "xiaolong"
mysql_password = '123456'
mysql_db = "kb_demo"

mongo_host = "rembern.com"
mongo_port = 32317
mongo_db = "kb_demo"
# mongo_table="kb_tablent_table"

log_file = "log.log"
error_log_file = "error.log"
log_level = DEBUG

redis_host = "rembern.com"
redis_port = "32379"

bert_ip = "172.16.10.254"
bert_in_port = 5555
bert_out_port = 5556

nlp_core = "jieba" # ltp
nlp_host = "rembern.com"
nlp_port = "18084"
