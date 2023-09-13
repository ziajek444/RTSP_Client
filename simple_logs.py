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
__formatter = logging.Formatter(f'[%(asctime)s] [%(levelname)s] [%(filename)s] %(message)s',
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

__valid_values = [x for x in range(48, 58)]
__valid_values += [x for x in range(65, 91)]
__valid_values += [x for x in range(97, 123)]
__single_char_range = len(__valid_values)
__log_id_list = [0] * 8


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
    return f"[{__get_log_id()}] [" + log_msg + "] "


def __get_log_id():
    global __log_id_list
    for slot_idx in range(len(__log_id_list)-1, -1, -1):
        if __log_id_list[slot_idx] >= __single_char_range-1:
            __log_id_list[slot_idx] = 0
            continue
        else:
            __log_id_list[slot_idx] += 1
        ret_str = "".join([chr(__valid_values[nr]) for nr in __log_id_list])
        return ret_str


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
    log_info("test simple_logs", to_console=True)
    __test_logging()
    for e in range(10):
        for f in range(10000):
            __get_log_id()
        log_info(__get_log_id(), to_console=True)
    log_info("pass", to_console=True)
