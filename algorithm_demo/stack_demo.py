#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: stack_demo
@date: 2020-06-10 
"""


class Stack:
    def __init__(self, capacity=None):
        self.capacity = capacity
        self.data = []

    def push(self, val):
        if self.capacity and len(self.data) >= self.capacity:
            raise RuntimeError('The stack is full')
        self.data.append(val)

    def pop(self):
        if len(self.data) <= 0:
            raise RuntimeError('The stack is empty')
        return self.data.pop()

    def peek(self):
        if len(self.data) > 0:
            return self.data[-1]


if __name__ == '__main__':
    stack = Stack(3)
    print(stack.peek())
    stack.push(3)
    stack.push(2)
    stack.push(1)
    print(stack.pop())
    print(stack.pop())
    print(stack.pop())

    stack.push(1)
    print(stack.pop())
    print(stack.peek())
