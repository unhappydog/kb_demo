import logging
import settings
import sys
from settings import BASE_DIR
from logging.handlers import RotatingFileHandler
import os

log_file = os.path.join(BASE_DIR, "logs", settings.log_file)
error_log_file = os.path.join(BASE_DIR, "logs", settings.error_log_file)
logging.basicConfig(level=settings.log_level,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=log_file,
                    filemode='w+')

console = logging.StreamHandler()
# console = logging.FileHandler(log_file, encoding='utf8')
# console = RotatingFileHandler(log_file, maxBytes=1024, backupCount=4, encoding='utf8')
# console.namer = lambda x:"backup."+x.split(".")[-1]
console.setLevel(settings.log_level)
formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

error_log = logging.FileHandler(error_log_file, encoding='utf8')
error_log.setLevel(logging.ERROR)
error_log.setFormatter(formatter)
logging.getLogger().addHandler(error_log)

logging = logging

# def info(msg):
#     logging.info(msg)
#
#
# def debug(msg):
#     logging.debug(msg)
#
#
# def waring(msg):
#     logging.warning(msg)
#
#
# def error(msg, e=None):
#     logging.error(msg,e, exc_info=True, stack_info=True)
#     # logging.exception(msg,e)
#
#
# def exception():
#     logging.exception(sys.exc_info())


if __name__ == '__main__':
    a = Exception()
    try:
        logging.info("test")
        print(1/0)
    except Exception as e:
        # logging.exception('a', sys.exc_info())
        logging.exception(e)