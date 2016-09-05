#!/usr/bin/env python
# coding:utf-8  
# @Author: linkcheng
# function：mydivmod
# 参数x，y的定义域是“整数”，且y不等于0。
# 函数的返回值是一个元组，即：(商, 模)
# 代码中不得使用"/", "//", "%"等运算符及其它模块的帮助

def mydivmod(dividend, divisor):
    if 0 == divisor:
        return 'inf', 0

    if 0 == dividend:
        return 0, 0

    if dividend * divisor > 0:
        tmp = 1
    else:
        tmp = -1

    quotient = tmp

    if dividend * divisor > 0:
        quotient = 1
        while False if abs(quotient) * abs(divisor) > abs(dividend) else True:
            quotient += 1
        quotient -= 1
    else:
        quotient = -1
        while False if abs(quotient) * abs(divisor) > abs(dividend) else True:
            quotient -= 1

    return quotient, dividend - quotient * divisor

if __name__ == "__main__":
    x, y = 8, 3
    print ("mydivmod(%d, %d) = %r" % (0, 9, mydivmod(0, 9)))
    print ("mydivmod(%d, %d) = %r" % (x, y, mydivmod(x, y)))
    print ("mydivmod(%d, %d) = %r" % (-x, y, mydivmod(-x, y)))
    print ("mydivmod(%d, %d) = %r" % (x, -y, mydivmod(x, -y)))
    print ("mydivmod(%d, %d) = %r" % (-x, -y, mydivmod(-x, -y)))
