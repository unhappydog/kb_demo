import os
from logging import WARN, ERROR, FATAL, CRITICAL, DEBUG, INFO

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

neo_host = "rembern.com"
neo_port = 32475

mysql_host = "172.16.6.10"
mysql_port = 32306
mysql_user = "xiaolong"
mysql_password = '123456'
mysql_db = "kb_demo"

mongo_host = "172.16.6.10"
mongo_port = 32317
# mongo_host = "127.0.0.1"
# mongo_port = 27017
mongo_db = "kb_demo"
# mongo_table="kb_tablent_table"

log_file = "log.log"
error_log_file = "error.log"
log_level = DEBUG

redis_host = "rembern.com"
redis_port = "32379"

host = "0.0.0.0"
port = 18082

bert_ip = "gpu1"
bert_in_port = 5555
bert_out_port = 5556
