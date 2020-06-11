#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: queue_demo
@date: 2020-06-10 
"""


class Queue:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError('Capacity must be > 0')
        # 最大容量
        self.capacity = capacity
        self.q = []

    def __repr__(self):
        return ','.join((str(i) for i in self.q))

    __str__ = __repr__

    def push(self, val):
        if len(self.q) >= self.capacity:
            raise RuntimeError('The queue is full')
        self.q.append(val)

    def poll(self):
        if len(self.q) <= 0:
            raise RuntimeError('The queue is empty')
        return self.q.pop(0)

    def peek(self):
        if self.q:
            return self.q[0]


class Queue2:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError('Capacity must be > 0')
        # 最大容量
        self.capacity = capacity
        self.q = [None] * capacity
        # 实际使用大小
        self.size = 0
        # 开始读取的位置
        self.start = 0
        # 可以读取的最后位置
        self.end = 0

    def push(self, val):
        if self.size >= self.capacity:
            raise RuntimeError('The queue is full')
        self.q[self.end] = val
        self.end += 1
        if self.end >= self.capacity:
            self.end = 0
        self.size += 1

    def poll(self):
        if self.size <= 0:
            raise RuntimeError('The queue is empty')
        val = self.q[self.start]
        self.start += 1
        if self.start >= self.capacity:
            self.start = 0
        self.size -= 1
        return val

    def peek(self):
        if self.size > 0:
            return self.q[self.start]


if __name__ == '__main__':
    queue = Queue(3)

    queue.push(1)
    queue.push(2)
    queue.push(3)
    print(queue)
    print(queue.peek())
    print(queue.poll())
    print(queue.poll())
    print(queue.poll())
    print(queue)
    queue.push(1)
    queue.push(2)
    print(queue.poll())
    queue.push(3)
    queue.push(4)
    print(queue.poll())
    print(queue)
