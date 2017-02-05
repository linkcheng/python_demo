# -*- coding: utf-8 -*-

import time
import logging
from functools import wraps


_logger = logging.getLogger(__name__)


def logger_conf(info_logger, log_lvl=logging.DEBUG):
    '''
    logging module config.
    '''
    info_format = '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'
    info_logName = './demo.log'
    info_formatter = logging.Formatter(info_format)

    info_logger.setLevel(log_lvl)

    info_handler = logging.StreamHandler()
    info_handler.setLevel(logging.INFO)

    debug_handler = logging.FileHandler(info_logName, 'a')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(info_formatter)

    info_logger.addHandler(info_handler)
    info_logger.addHandler(debug_handler)


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()

        print('Total time running %s: %s seconds' % (function.func_name, str(end - start)))
        return result

    return function_timer
