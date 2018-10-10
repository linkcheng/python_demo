#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from functools import wraps

IS_DEBUG = True


def fn_timer(function):
    """
    计算 function 的运算时间
    :param function:
    :return:
    """
    @wraps(function)
    def function_timer(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()

        print('Total time running %s: %s seconds' % (function.func_name, str(end - start)))
        return result

    return function_timer


def partition(lists, low, high):
    key = lists[low]

    while low < high:
        while low < high and lists[high] >= key:
            high -= 1
        lists[low] = lists[high]
        while low < high and lists[low] <= key:
            low += 1
        lists[high] = lists[low]

    lists[low] = key
    return low


def quick_sort(arr, low, high):
    if IS_DEBUG:
        print('low=%d, high=%d' % (low, high)),
        print(arr)
    if low < high:
        key_index = partition(arr, low, high)
        quick_sort(arr, low, key_index)
        quick_sort(arr, key_index+1, high)
    return arr


def pythonic_quick_sort(a):
    if len(a) <= 1:
        return a

    pivot = a[-1]
    pivots = [i for i in a if i == pivot]
    left = pythonic_quick_sort([i for i in a if i < pivot])
    right = pythonic_quick_sort([i for i in a if i > pivot])

    return left + pivots + right


def insert_sort(arr):
    """
    插入排序, 将一个数据插入到已经排好序的有序数据中，从而得到一个新的、个数加一的有序数据
    :param arr:
    :return:
    """
    for i in range(1, len(arr)):
        key = arr[i]
        for j in range(i-1, -1, -1):
            if arr[j] > key:
                arr[j+1], arr[j] = arr[j], key
        if IS_DEBUG:
            print('i=%d, ' % i),
            print(arr)

    return arr


def bubble_sort(arr):
    """
    冒泡排序, 它重复地走访过要排序的数列，一次比较两个元素，如果他们的顺序错误就把他们交换过来。
    走访数列的工作是重复地进行直到没有再需要交换，也就是说该数列已经排序完成。
    :param arr:
    :return:
    """
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[j] < arr[i]:
                arr[i], arr[j] = arr[j], arr[i]
        if IS_DEBUG:
            print('i=%d, ' % i),
            print(arr)
    return arr


from heapq import merge


def merge1(a, b):
    temp = []
    i = j = 0
    la = len(a)
    lb = len(b)

    while i < la and j < lb:
        if a[i] < b[j]:
            temp.append(a[i])
            i += 1
        else:
            temp.append(b[j])
            j += 1

    remain, r = (a, i) if i < j else (b, j)

    lr = len(remain)
    while r < lr:
        temp.append(remain[r])
        r += 1

    return temp


def merge2(left, right):
    merged = []

    while left and right:
        merged.append(left.pop(0) if left[0] <= right[0] else right.pop(0))

    while left:
        merged.append(left.pop(0))

    while right:
        merged.append(right.pop(0))

    return merged


def merge_sort(array):
    length = len(array)
    if length <= 1:
        return array

    mid = length // 2
    left = merge_sort(array[:mid])
    right = merge_sort(array[mid:])

    return list(merge(left, right))


@fn_timer
def sort_main():
    array = [
        8, 10, 9, 6, 4, 5, 2, 1, 7, 3,
    ]
    print(array)
    for i in range(1):
        # new_array = array.sort()
        # new_array = sorted(array)
        new_array = quick_sort(array, 0, len(array) - 1)
        # new_array = pythonic_quick_sort(array)
        # new_array = insert_sort(array)
        # new_array = bubble_sort(array)

    print(new_array)
    print(array)

if __name__ == '__main__':
    sort_main()
