#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: greedy_demo 
@date: 2020-06-24 
"""
import heapq
from typing import List, Generic, TypeVar, Callable
from functools import cmp_to_key, total_ordering

T = TypeVar('T')


def cmp(e2: T, e1: T):
    return 0 if e2 == e1 else 1 if e2 > e1 else -1


def my_cmp(x, y):
    return x - y


class PriorityQueue(Generic[T]):
    def __init__(self,
                 data: List[T] = None,
                 comparator: Callable = cmp):

        self.key = cmp_to_key(comparator)
        self.data = [self.key(i) for i in data] if data else []
        heapq.heapify(self.data)

    def peek(self):
        return self.data[0].obj if self.data else None

    def push(self, v: T):
        v = self.key(v)
        heapq.heappush(self.data, v)

    def poll(self):
        return heapq.heappop(self.data).obj if self.data else None

    def size(self):
        return len(self.data)

    def is_empty(self):
        return self.size() == 0


@total_ordering
class Node:
    def __init__(self, cost: int, profit: int):
        self.cost = cost
        self.profit = profit

    def __repr__(self):
        return f'Node[cost={self.cost}, profit={self.profit}]'

    __str__ = __repr__

    def __gt__(self, other):
        print(f'__gt__ {self}, {other}')
        return self.cost > other.cost

    def __eq__(self, other):
        print(f'__eq__ {self}, {other}')
        return self.cost == other.cost


class Solution:

    @staticmethod
    def cmp(self, other):
        # print(self, other)
        if (self + other) > (other + self):
            return 1
        elif (self + other) < (other + self):
            return -1
        else:
            return 0

    def dict_order_smallest(self, arr: List[str]):
        """一个字符串数组，拼接后字典序最小"""
        arr.sort(key=cmp_to_key(Solution.cmp))
        return '-'.join(arr)

    def test_dict_order_smallest(self):
        arr = ['b', 'cd', 'ba', 'de']
        s = self.dict_order_smallest(arr)
        print(s)

    def ipo(self, arr: List[Node], capital: int, k: int):
        """有一些项目，成本 cost，收益 profit，求不重复做项目 k 次后，收益做最大"""
        # return 0 if e2 == e1 else 1 if e2 > e1 else -1
        cmp1 = lambda e2, e1: e2.cost - e1.cost
        cmp2 = lambda e2, e1: e1.profit - e2.profit

        cost_q = PriorityQueue(arr, cmp1)

        prof_q = PriorityQueue(comparator=cmp2)

        while cost_q.peek() and cost_q.peek().cost <= capital:
            prof_q.push(cost_q.poll())

        for i in range(k):
            node = prof_q.poll()
            print(f'第{i}次，profit={node.profit}')
            capital += node.profit

            while cost_q.peek() and cost_q.peek().cost <= capital:
                prof_q.push(cost_q.poll())

            if prof_q.is_empty():
                return capital

        return capital

    def test_ipo(self):
        capital = 20
        k = 3
        # arr = [Node(10, 2), Node(15, 3), Node(30, 10), Node(25, 4), Node(28, 7)]
        arr = [Node(10, 2), Node(15, 3), Node(30, 10), Node(26, 4), Node(28, 7)]
        cnt = self.ipo(arr, capital, k)
        print(f'test_ipo={cnt}')

    def split_block(self, arr):
        """一块金条切成两半，是需要花费和长度数值一样的铜板的。
        比如长度为20的金条，不管切成长度多大的两半都要花费20个铜板。
        一群人想整分整块金条，怎么分最省铜板？
        例如给定数组{10,20,30}，代表一共三个人，整块金条长度为10+20+30=60
        金条要分成10,20,30三个部分
            如果， 先把长 度60的金条分成10和50，花费60再把长度50的金条分成20和30， 花费50 一共花费110铜板
            但是如果先把长度60的金条分成30和30，花费60 再把长度30 金条分成10和20，花费30 一共花费90铜板
        输入一个数组，返回分割的最小代价"""
        q = PriorityQueue(arr)

        cost = 0
        while q.size() > 1:
            cur = q.poll() + q.poll()
            print(cur)
            cost += cur
            q.push(cur)

        return cost

    def test_split_block(self):
        arr = [10, 20, 30]
        cost = self.split_block(arr)
        print(f'cost={cost}')


if __name__ == '__main__':
    so = Solution()
    so.test_dict_order_smallest()
    so.test_ipo()
    so.test_split_block()
