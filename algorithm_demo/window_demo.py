#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from typing import List, Optional
from collections import deque


def max_in_window(arr: List[int], w: int) -> Optional[List[int]]:
    """有一个数组 arr，求以大小为 w 的滑动窗口生成的最大值集合"""
    if not arr or w < 1 or len(arr) < w:
        return
    # 使用双端队列保存窗口w长度内的最大值
    qmax = deque()
    res = []
    for i, v in enumerate(arr):
        # 移除双端队列尾部比当前值小的元素
        while len(qmax) > 0 and arr[qmax[-1]] <= v:
            qmax.pop()
        qmax.append(i)
        # 判断队列头部时都有过期
        if i - qmax[0] == w:
            qmax.popleft()
        # 已经形成w长度的窗口时，才有最大值
        if i+1 >= w:
            res.append(arr[qmax[0]])

    return res


def lengthOfLongestSubstring(s: str) -> int:
    """最长连续不重复子序列"""
    if not s or s == "":
        return 0

    length = len(s)
    if length == 1:
        return 1

    data = {}
    start_ptr = 0
    end_ptr = 0
    position = [start_ptr, end_ptr]

    for i in range(length):
        if s[i] in data:
            m_len = len(data)

            # 如果有最大长度有变化，则记录
            if m_len > position[1] - position[0]:
                position[0] = start_ptr
                position[1] = end_ptr

            # 移除最早有重复值之前的数据
            old_end_ptr = data[s[i]]
            while start_ptr <= old_end_ptr:
                data.pop(s[start_ptr])
                start_ptr += 1
        end_ptr = i
        data[s[i]] = i

    m_len = len(data)
    if m_len > position[1] - position[0]:
        position[0] = start_ptr
        position[1] = end_ptr

    return position


# print(lengthOfLongestSubstring('abcda'))
# print(lengthOfLongestSubstring('abcdbfe'))
print(lengthOfLongestSubstring('abcabcbb'))


def longest_sub_array():
    """求数组中和为 0 的最长子数组"""



def calculate(string: str) -> int:
    """计算 1+2*3-(6-2)/2+(3+1)*3"""
