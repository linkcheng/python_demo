#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from functools import wraps
import threading

IS_DEBUG = True
Lock = threading.Lock()


class Singleton(object):

    # 定义静态变量实例
    __instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance


def test_singleton_in_thread():
    print id(Singleton())


if __name__ == '__main__':
    test_singleton_in_thread()
