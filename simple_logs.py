import logging
import os
from logging.handlers import RotatingFileHandler
import traceback

pycharm_pwd_start = os.path.curdir
pycharm_pwd_start = os.path.join(pycharm_pwd_start, "newfile.log")

idx = 1
temp_log_to_rm = pycharm_pwd_start + f".{idx}"
while os.path.exists(temp_log_to_rm):
    idx += 1
    os.remove(temp_log_to_rm)
    temp_log_to_rm = pycharm_pwd_start + f".{idx}"

with open(pycharm_pwd_start, 'w'):
    pass

logger = logging.getLogger("dupa")  # Rotating Log
logger.setLevel(logging.DEBUG)
rot_handler = RotatingFileHandler(pycharm_pwd_start, maxBytes=1024*1024*100,  # 100MB
                              backupCount=1)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s] [%(funcName)s] [%(message)s]',
                              "%m-%d %H:%M:%S")
rot_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.CRITICAL)

logger.addHandler(console_handler)
logger.addHandler(rot_handler)


# logging.basicConfig(filename=pycharm_pwd_start,
#                     format='[%(asctime)s] [%(levelname)s] [%(filename)s] [%(funcName)s] [%(message)s]',
#                     filemode='a',
#                     level=logging.DEBUG)

TRACE = (logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)
MALFUNCTION = (logging.CRITICAL, logging.ERROR, logging.DEBUG)
EVENT = (logging.INFO, logging.DEBUG)
INFO = (logging.CRITICAL, logging.ERROR, logging.INFO)
WARNING = (logging.CRITICAL, logging.ERROR, logging.WARNING)
LONG_LIFE = (logging.CRITICAL, logging.ERROR)

specified_logging_lvls = TRACE


def log_debug(*args):
    global specified_logging_lvls
    if logging.DEBUG in specified_logging_lvls:
        logging._acquireLock()
        try:
            log_msg = " ".join(map(str, args))
            logger.debug(log_msg)
        finally:
            logging._releaseLock()


def log_info(*args):
    global specified_logging_lvls
    if logging.INFO in specified_logging_lvls:
        logging._acquireLock()
        try:
            log_msg = " ".join(map(str, args))
            logger.info(log_msg)
        finally:
            logging._releaseLock()


def log_warning(*args):
    global specified_logging_lvls
    if logging.WARNING in specified_logging_lvls:
        log_msg = " ".join(map(str, args))
        logger.warning(log_msg)



def log_error(*args):
    global specified_logging_lvls
    if logging.ERROR in specified_logging_lvls:
        log_msg = " ".join(map(str, args))
        logger.error(log_msg)


def log_critical(*args):
    global specified_logging_lvls
    if logging.CRITICAL in specified_logging_lvls:
        log_msg = " ".join(map(str, args))
        logger.critical(log_msg)


def asd_logging():
    # logging.debug('This is a debug message')
    # logging.info('This is an info message')
    # logging.warning('This is a warning message')
    # logging.error('This is an error message')
    # logging.critical('This is a critical message')
    # log_debug("custom logs log_debug")
    # log_info("custom logs log_info")
    # log_warning("custom logs log_warning")
    # log_error("custom logs log_error")
    # log_critical("custom logs log_critical")
    for e in range(40000):
        log_debug("custom logger log_debug ", e)
        log_info("custom logger log_info ", e)
        log_warning("custom logger log_warning ", e)
        log_error("custom logger log_error ", e)
        #log_critical("custom logger log_critical ", e)


asd_logging()
print("file size: ", os.path.getsize(pycharm_pwd_start))
