import logging
import os

pycharm_pwd_start = os.path.curdir
pycharm_pwd_start = os.path.join(pycharm_pwd_start, "newfile.log")

with open(pycharm_pwd_start, 'w'):
    pass

logging.basicConfig(filename=pycharm_pwd_start,
                    format='[%(asctime)s] [%(levelname)s] [%(filename)s] [%(funcName)s] [%(message)s]',
                    filemode='a',
                    level=logging.DEBUG)

specified_logging_lvls = (logging.CRITICAL, logging.DEBUG)


def log_debug(*args):
    global specified_logging_lvls
    if logging.DEBUG in specified_logging_lvls:
        logging._acquireLock()
        try:
            log_msg = " ".join(map(str, args))
            logging.debug(log_msg)
        finally:
            logging._releaseLock()


def log_info(*args):
    global specified_logging_lvls
    if logging.INFO in specified_logging_lvls:
        logging._acquireLock()
        try:
            log_msg = " ".join(map(str, args))
            logging.info(log_msg)
        finally:
            logging._releaseLock()


def log_warning(*args):
    global specified_logging_lvls
    if logging.WARNING in specified_logging_lvls:
        logging._acquireLock()
        try:
            log_msg = " ".join(map(str, args))
            logging.warning(log_msg)
        finally:
            logging._releaseLock()


def log_error(*args):
    global specified_logging_lvls
    if logging.ERROR in specified_logging_lvls:
        logging._acquireLock()
        try:
            log_msg = " ".join(map(str, args))
            logging.error(log_msg)
        finally:
            logging._releaseLock()


def log_critical(*args):
    global specified_logging_lvls
    if logging.CRITICAL in specified_logging_lvls:
        logging._acquireLock()
        handle_log_file()
        try:
            log_msg = " ".join(map(str, args))
            logging.critical(log_msg)
        finally:
            logging._releaseLock()


def handle_log_file():
    if os.path.getsize(pycharm_pwd_start) > 1048576:  # 100MB
        pass ## TODO set seek to begining (of file)


def asd_logging():
    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')
    log_debug("custom logs log_debug")
    log_info("custom logs log_info")
    log_warning("custom logs log_warning")
    log_error("custom logs log_error")
    log_critical("custom logs log_critical")

asd_logging()
print("file size: ", os.path.getsize(pycharm_pwd_start))