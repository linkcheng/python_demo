#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from cache.cache import HangjuXfnlParamCache, LocationCache


def init_cache():
    """缓存初始化"""
    HangjuXfnlParamCache().init()
    LocationCache().init()


if __name__ == '__main__':
    init_cache()
