#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link
@module: lru_cache 
@date: 2020-06-10 
"""

from collections import OrderedDict


class LRUCache(OrderedDict):
    """不能存储可变类型对象，不能并发访问set()"""

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
        else:
            value = None

        return value

    def set(self, key, value):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
        else:
            if len(self.cache) == self.capacity:
                self.cache.popitem(last=False)  # pop出第一个item
                self.cache[key] = value
            else:
                self.cache[key] = value


class LRUCache2:
    """不借助外部数据类型，仅使用链表跟字典"""

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.help = []

    def get(self, key):
        if key in self.cache:
            self.help.remove(key)
            self.help.append(key)
        return self.cache.get(key)

    def set(self, key, value):
        if key in self.cache:
            self.help.remove(value)
        elif len(self.cache) >= self.capacity:
            self.cache.pop(self.help.pop(0))

        self.cache[key] = value
        self.help.append(key)
