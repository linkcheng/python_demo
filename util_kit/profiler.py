#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import cProfile
from functools import wraps


def profiler(fn):
    """
    print_stats(sort)
    sort 排序参数
    -1: "stdname",
    0:  "calls",
    1:  "time",
    2:  "cumulative"

    :param fn:
    :return:
    """
    @wraps(fn)
    def _profiler(*args, **kwargs):
        profile = cProfile.Profile()
        result = profile.runcall(fn, *args, **kwargs)
        profile.dump_stats("%s.cprof" % (fn.func_name,))
        # profile.print_stats(2)
        return result

    return _profiler
