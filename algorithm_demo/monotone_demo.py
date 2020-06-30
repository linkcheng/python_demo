#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# 单调栈使用

from typing import List


def monotone_stack(arr: List) -> List[List[int]]:
    """求数组中每个元素它的左右两边第一个比它大的元素"""
    stack = []
    res = [None] * len(arr)
    for i, v in enumerate(arr):
        # 弹出时记录左右比当前值大的元素
        while len(stack) > 0 and arr[stack[-1]] < v:
            t = stack.pop(-1)
            left = None
            if len(stack) > 0:
                left = arr[stack[-1]]
            res[t] = [left, arr[i]]
        stack.append(i)

    while len(stack) > 1:
        t = stack.pop(-1)
        res[t] = [arr[stack[-1]], None]
    res[stack[0]] = [None, None]
    return res


print(monotone_stack([3, 2, 4, 1, 0, 5]))
