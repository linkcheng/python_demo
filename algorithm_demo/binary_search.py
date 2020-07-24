#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
[(15, 0, 16, 20), (18, 30, 19, 20), (20, 10, 20, 30)]
(16, 10)
"""

from typing import List


def contains(intervals: List[List[int]], moment: List[int]) -> bool:
    if not intervals:
        return False

    monment_int = moment[0] * 100 + moment[1]
    idx = find_last_lte(intervals, monment_int)
    if idx == -1:
        return False

    possible = intervals[idx]
    return possible[0] * 100 + possible[1] <= moment[0] * 100 + moment[1] <= possible[2] * 100 + possible[3]


def find_last_lte(intervals, moment) -> int:
    """开始时间比 moment 小的最大的那个"""
    left = 0
    right = len(intervals) - 1

    while left <= right:
        mid = (left + right) >> 1
        val = intervals[mid][0] * 100 + intervals[mid][1]

        if val == moment:
            return mid
        elif val > moment:
            right = mid - 1
        else:
            left = mid + 1

    return -1 if right < 0 else right


if __name__ == '__main__':
    i = [(15, 0, 16, 20), (18, 30, 19, 20), (20, 10, 20, 30)]
    m = 1630
    res = find_last_lte(i, m)
    print(res)

    res = contains(i, (16, 30))
    print(res)
