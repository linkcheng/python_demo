# -*- coding: utf-8 -*-
# !/usr/bin/python


def reverse_sentense(src):
    '''
    按照空格分割字符串并且翻转顺序
    :param src:
    :return:
    '''

    des = ''

    src_list = src.split(' ')
    src_list.reverse()

    for item in src_list:
        des = des + item + ' '
    else:
        des = des[:-1]

    return des
