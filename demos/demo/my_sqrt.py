# -*- coding: utf-8 -*-
# !/usr/bin/python

import math

from util import fn_timer


@fn_timer
def my_sqrt(x, e=0.0001):
    '''
    牛顿法开方根
    :param x: 需要开放的数字
    :param e: 结果的精度，默认0.0001
    :return:
    '''

    x = float(x)
    guess = 1.0

    guess = 0.5 * (x + x / guess)

    while(abs(x - guess * guess) >= e):
        guess = 0.5 * (guess + x / guess)

    return guess


@fn_timer
def math_sqrt(x):
    return math.sqrt(x)


if __name__ == '__main__':
    print("my_sqrt = %d" % my_sqrt(10))
    print("math_sqrt = %d" % math_sqrt(10))

