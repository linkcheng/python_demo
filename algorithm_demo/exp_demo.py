#!/usr/bin/env python3
# -*- coding: UTF-8 -*
"""
给你一个字符串 s 和一个字符规律 p，请你来实现一个支持 '.' 和 '*' 的正则表达式匹配。
'.' 匹配任意单个字符
'*' 匹配零个或多个前面的那一个元素
所谓匹配，是要涵盖 整个 字符串 s的，而不是部分字符串。
说明:

s 可能为空，且只包含从 a-z 的小写字母。
p 可能为空，且只包含从 a-z 的小写字母，以及字符 . 和 *。
"""


class Solution:
    def is_match(self, s: str, p: str) -> bool:
        # 特殊值处理
        if not p:
            return not s
        if len(p) == 1 and not s:
            return False

        m, n = len(s)+1, len(p)+1
        dp = [[False]*n for _ in range(m)]

        # base case
        dp[0][0] = True
        dp[0][1] = False
        # for i in range(1, m):
        #     dp[i][0] = False
        for i in range(2, n):
            if p[i-1] == '*':
                dp[0][i] = dp[0][i-2]

        # other
        # dp[i][j] 表示的状态是 s 的前 i 项和 p 的前 j 项是否匹配。
        for i in range(1, m):
            for j in range(1, n):
                if p[j-1] in {s[i-1], '.'}:
                    dp[i][j] = dp[i-1][j-1]
                elif p[j-1] == '*':
                    # 如果 p 最后一位是 *
                    if p[j-2] in {s[i-1], '.'}:
                        # 如果 * 星号前一个值 == s 当前值或者 .  重复 0 次或者重复 1 次
                        dp[i][j] = dp[i][j-2] or dp[i-1][j]
                    else:
                        # 如果 * 星号前一个值 ！= s 当前值或者 .  只能重复 0 次
                        dp[i][j] = dp[i][j-2]
                else:
                    dp[i][j] = False

        return dp[m-1][n-1]

    def is_match_rec(self, s: str, p: str) -> bool:
        if not p:
            return not s
        if len(p) == 1 and not s:
            return False
        return self._is_match(s, p, len(s), len(p), 0, 0)

    def _is_match(self, s: str, p: str, s_len: int, p_len: int, s_i: int, p_i: int) -> bool:
        if p_i >= p_len:
            return s_i == s_len

        if s_i >= s_len:
            return s_i == p_len

        # 如果当前长度最后一位是 *，则有两种情况
        # 1. 重复前值 0 次
        # 2. 重复前值 1 次
        match = s_i < s_len and p[p_i] in {s[s_i], '.'}
        if (p_i+1) < p_len and p[p_i+1] == '*':
            return (
                self._is_match(s, p, s_len, p_len, s_i, p_i+2)
                or
                (match and self._is_match(s, p, s_len, p_len, s_i+1, p_i))
            )
        else:
            return match and self._is_match(s, p, s_len, p_len, s_i+1, p_i+1)


class Solution1:
    def isMatch(self, s: str, p: str) -> bool:
        if not s:
            return p in {'', '*', '?'}
        
        if not p:
            return False

        return self._isMatch(s, p, len(s), len(p), 0, 0)
    
    def _isMatch(self, s, p, s_len, p_len, i, j) -> bool:
        if i == s_len:
            return j == p_len
        
        # if j == p_len:
        #     return i == s_len

        if p[j] in {s[i], '?'}:
            return self._isMatch(s, p, s_len, p_len, i+1, j+1)
        elif p[j] == '*':
            return (
                # 重复 0 次
                self._isMatch(s, p, s_len, p_len, i, j+1)
                or 
                # 重复 1 次
                self._isMatch(s, p, s_len, p_len, i+1, j)
            )
        else:
            return False


if __name__ == '__main__':
    # so = Solution()
    # res = so.is_match_rec("aa", "a*")
    # res = so.is_match_rec("mississippi", "mis*is*p*.")
    # print(res)
    # res = so.is_match("mississippi", "mis*is*p*.")
    # print(res)

    # res = so.is_match_rec("aab", "c*a*b")
    # print(res)
    # res = so.is_match("aab", "c*a*b")
    # print(res)

    so1 = Solution1()
    res = so1.isMatch("adceb", "*a*b")
    print(res)
