#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: kmp_demo 
@date: 2020-06-17 
"""


class KMP:
    """
    在字符串 string 中找字符串 pattern
    """
    def __init__(self, string, pattern):
        self.string = string
        self.pattern = pattern

    def search(self):
        next_table = self.build_next_table(self.pattern)

        s_idx = 0
        s_len = len(self.string)
        p_idx = 0
        p_len = len(self.pattern)

        while s_idx < s_len:
            if self.string[s_idx] == self.pattern[p_idx]:
                s_idx += 1
                p_idx += 1
            else:
                if p_idx > 0:
                    # 在 next_table 中的前一个位置
                    p_idx = next_table[p_idx - 1]
                else:
                    s_idx += 1

            if p_idx == p_len:
                # 查找剩余位置是否还有
                print(s_idx-p_idx)
                p_idx = next_table[p_idx - 1]

    def build_next_table(self, string):
        """生成 PMT"""
        next_table = [0, ]

        p_idx = 0
        str_idx = 1
        str_len = len(string)

        while str_idx < str_len:
            if string[str_idx] == string[p_idx]:
                str_idx += 1
                p_idx += 1
                next_table.append(p_idx)
            else:
                if p_idx > 0:
                    p_idx = next_table[p_idx - 1]
                else:
                    str_idx += 1
                    next_table.append(0)
        print(next_table)
        return next_table


if __name__ == '__main__':
    kmp = KMP('ababcabcdabab', 'aba')
    kmp.search()

