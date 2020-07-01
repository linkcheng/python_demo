#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from typing import Generic, TypeVar, List, Optional
from functools import total_ordering
from random import randint

T = TypeVar('T')
MAX_DEPTH = 4


@total_ordering
class Maximum:
    def __eq__(self, value):
        return False

    def __gt__(self, value):
        return True


@total_ordering
class Minimum:
    def __eq__(self, value):
        return False

    def __lt__(self, value):
        return True


class SkipListNode(Generic[T]):
    def __init__(self, val: T, height: int = 1):
        self.val = val
        # 每一个值都指向这一层的下一个节点
        self.next_node: List[SkipListNode] = [None] * height

    def __repr__(self):
        return f'SkipListNode[val={self.val}, next_height={len(self.next_node)}]'


class SkipList:
    def __init__(self):
        self.head = SkipListNode(Minimum())

    def random_height(self) -> int:
        """随机计算跳表高度"""
        k = 1
        while randint(0, 1):
            k += 1
            if k > MAX_DEPTH:
                break
        return k

    def insert(self, val):
        """在调表中插入数据"""
        height = self.random_height()
        node = SkipListNode(val, height)

        max_height = len(self.head.next_node)
        # 调表头节点【全局最小】的高度调整
        while len(self.head.next_node) < height:
            self.head.next_node.append(node)

        start_height = min(height, max_height)
        cur = self.head
        # 负责从上到下移动
        for i in range(start_height-1, -1, -1):
            # 负责前后移动，如果下一跳的值小于当前值，则继续后跳
            while cur.next_node[i] and cur.next_node[i].val < val:
                cur = cur.next_node[i]
            # 先在next_node前插入新节点node，然后cur再指向node
            node.next_node[i] = cur.next_node[i]
            cur.next_node[i] = node

    def remove(self, val: int) -> Optional[SkipListNode]:
        """删除节点"""
        res: SkipListNode = self.search(val)
        if not res:
            return

        height = len(self.head.next_node)
        cur = self.head
        for i in range(height-1, -1, -1):
            while cur.next_node and cur.next_node[i].val < val:
                cur = cur.next_node[i]

            if cur.next_node and cur.next_node[i] == res:
                cur.next_node[i] = res.next_node[i]

        return res

    def search(self, val) -> Optional[SkipListNode]:
        """搜索节点"""
        cur = self.head
        height = len(self.head.next_node)

        for i in range(height-1, -1, -1):
            while cur.next_node[i] and cur.next_node[i].val < val:
                cur = cur.next_node[i]
            if cur.next_node[i] and cur.next_node[i].val == val:
                print(f'i={i}')
                break

        try:
            res = cur.next_node[i] if cur.next_node[i].val == val else None
        except Exception as e:
            print(e)
            res = None
        return res


sl = SkipList()

for i in range(0, 32, 2):
    sl.insert(i)

cur = sl.head
while cur:
    print(cur)
    cur = cur.next_node[0]

print(sl.search(14))
print(sl.search(25))
print(sl.search(34))

print(sl.remove(16))
print(sl.remove(27))


cur = sl.head
while cur:
    print(cur)
    cur = cur.next_node[0]
