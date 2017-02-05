# -*- coding: utf-8 -*-
# !/usr/bin/python


def g():
    x = yield 'hello'

    print('x = %s' % x)

    y = 5 + (yield x + 5)

    print('y = %s' % y)
