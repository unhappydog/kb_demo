import os
from logging import WARN, ERROR, FATAL, CRITICAL, DEBUG, INFO

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

neo_host = "centos1"
neo_port = 32474

mysql_host = "centos1"
mysql_port = 32306
mysql_user = "root"
mysql_password = '111111'
mysql_db = "kb_demo"

mongo_host = "centos1"
mongo_port = 32317
mongo_db = "kb_demo"
# mongo_table="kb_tablent_table"

log_file = "log.log"
error_log_file = "error.log"
log_level = DEBUG

redis_host = ""
redis_port = ""

host = "0.0.0.0"
port = 18081
