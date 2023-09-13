import logging
import os
from logging.handlers import RotatingFileHandler

__logger_dir = "logs/"
__pycharm_pwd_start = os.path.curdir
__pycharm_pwd_start = os.path.join(__pycharm_pwd_start, __logger_dir)
if not os.path.exists(__pycharm_pwd_start):
    os.mkdir(__pycharm_pwd_start)
__pycharm_pwd_start = os.path.join(__pycharm_pwd_start, "camlogger.log")

__idx = 1
__temp_log_to_rm = __pycharm_pwd_start + f".{__idx}"
while os.path.exists(__temp_log_to_rm):
    __idx += 1
    os.remove(__temp_log_to_rm)
    __temp_log_to_rm = __pycharm_pwd_start + f".{__idx}"

with open(__pycharm_pwd_start, 'w'):
    pass

__DISABLED_LOGS = 51
__ENABLED_LOGS = 10
__MAX_LOG_BYTES = 1024 * 1024 * 10  # 10MB

__logger = logging.getLogger("Rotating Log")  # Rotating Log
__logger.setLevel(__ENABLED_LOGS)
__rot_handler = RotatingFileHandler(__pycharm_pwd_start, maxBytes=__MAX_LOG_BYTES, backupCount=11)
__formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s] [%(message)s]',
                              "%m-%d %H:%M:%S")
__rot_handler.setFormatter(__formatter)
__console_handler = logging.StreamHandler()
__console_handler.setLevel(__DISABLED_LOGS)

__logger.addHandler(__console_handler)
__logger.addHandler(__rot_handler)

__TRACE = (logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)
__MALFUNCTION = (logging.CRITICAL, logging.ERROR, logging.DEBUG)
__EVENT = (logging.INFO, logging.DEBUG)
__INFO = (logging.CRITICAL, logging.ERROR, logging.INFO)
__WARNING = (logging.CRITICAL, logging.ERROR, logging.WARNING)
__LONG_LIFE = (logging.CRITICAL, logging.ERROR)

__specified_logging_lvls = __TRACE


def log_debug(*args, to_console: bool = False):
    log_msg = __log_wrapper(*args, _to_console=to_console, logging_level=logging.DEBUG)
    __logger.debug(log_msg)


def log_info(*args, to_console: bool = False):
    log_msg = __log_wrapper(*args, _to_console=to_console, logging_level=logging.INFO)
    __logger.info(log_msg)


def log_warning(*args, to_console: bool = False):
    log_msg = __log_wrapper(*args, _to_console=to_console, logging_level=logging.WARNING)
    __logger.warning(log_msg)


def log_error(*args, to_console: bool = False):
    log_msg = __log_wrapper(*args, _to_console=to_console, logging_level=logging.ERROR)
    __logger.error(log_msg)


def log_critical(*args, to_console: bool = False):
    log_msg = __log_wrapper(*args, _to_console=to_console, logging_level=logging.CRITICAL)
    __logger.critical(log_msg)


def __log_wrapper(*args, _to_console: bool = False, logging_level: int):
    global __specified_logging_lvls
    if logging_level in __specified_logging_lvls:
        log_msg = " ".join(map(str, args))
        if _to_console and __console_handler.level != __ENABLED_LOGS:
            __console_handler.setLevel(__ENABLED_LOGS)
        if not _to_console and __console_handler.level != __DISABLED_LOGS:
            __console_handler.setLevel(__DISABLED_LOGS)
    return log_msg


def __test_logging():
    __rot_handler.maxBytes = 1000000
    assert os.path.exists(__pycharm_pwd_start + ".1") is False
    for e in range(2000):
        log_debug("custom logger log_debug ", e)
        log_info("custom logger log_info ", e)
        log_warning("custom logger log_warning ", e)
        log_error("custom logger log_error ", e)
        log_critical("custom logger log_critical ", e)
    assert os.path.exists(__pycharm_pwd_start) is True
    assert os.path.exists(__pycharm_pwd_start + ".1") is False
    for e in range(2000, 10000):
        log_debug("custom logger log_debug ", e)
        log_info("custom logger log_info ", e)
        log_warning("custom logger log_warning ", e)
        log_error("custom logger log_error ", e)
        log_critical("custom logger log_critical ", e)
    assert os.path.exists(__pycharm_pwd_start) is True
    assert os.path.exists(__pycharm_pwd_start + ".1") is True
    __rot_handler.maxBytes = __MAX_LOG_BYTES


if __name__ == "__main__":
    print("test simple_logs")
    __test_logging()
    print("pass")
