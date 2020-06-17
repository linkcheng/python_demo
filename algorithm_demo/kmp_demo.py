#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: kmp_demo 
@date: 2020-06-17 
"""


class KMP:
    """
    在字符串 p 中找字符串 m
    """
    def __init__(self, p, m):
        self.p = p
        self.m = m

    def search(self):
        next_table = self.build_next_table(self.m)

        p_cur = 0
        p_len = len(self.p)
        m_cur = 0
        m_len = len(self.m)

        while p_cur < p_len:
            if self.p[p_cur] == self.m[m_cur]:
                p_cur += 1
                m_cur += 1
            else:
                if m_cur > 0:
                    # 在 next_table 中的前一个位置
                    m_cur = next_table[m_cur - 1]
                else:
                    p_cur += 1

            if m_cur == m_len:
                # 查找剩余位置是否还有
                print(p_cur-m_cur)
                m_cur = next_table[m_cur - 1]

    def build_next_table(self, string):
        """生成 PMT"""
        next_table = [0, ]

        p_index = 1
        m_index = 0
        str_len = len(string)

        while p_index < str_len:
            if string[p_index] == string[m_index]:
                p_index += 1
                m_index += 1
                next_table.append(m_index)
            else:
                if m_index > 0:
                    m_index = next_table[m_index - 1]
                else:
                    p_index += 1
                    next_table.append(0)

        return next_table


if __name__ == '__main__':
    kmp = KMP('ababcabcdab', 'abc')
    kmp.search()

