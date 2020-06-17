#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: algorithm_demo
@date: 2019-11-03 
"""
import time
import random


def swap( array, start, end):
    array[start], array[end] = array[end], array[start]


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
        print(t2 - t1)

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

    def binary_search(self, arr, key):
        """二分查找 key 的位置
        head = 0
        tail = len(array) - 1
        # >> 1 == //2
        pivot = (head + tail) >> 1
        """
        left = 0
        right = len(arr) - 1

        while left <= right:
            mid = (left + right) >> 1
            if arr[mid] == key:
                return mid
            elif arr[mid] > key:
                right = mid - 1
            else:
                left = mid + 1

        return -1

    def test_binary_search(self, key):
        arr = [1, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7]
        x = self.binary_search(arr, key)
        print(f'binary_search = {x}')

    def binary_search_first_equal(self, arr, key):
        """第一个 == key 的位置"""
        length = len(arr)
        left = 0
        right = length - 1

        while left <= right:
            mid = (left + right) >> 1
            if arr[mid] >= key:
                right = mid - 1
            else:
                left = mid + 1

        if left < length and arr[left] == key:
            return left
        else:
            return -1

    def test_binary_search_first_equal(self, key):
        arr = [1, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7]
        x = sol.binary_search_first_equal(arr, key)
        print(f'first_equal = {x}')

    def binary_search_last_equal(self, arr, key):
        """最后一个 == key 的位置"""
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid = (left + right) >> 1
            if arr[mid] <= key:
                left = mid + 1
            else:
                right = mid - 1

        if right >= 0 and arr[right] == key:
            return right
        else:
            return -1

    def test_binary_search_last_equal(self, key):
        arr = [1, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7]
        x = sol.binary_search_last_equal(arr, key)
        print(f'last_equal = {x}')

    def binary_search_first_greater(self, arr, key):
        """第一个 > key 的位置"""
        left = 0
        right = len(arr) - 1

        while left <= right:
            mid = left + ((right - left) >> 1)
            if arr[mid] <= key:
                left = mid + 1
            else:
                right = mid - 1
        if left >= len(arr):
            return -1
        return left

    def test_binary_search_first_greater(self, key):
        a = [1, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7]
        x = self.binary_search_first_greater(a, key)
        print(f'first_greater = {x}')

    def binary_search_first_ge(self, arr, key):
        """
        第一个 >= key 的位置
        [2,4,6,8,10], 3->4
        """
        left = 0
        right = len(arr) - 1

        while left <= right:
            mid = (left + right) >> 1
            if arr[mid] >= key:
                right = mid - 1
            else:
                left = mid + 1
        if left >= len(arr):
            return -1
        else:
            return left

    def test_binary_search_first_ge(self, key):
        a = [1, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7]
        x = self.binary_search_first_ge(a, key)
        print(f'first_ge = {x}')

    def binary_search_last_less(self, arr, key):
        """最后一个 < key 的元素的位置"""
        left = 0
        right = len(arr) - 1

        while left <= right:
            mid = left + ((right - left) >> 1)
            if arr[mid] >= key:
                right = mid - 1
            else:
                left = mid + 1
        if right < 0:
            return -1
        else:
            return right

    def test_binary_search_last_less(self, key):
        a = [1, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7]
        x = self.binary_search_last_less(a, key)
        print(f'last_less = {x}')

    def binary_search_last_le(self, arr, key):
        """最后一个 <= key 的元素的位置"""
        left = 0
        right = len(arr) - 1

        while left <= right:
            mid = left + ((right-left) >> 1)
            if arr[mid] <= key:
                left = mid + 1
            else:
                right = mid - 1

        if right < 0:
            return -1
        else:
            return right

    def test_binary_search_last_le(self, key):
        a = [1, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7]
        x = self.binary_search_last_le(a, key)
        print(f'last_le = {x}')

    def bubble_sort(self, array):
        """冒泡排序"""
        # print(array)
        # print('=======')
        length = len(array)
        for i in range(length):
            for j in range(i + 1, length):
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
            for j in range(i + 1, length):
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

    def insert_sort(self, array):
        if not array or len(array) < 2:
            return
        length = len(array)
        for i in range(1, length):
            for j in range(i-1, -1, -1):
                if array[j] > array[j+1]:
                    swap(array, j, j+1)

    def merge_sort1(self, arr):
        if not arr:
            return
        self._merge_sort1(arr, 0, len(arr)-1)

    def _merge_sort1(self, arr, left, right):
        if left == right:
            return
        mid = (left+right) >> 1
        self._merge_sort1(arr, left, mid)
        self._merge_sort1(arr, mid+1, right)
        self._merge1(arr, left, mid, right)

    def _merge1(self, arr, left, mid, right):
        """
        合并数组的有序的两部分，left~mid 与 mid+1~right，使得最后的数组依然保持有序
        :param arr:
        :param left:
        :param mid:
        :param right:
        :return:
        """
        tmp = [None] * (right-left+1)
        tmp_index = 0
        p1 = left
        p2 = right

        while p1 <= mid and p2 <= right:
            tmp[tmp_index] = min(arr[p1], arr[p2])
            tmp_index += 1
            if arr[p1] < arr[p2]:
                p1 += 1
            else:
                p2 += 1

        while p1 <= mid:
            tmp[tmp_index] = arr[p1]
            p1 += 1

        while p2 <= right:
            tmp[tmp_index] = arr[p2]
            p2 += 1

        for i, v in enumerate(tmp):
            arr[left+i] = v

    def merge_sort(self, arr, left, right):
        if left >= right:
            # print(f"base={arr[left]}")
            # print("$$$$")
            return arr[left]

        # print(f"left={left}")
        # print(f"right={right}")
        mid = left + ((right - left) >> 1)
        # print(f"mid={mid}")
        # print(f"#####")

        # print('sort left')
        self.merge_sort(arr, left, mid)
        # print('sort right')
        self.merge_sort(arr, mid + 1, right)
        # print('merge')
        self.merge(arr, left, mid, right)

    def merge(self, arr, left, mid, right):
        tmp = [None] * (right - left + 1)
        p1 = left
        p2 = mid + 1
        i = 0

        # 遍历两个交叉部分
        while p1 <= mid and p2 <= right:
            if arr[p1] < arr[p2]:
                tmp[i] = arr[p1]
                p1 += 1
                i += 1
            else:
                tmp[i] = arr[p2]
                p2 += 1
                i += 1

        # 交叉部分合并完后，把剩余部分直接追加到尾部
        while p1 <= mid:
            tmp[i] = arr[p1]
            p1 += 1
            i += 1
        while p2 <= right:
            tmp[i] = arr[p2]
            p2 += 1
            i += 1
        # print(f"left={left}")
        # print(f"right={right}")
        # print(f"origin={arr[left: right+1]}")
        # print(f"sorted={tmp}")
        # print("=======")

        # 把临时数据替换到原来的位置
        for i, v in enumerate(tmp):
            arr[left + i] = v

    def test_merge_sort(self, a):
        # a = [1, 2, 3, 4, 5, 6]
        self.merge_sort(a, 0, len(a) - 1)

    def quick_sort1(self, arr):
        if not arr or len(arr) < 2:
            return arr
        self._quick_sort1(arr, 0, len(arr)-1)

    def _quick_sort1(self, arr, left, right):
        if left < right:
            # 基于随机的选择一个值放在最后
            swap(arr, random.randint(left, right-1), right)
            l, r = self._partition1(arr, left, right)
            self._quick_sort1(arr, left, l-1)
            self._quick_sort1(arr, r+1, right)

    def _partition1(self, arr, left, right):
        """
        在数组 array 上的 left~right 范围上划分数组
        分成小于，等于，大于 arr[right] 的三部分，每一部分可以乱序
        :param arr:
        :param left:
        :param right:
        :return: (l, r) l~r范围内的数据==arr[right]
                l 表示 == arr[right] 的左边界
                r 表示 == arr[right] 的右边界
        """
        # 小于 arr[right] 的最后一个数的位置
        less = left - 1
        # 大于 arr[right] 的第一个数的位置，但是不包含最后一个位置的数字
        more = right

        while left < more:
            if arr[left] < arr[right]:
                less += 1
                swap(arr, less, left)
                left += 1
            elif arr[left] > arr[right]:
                more -= 1
                # 当前left的位置被替换，所以不需要前进，继续判断这个位置
                swap(arr, left, more)
            else:
                left += 1
        # 最后把right的位置的数也换到相等的区域
        swap(arr, more, right)

        return less+1, more

    def quick_sort(self, array):
        """快排"""
        if array is None or len(array) < 2:
            return array

        length = len(array)
        pivot = array[random.randint(0, length-1)]
        left = [i for i in array if i > pivot]
        right = [i for i in array if i < pivot]
        mid = [i for i in array if i == pivot]

        return self.quick_sort(left) + mid + self.quick_sort(right)

    def test_quick_sort(self, a):
        # a = [1, 2, 3, 4, 5, 6]
        b = self.quick_sort(a)
        # print(b)
        return b

    def heap_sort1(self, array):
        """堆排序"""
        if not array or len(array) < 2:
            return array

        size = len(array)
        # 构建大根堆
        self._heap_sort1(array, size)

        # 一次把堆顶位置的值与堆中最后一个值交换，
        # 通过 heapify 继续保持堆结构
        size -= 1
        swap(array, 0, size)
        while size > 0:
            self._heapify(array, 0, size)
            size -= 1
            swap(array, 0, size)

    def _heapify(self, array, root, size):
        """保持以 root 为根节点的大根堆在 size 范围内依然是大根堆结构"""
        left = (root << 1) + 1
        while left < size:
            right = left + 1
            largest = right if right < size and array[right] > array[left] else left
            largest = largest if array[largest] > array[root] else root
            if largest == root:
                break
            swap(array, largest, root)
            root = largest
            left = (root << 1) + 1

    def _heap_sort1(self, array, size):
        # 根据数组 array size 范围内构建大根堆
        for i in range(size):
            self._heap_insert1(array, i)

    def _heap_insert1(self, array, index):
        """把 index 位置的数插入大根堆，并保持大根堆结构"""
        parent = index - 1 >> 1
        while parent >= 0 and array[index] > array[parent]:
            swap(array, parent, index)
            index = parent
            parent = index - 1 >> 1

    def heap_sort(self, array):
        """
        堆排序
        """
        if array is None or len(array) < 2:
            return array

        length = len(array)

        # 构建一颗大根堆
        for i in range(length):
            self.heap_insert(array, i)
        print(array)
        # 此时 array 第一个元素就是最大值
        length -= 1
        swap(array, 0, length)

        while length > 0:
            self.heapify(array, 0, length)
            length -= 1
            swap(array, 0, length)

    def heap_insert(self, array, index):
        """构建大根堆"""
        parent = index-1 >> 1
        while parent >= 0 and array[index] > array[parent]:
            swap(array, index, parent)
            # array[index], array[parent] = array[parent], array[index]
            index = parent
            parent = index - 1 >> 1

    def heapify(self, array, parent, size):
        """对 array 中以 parent 为头结点的堆，在大小为 size 范围内排序"""
        left = (parent << 1) + 1
        while left < size:
            right = left + 1
            if right < size and array[right] > array[left]:
                largest = right
            else:
                largest = left

            largest = largest if array[largest] > array[parent] else parent
            if largest == parent:
                break

            swap(array, largest, parent)
            # array[parent], array[largest] = array[largest], array[parent]
            parent = largest
            left = (parent << 1) + 1

    def test_heapify_sort(self):
        a = [3, 5, 7, 2, 9, 1, 10]
        print(a)
        self.heap_sort(a)
        print(a)

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
    # arr = [4, 1, 7, 2, 2, 7, 5, 9, 6, 3]
    arr = [random.randint(1, 1000) for _ in range(100)]
    arr1 = [arr for _ in range(n)]
    arr2 = arr1.copy()
    arr3 = arr1.copy()
    arr4 = arr1.copy()

    print(arr1)

    t1 = now()
    for a1 in arr1:
        so.test_bubble_sort(a1)
        print(a1)
    t2 = now()
    print(t2 - t1)

    t3 = now()
    for a2 in arr2:
        so.test_select_sort(a2)
        print(a2)
    t4 = now()
    print(t4 - t3)

    r = None
    t5 = now()
    for a3 in arr3:
        r = so.test_quick_sort(a3)
        print(r)
    t6 = now()
    print(t6 - t5)

    t7 = now()
    for a4 in arr4:
        so.test_merge_sort(a4)
        print(a4)
    t8 = now()
    print(t8 - t7)


def binary_search_test():
    so = Solution()

    a = [1, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7]
    print(f'arr = {a}')
    so.test_binary_search(5)
    so.test_binary_search_first_equal(5)
    so.test_binary_search_last_equal(5)

    so.test_binary_search_first_ge(5)
    so.test_binary_search_first_greater(5)

    so.test_binary_search_last_le(5)
    so.test_binary_search_last_less(5)


def get_gap(array: list):
    """查找数据排序后相邻数的最大差值，时间复杂度要求O(N)，不能使用基于比较的排序"""
    if not array or len(array) < 2:
        return 0

    min_item = min(array)
    max_item = max(array)

    if min_item == max_item:
        return 0

    length = len(array)
    has_num = [False] * (length+1)
    mins = [None] * (length+1)
    maxs = [None] * (length+1)

    for item in array:
        bid = bucket(item, min_item, max_item, length)
        mins[bid] = min(mins[bid], item) if has_num[bid] else item
        maxs[bid] = max(maxs[bid], item) if has_num[bid] else item
        has_num[bid] = True

    max_num = 0
    last_max = maxs[0]

    for i in range(1, length+1):
        if has_num[i]:
            max_num = max(max_num, mins[i]-last_max)
            last_max = maxs[i]

    return max_num


def bucket(cur_num, min_num, max_num, size):
    return (cur_num-min_num)*size//(max_num-min_num)


if __name__ == '__main__':
    a = [random.randint(1, 100) for _ in range(10)]
    print(a)
    sol = Solution()
    sol.quick_sort1(a)
    print(a)
    # sol.test_find(151)
    # sol.test_replace_space('we are happy.')
    # sol.test_queue()
    # for _i in range(10):
    #     sol.test_binary_search(_i)
    # sol.test_is_pop_order()
    # compare_sort()

    # binary_search_test()

    sol.test_heapify_sort()


class MyType(type):
    def __new__(cls, *args, **kwargs):
        print(f"__new__, {args, kwargs}")
        return type.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        print(f"__init__, {args, kwargs}")

    def __call__(cls, *args, **kwargs):
        print(f"__call__, {args, kwargs}")
        obj = cls.__new__(cls, *args, **kwargs)
        obj.__init__(*args, **kwargs)
        return obj

class Foo(metaclass=MyType):
    def __init__(self):
        self.name = 'name'



from abc import ABCMeta, abstractmethod


def meth(self):
    print(f"Calling method={self.attr}")


class MyMeta(type):
    @classmethod
    def __prepare__(cls, name, baseClasses):
        return {'meth': meth}

    def __new__(cls, name, baseClasses, classdict):
        return type.__new__(cls, name, baseClasses, classdict)


def _check_methods(C, *methods):
    print(f"_check_methods C={C}, methods={methods}")
    mro = C.__mro__
    print(mro)
    for method in methods:
        for B in mro:
            if method in B.__dict__:
                if B.__dict__[method] is None:
                    return NotImplemented
                break
        else:
            return NotImplemented
    return True


class MySized(metaclass=ABCMeta):
    __slots__ = ()

    @abstractmethod
    def __len__(self):
        return 0

    @classmethod
    def __subclasshook__(cls, C):
        print(f"cls={cls}, C={C}")
        if cls is MySized:
            return _check_methods(C, "__len__")
        return NotImplemented


class Test(metaclass=MyMeta):
    attr = 'an attribute'

    def __init__(self):
        pass

    def __len__(self):
        return 0


a = Test()

isinstance(a, MySized)  # True

