#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: algorithm_demo
@date: 2019-11-03 
"""
import time
import random


class Solution:
    def find(self, target, array):
        """有序矩阵寻找数字
        1   2   3   4
        2   4   6   8
        3   5   7   9
        8  11  13  15
        """
        row_count = len(array)
        col_count = len(array[0])

        row = 0
        col = col_count - 1

        while row < row_count and col >= 0:
            value = array[row][col]
            if value == target:
                return True
            elif value < target:
                row += 1
            else:
                col -= 1

        return False

    def test_find(self, tar):
        arr = [
            [1, 2, 3, 4],
            [2, 4, 6, 8],
            [3, 5, 7, 9],
            [8, 11, 13, 15],
        ]

        print(self.find(tar, arr))

    def replace_space(self, s):
        """从字符数字 s 中找到空格并替换为 %20
        'we are happy.' -> 'we%20are%20happy.'
        """
        n = 1000
        t1 = time.time()
        for i in range(n):
            s1 = s.replace(' ', '%20')
        t2 = time.time()
        print(t2-t1)

        t1 = time.time()
        for i in range(n):
            arr = ['%20' if i == ' ' else i for i in s]
            s2 = ''.join(arr)
        t2 = time.time()
        print(t2 - t1)

    def test_replace_space(self, s):
        print(self.replace_space(s))

    def test_queue(self):

        class Stack:
            def __init__(self):
                self.a = []

            def push(self, i):
                self.a.append(i)

            def pop(self):
                if self.is_empty():
                    return None
                return self.a.pop()

            def is_empty(self):
                return len(self.a) == 0

        class Queue:
            def __init__(self):
                self.s1 = Stack()
                self.s2 = Stack()

            def push(self, i):
                self.s1.push(i)

            def pop(self):
                if self.s2.is_empty():
                    while not self.s1.is_empty():
                        self.s2.push(self.s1.pop())
                return self.s2.pop()

            def is_empty(self):
                return self.s1.is_empty() and self.s2.is_empty()

        q = Queue()
        q.push(1)
        q.push(2)
        q.push(3)
        print(q.pop())

        q.push(4)
        q.push(5)

        while not q.is_empty():
            print(q.pop())

    def binary_search(self, array, target):
        """二分查找
        head = 0
        tail = len(array) - 1
        # >> 1 == //2
        pivot = (head + tail) >> 1

        while (pivot > head) and (pivot < tail):
            if array[pivot] == target:
                return pivot
            elif array[pivot] < target:
                head = pivot
                pivot = (head + tail) >> 1
            else:
                tail = pivot
                pivot = (head + tail) >> 1

        if array[0] == target:
            return 0
        elif array[-1] == target:
            return len(array) - 1
        else:
            return -1

        """
        head = 0
        tail = len(array) - 1

        while head <= tail:
            pivot = (head + tail) >> 1
            if array[pivot] == target:
                return pivot
            elif array[pivot] < target:
                head = pivot + 1
            else:
                tail = pivot - 1

        return -1

    def test_binary_search(self, target):
        arr = [2, 3, 4, 5, 6, 7]
        print(self.binary_search(arr, target))

    def bubble_sort(self, array):
        """冒泡排序"""
        # print(array)
        # print('=======')
        length = len(array)
        for i in range(length):
            for j in range(i+1, length):
                # if array[i] > array[j]:
                if array[i] < array[j]:
                    array[i], array[j] = array[j], array[i]
            # print(array)
        # print('=======')
        # print(array)
        return array

    def test_bubble_sort(self, a):
        # a = [5, 4, 3, 2, 1]
        # a = [1, 2, 3, 4, 5, 6]
        self.bubble_sort(a)

    def select_sort(self, array):
        """选择排序"""
        length = len(array)

        # print(array)
        # print('=======')
        for i in range(length):
            k = i
            for j in range(i+1, length):
                if array[k] < array[j]:
                    k = j
            if k != i:
                array[i], array[k] = array[k], array[i]
        # print('=======')
        # print(array)
        return array

    def test_select_sort(self, a):
        # a = [1, 2, 3, 4, 5, 6]
        self.select_sort(a)

    def quick_sort(self, array):
        """快排"""
        if len(array) <= 1:
            return array

        pivot = array[0]
        left = [i for i in array if i > pivot]
        right = [i for i in array if i < pivot]
        mid = [i for i in array if i == pivot]

        return self.quick_sort(left) + mid + self.quick_sort(right)

    def test_quick_sort(self, a):
        # a = [1, 2, 3, 4, 5, 6]
        b = self.quick_sort(a)
        # print(b)
        return b

    def min_stack(self):
        """包含min函数的栈"""
        class Stack:
            def __init__(self):
                self.a = []
                self.min_value = []

            def push(self, node):
                self.a.append(node)
                if self.min_value:
                    self.min_value.append(min(self.min_value[-1], node))
                else:
                    self.min_value.append(node)

            def pop(self):
                if self.is_empty():
                    return None
                self.min_value.pop()
                return self.a.pop()

            def top(self):
                if self.is_empty():
                    return None
                return self.a[-1]

            def is_empty(self):
                return len(self.a) == 0

            def min(self):
                if self.is_empty():
                    return None
                return self.min_value[-1]

    def is_pop_order(self, push_v, pop_v):
        """
        两个整数序列，push_v 表示栈的压栈顺序，
        判断第二个序列 pop_v 是否可能为该栈的弹出顺序。
        1, 2, 3, 4, 5 压栈顺序
            4, 5, 3, 2, 1 是，
            4, 3, 5, 1, 2 不是
        :param push_v: 压栈序列
        :param pop_v: 出栈序列
        :return: bool

        首先需要一个栈，
        按照 push_v 的方式压入栈，
        弹出的时候需要循环判断，是需要继续弹出还是进行压栈操作，
        判断是否需要弹出的时机：压入后就判断
        判断需要弹出的条件：压入栈的顶部跟跟出栈序列的顶部数据相等
        """
        class Stack:
            def __init__(self):
                self.a = []

            def push(self, i):
                self.a.append(i)

            def pop(self):
                if self.is_empty():
                    return None
                return self.a.pop()

            def top(self):
                if self.is_empty():
                    return None
                return self.a[-1]

            def is_empty(self):
                return len(self.a) == 0

        s1 = Stack()
        index = 0

        for item in push_v:
            s1.push(item)

            while not s1.is_empty() and s1.top() == pop_v[index]:
                index += 1
                s1.pop()

        return s1.is_empty()

    def test_is_pop_order(self):
        push_v = [1, 2, 3, 4, 5]
        pop_v = [4, 5, 3, 2, 1]
        x = self.is_pop_order(push_v, pop_v)
        print(x)

        pop_v = [4, 3, 5, 1, 2]
        x = self.is_pop_order(push_v, pop_v)
        print(x)


def compare_sort():
    so = Solution()
    now = time.time
    n = 10
    arr = [4, 1, 7, 2, 2, 7, 5, 9, 6, 3]
    arr1 = [random.randint(1, 1000) for _ in range(200)]
    arr2 = arr1.copy()
    arr3 = arr1.copy()

    print(arr1)

    t1 = now()
    for _i in range(n):
        so.test_bubble_sort(arr1)
    t2 = now()
    print(t2-t1)
    print(arr1)

    t3 = now()
    for _i in range(n):
        so.test_select_sort(arr2)
    t4 = now()
    print(t4 - t3)
    print(arr2)

    r = None
    t5 = now()
    for _i in range(n):
        r = so.test_quick_sort(arr3)
    t6 = now()
    print(t6 - t5)
    print(r)


if __name__ == '__main__':
    sol = Solution()
    # sol.test_find(151)
    # sol.test_replace_space('we are happy.')
    # sol.test_queue()
    # for _i in range(10):
    #     sol.test_binary_search(_i)
    sol.test_is_pop_order()

