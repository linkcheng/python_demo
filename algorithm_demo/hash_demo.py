#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: hash_demo 
@date: 2020-06-21 
"""
import array
import random
from typing import Dict, NoReturn, Optional


class RandomPool:
    """get_random 严格随机返回一个值，
    并且insert delete get_random 时间复杂度 O（1）"""

    def __init__(self):
        self.map1: Dict[str, int] = {}
        self.map2: Dict[int, str] = {}
        self.size: int = 0

    def insert(self, key: str) -> NoReturn:
        if key in self.map1:
            return

        self.map1[key] = self.size
        self.map2[self.size] = key
        self.size += 1

    def get_random(self) -> Optional[str]:
        if self.size == 0:
            return None
        key = random.randint(0, self.size-1)
        return self.map2.get(key)

    def delete(self, key) -> NoReturn:
        index = self.map1.pop(key, None)

        if index:
            self.size -= 1
            last_key = self.map2.pop(self.size)
            self.map1[last_key] = index
            self.map2[index] = last_key


class BitMap:
    pass


class BloomFilter:
    pass


if __name__ == '__main__':
    pass
