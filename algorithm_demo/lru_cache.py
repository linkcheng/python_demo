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

    def get(self, key, default=None):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
        else:
            value = default
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

    def get1(self, key, default=None):
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        except KeyError:
            return default

    def set1(self, key, value):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value


class LRUCache2:
    """不借助外部数据类型，仅使用链表跟字典"""

    def __init__(self, capacity):
        self.capacity = capacity
        # k:v
        self.cache = {}
        # k
        self.help = []

    def get(self, key, default=None):
        if key in self.cache:
            self.help.remove(key)
            self.help.append(key)
        return self.cache.get(key) or default

    def set(self, key, value):
        if key in self.cache:
            self.help.remove(key)
        elif len(self.cache) >= self.capacity:
            self.cache.pop(self.help.pop(0))

        self.cache[key] = value
        self.help.append(key)
