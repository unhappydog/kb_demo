import os
from logging import WARN, ERROR, FATAL, CRITICAL, DEBUG, INFO

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


log_file = "log.log"
error_log_file = "error.log"
log_level = DEBUG

host = "0.0.0.0"
port = 18084
