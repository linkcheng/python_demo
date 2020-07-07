#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from typing import Generic, TypeVar, List

T = TypeVar("T")


class Queue(Generic[T]):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self._data = []

    def add(self, val: T):
        if self.size >= self.capacity:
            raise RuntimeError("Queue is full")
        self._data.append(val)
        self.size += 1

    def poll(self) -> T:
        if self.size <= 0:
            raise RuntimeError("Queue is empty")
        self.size -= 1
        return self._data.pop(0)

    def peek(self) -> T:
        if self.size <= 0:
            raise RuntimeError("Queue is empty")
        return self._data[0]

    def is_empty(self) -> bool:
        return self.size == 0


class Stack(Generic[T]):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self._data = []

    def push(self, val: T):
        if self.size >= self.capacity:
            raise RuntimeError("Stack is full")
        self._data.append(val)
        self.size += 1

    def pop(self) -> T:
        if self.size <= 0:
            raise RuntimeError("Stack is empty")
        self.size -= 1
        return self._data.pop(-1)

    def peek(self) -> T:
        if self.size <= 0:
            raise RuntimeError("Stack is empty")
        return self._data[-1]

    def is_empty(self) -> bool:
        return self.size == 0


def monotonic_stack(arr: List[int]) -> List[int]:
    """给定一个长度为N的整数数列，输出每个数左边第一个比它小的数，如果不存在则输出-1"""
    if not arr:
        return

    length = len(arr)
    data = Stack(length)
    res = [None] * length

    # for i in range(length-1, -1, -1):
    #     if data.is_empty():
    #         data.push(i)
    #     else:
    #         if arr[i] > arr[data.peek()]:
    #             data.push(i)
    #         else:
    #             while not data.is_empty() and arr[i] < arr[data.peek()]:
    #                 idx = data.pop()
    #                 res[idx] = arr[i]
    #             data.push(i)

    for i in range(length-1, -1, -1):
        while not data.is_empty() and arr[i] < arr[data.peek()]:
            idx = data.pop()
            res[idx] = arr[i]
        data.push(i)

    while not data.is_empty():
        idx = data.pop()
        res[idx] = -1

    return res


print(monotonic_stack([1, 2, 3, 4, 5]))
print(monotonic_stack([1, 1, 1, 1, 1]))
