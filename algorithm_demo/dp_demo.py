#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: dp_demo 
@date: 2020-06-24 
"""
from typing import List
from functools import wraps


class Node:
    def __init__(self, liveness: int, nexts: List[Node]):
        # 活跃度
        self.liveness = liveness
        # 下级
        self.nexts = nexts


class ReturnData:
    def __init__(self, coming_liveness, not_liveness):
        # 来的情况的最大活跃度
        self.coming_liveness = coming_liveness
        # 不来的时候最大活跃度
        self.not_liveness = not_liveness


class Solution:
    def move(self, size: int, left: str, right: str, mid: str):
        """size 层汉诺塔搬移，从 left 到 right，借助 mid"""
        if size == 1:
            print(f'Move 1 from {left} to {right} ')
            return
        # 把n-1个数移动到mid上
        self.move(size - 1, left, mid, right)
        # 把最后一个移动到right
        print(f'Move {size} from {left} to {right} ')
        # 把mid的n-1个移动到right
        self.move(size - 1, mid, right, left)

    def walk(self, matrix: List[List[int]], i: int, j: int) -> int:
        """求从矩阵 matrix 的（i,j）到达（row, col) 的最小路径和"""
        row = len(matrix) - 1
        col = len(matrix[0]) - 1

        # 到达最后
        if row == i and col == j:
            return matrix[i][j]
        # 到达最后一行
        if row == i:
            return matrix[i][j] + self.walk(matrix, i, j + 1)
        # 到达最右列
        if col == j:
            return matrix[i][j] + self.walk(matrix, i + 1, j)
        # 其他情况，取往右跟往下的最小值
        # 往右走
        right = self.walk(matrix, i, j + 1)
        # 往下走
        down = self.walk(matrix, i + 1, j)
        return matrix[i][j] + min(right, down)

    def is_sum(self, arr: List[int], i: int, acc: int, aim: int) -> bool:
        """从 arr 中能不能任意选择数字，累计和为 aim
        i 表示 arr 中 i 位置的数字，acc 表示在前 i-1 个数字任意累计的和"""
        if i == len(arr):
            return acc == aim

        return self.is_sum(arr, i + 1, acc, aim) or self.is_sum(
            arr, i + 1, acc + arr[i], aim)

    def is_sum_dp(self, arr: List[int], i: int, acc: int, aim: int) -> bool:
        row = len(arr)
        col = sum(arr)

        if col < aim:
            return False

        dp_table = [[False for j in range(col+1)] for i in range(row+1)]
        dp_table[-1][aim] = True
        for row_no in range(row-1, -1, -1):
            for i in range(col-arr[row_no]):
                dp_table[row_no][i] = dp_table[row_no+1][i] or dp_table[row_no+1][i+arr[row_no]]
        return dp_table[0][0]

    def get_max_liveness(self, head: Node) -> int:
        """开年会，计算最大活跃度。领导来，下级一定不来，反之而可能来也可能不来"""
        data = self.process(head)
        return max(data.coming_liveness, data. not_liveness)

    def process(self, head: Node) -> ReturnData:
        """获得head来和不来是最大的活跃度"""
        coming = head.liveness
        not_coming = 0

        for node in head.nexts:
            data = self.process(node)
            coming += data.not_liveness
            not_coming += max(data.coming_liveness, data.not_liveness)

        return ReturnData(coming, not_coming)


def cache(f):
    data = {}

    @wraps(f)
    def wrapper(*args, **kwargs):
        key = args[0] if args else kwargs.get('key')

        if key in data:
            return data[key]
        else:
            res = f(*args, **kwargs)
            data[key] = res
            return res

    return wrapper


if __name__ == '__main__':
    so = Solution()
    so.move(3, "左", "右", "中")
    res = so.walk(
            [[1, 3, 5, 9], [8, 1, 3, 4], [5, 0, 6, 1], [8, 8, 4, 0]], 
            0,
            0
        )

    print(res)
    res = so.is_sum([1, 2, 3], 0, 0, 5)
    print(res)

    res = so.is_sum_dp([1, 2, 3], 0, 0, 5)
    print(res)
