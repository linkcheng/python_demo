# -*- coding: utf-8 -*-

from util import fn_timer


@fn_timer
def compare_str(text, pattern):
    '''
    T=acaabc 和模式 P=aab，暴力解除
    :param text: 被搜索的字符串
    :param pattern: 搜索索引
    :return: 第一次匹配的位置
    '''
    text_len = len(text)
    pattern_len = len(pattern)

    des = 0

    for x in range(10000):  # for test time
        for i in range(text_len - pattern_len):
            for j in range(pattern_len):
                if pattern[j] != text[i+j]:
                    break
            else:
                des = i
                break

    return des + 1


@fn_timer
def compare_str_2(text, pattern):
    '''
    T=acaabc 和模式P=aab
    :param text: 被搜索的字符串
    :param pattern: 搜索索引
    :return: 第一次匹配的位置
    '''
    text_len = len(text)
    pattern_len = len(pattern)
    len_sub_pattern = 0
    des = 0

    for x in range(10000):  # for test time

        for i in range(text_len - pattern_len):
            for j in range(pattern_len):
                if pattern[j] != text[len_sub_pattern+i+j]:
                    sub_pattern = text[len_sub_pattern+i:len_sub_pattern+i+j]
                    break
            else:
                des = len_sub_pattern + i
                break

            len_sub_pattern = compare_sub_pattern(text, sub_pattern, i+len_sub_pattern)

    return des + 1


def compare_sub_pattern(text, sub_p, index):
    '''

    :param text: 原字符串
    :param sub_p: 子匹配模式
    :param index: 已经匹配到的 text 的索引
    :return:
    '''

    len_sub_p = len(sub_p)
    k = 0

    while k < len_sub_p:
        k += 1
        if sub_p[k-1] != text[index+k]:
            k = 0
            index += 1

    return index
