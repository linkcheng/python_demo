#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time
import logging
from functools import wraps
from datetime import datetime
from cache.cache import HangjuXfnlParamCache

FMT = '%Y-%m-%d %H:%M:%S'
time_start = datetime(1970, 1, 1)
hangju_xfnlParam_cache = HangjuXfnlParamCache()
logger = logging.getLogger(__name__)


def fn_timer(fn):
    """
    计算 fn 的运算时间
    :param fn:
    :return:
    """
    @wraps(fn)
    def function_timer(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        logger.info(fn.__name__ + ' total running time %s seconds' % str(end - start))
        return result

    return function_timer


if __name__ == '__main__':
    pass
