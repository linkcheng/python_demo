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
    def __init__(self, liveness: int, nexts: List['Node']):
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
        return max(data.coming_liveness, data.not_liveness)

    def process(self, head: Node) -> ReturnData:
        """获得head来和不来时最大的活跃度"""
        coming = head.liveness
        not_coming = 0

        for node in head.nexts:
            data = self.process(node)
            coming += data.not_liveness
            not_coming += max(data.coming_liveness, data.not_liveness)

        return ReturnData(coming, not_coming)

    def sum_aim(self, arr: List[int], aim: int):
        """arr 都是整数，从 arr 选择任意个数，可以累加出 aim 的方法数"""
        if not arr or aim < 0:
            return 0
        return self.sum_aim_process(arr, 0, aim)

    def sum_aim_process(self, arr: List[int], index: int, aim: int):
        """index 表示可以使用 arr 中 >= index的数字"""
        # 最有的时候剩余的目标为 0，表示试一次成功的选择方式
        if index == len(arr):
            return 1 if aim == 0 else 0

        res = 0
        cnt = 0
        while arr[index] * cnt < aim:
            # 当前位置的数字使用次数，最大不能超多 aim
            res += self.sum_aim_process(arr, index+1, aim-arr[index]*cnt)
            cnt += 1
        return res

    def card_inline(self, arr: List[int]):
        """给定一个整型数组arr，代表数值不同的纸牌排成一条线。
        玩家A和玩家B依次拿走每张纸牌，规定玩家A先拿，玩家B后拿，
        但是每个玩家每次只能拿走最左边或者最右边的一张牌，
        最后所拿牌累加和最大的玩家获胜，玩家A和玩家B都绝顶聪明。
        请返回最后获胜者的分数。
        用暴力递归的方法：
        定义递归函数f(i,j),表示如果arr[i...j]这个排列上的纸牌被绝顶聪明的人拿走，最终能够获得什么分数。
        定义递归函数s(i,j),表示如果a[i..j]这个排列上的纸牌被绝顶聪明的人后拿，最终能获得什么分数。
        首先来分析，具体过程如下：
        1.如果i==j(只有一张纸牌)，会被先拿纸牌的人拿走，所以返回arr[i];
        2.如果i!=j,先拿纸牌的人有两种选择，要么拿走arr[i],要么拿走arr[j];
        如果拿走arr[i],剩下arr[i+1,j]。对于arr[i+1,j]的纸牌，当前玩家成了后拿的人，
        因此他后续能获得的分数为s(i+1,j).如果拿走arr[j],那么剩下arr[i,j-1],
        当前玩家后续能获得的分数为s[i,j-1],作为绝顶聪明的人，必然会在两种决策中选择最优的。
        所以返回max{arr[i]+s[i+1,j],arr[j]+s[i][j-1]}
        然后来分析s(i,j):
        1.如果i==j,后拿纸牌的人什么也拿不到，返回0
        2.如果i!=j,玩家的对手会先拿纸牌。对手要么先拿走a[i],要么先拿走arr[j],
        如果对手拿走arr[i],那么排列剩下arr[i+1,j],如果对手拿走arr[j],剩下arr[i,j-1],
        对手也是绝顶聪明的人，所以也会把最差的情况留给玩家因此返回min{f(i+1,j),f(i,j-1)}
        """
        if not arr:
            return 0

    def first_player(self, arr: List[int], i, j):
        """第一位选手，在 arr 的 i~j 范围选择，要么选择第一张 i, 要么选择最后一张 j
        """
        if i == j:
            return arr[i]
        return max(self.second_player(arr, i+1, j), self.second_player(arr, i, j-1))

    def second_player(self, arr: List[int], i, j):
        """第二位选手，在 arr 的 i~j 范围选择，要么选择第一张 i, 要么选择最后一张 j
        """
        if i == j:
            return 0
        return min(self.first_player(arr, i+1, j), self.first_player(arr, i, j-1))


def robot_move(m: int, n: int, k: int):
    """地上有一个m行和n列的方格。
    一个机器人从坐标 0,0 的格子开始移动，每一次只能向左，右，上，下四个方向移动一格，
    但是不能进入行坐标和列坐标的数位之和大于 k 的格子.
    例如:
    当k为18时，机器人能够进入方格（35,37），因为3+5+3+7 = 18。
    但是，它不能进入方格（35,38），因为3+5+3+8 = 19。
    请问该机器人能够达到多少个格子？

    arr: 格子
    m: 行
    n: 列
    k: 边界，不能超过 m1+m2 + n1+n2 <= k

    public int movingCount(int threshold, int rows, int cols) {
        boolean[][] visited = new boolean[rows][cols];
        return countingSteps(threshold, rows, cols, 0, 0, visited);
    }

    public int countingSteps(int limit, int rows, int cols, int r, int c, boolean[][] visited) {
        if (r < 0 || r >= rows || c < 0 || c >= cols
                || visited[r][c] || bitSum(r) + bitSum(c) > limit) return 0;
        visited[r][c] = true;
        return countingSteps(limit, rows, cols, r - 1, c, visited)
                + countingSteps(limit, rows, cols, r, c - 1, visited)
                + countingSteps(limit, rows, cols, r + 1, c, visited)
                + countingSteps(limit, rows, cols, r, c + 1, visited)
                + 1;
    }

    public int bitSum(int t) {
        int count = 0;
        while (t != 0) {
            count += t % 10;
            t /= 10;
        }
        return count;
    }

    """
    # x1 = min(n % 10 + (n // 10) % 10, k+1)
    # x2 = min(m % 10 + (m // 10) % 10, k+1)
    # print(f'x1={x1}, x2={x2}')
    # 其他
    return _robot_move(m, n, k)


def _robot_move(m, n, k):
    if k < 0:
        return 0
    # 只有一个格子
    if k == 0 or (m == 1 and n == 1):
        return 1
    # 只有一行
    if m == 1 and n != 1:
        res = 0
        for i in range(n):
            if bit_sum(i) <= k:
                res += 1
            else:
                break
        return res
    # 只有一列
    if m != 1 and n == 1:
        res = 0
        for i in range(m):
            if bit_sum(i) <= k:
                res += 1
            else:
                break
        return res
    # 其他
    cnt = 0
    for i in range(m):
        if bit_sum(i) > k:
            break
        res = _robot_move(1, n, k-bit_sum(i))
        print(f'{i} 行 {k-bit_sum(i)} 限制， res={res}')
        cnt += res
    return cnt


def bit_sum(n):
    """位数之和
    123 => 1+2+3
    345 => 3+4+5
    """
    res = 0
    while n > 0:
        res += n % 10
        n //= 10
    return res


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

    # res = robot_move(2, 3, 1)
    # print(res)

    # res = robot_move(2, 3, 2)
    # print(res)

    # res = robot_move(2, 3, 3)
    # print(res)

    res = robot_move(38, 15, 9)
    print(res)

    res = robot_move(4, 11, 13)
    print(res)
