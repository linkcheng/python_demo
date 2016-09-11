#!/usr/bin/env python
# coding:utf-8  
# @Author: linkcheng
# function：mydivmod
# 参数x，y的定义域是“整数”，且y不等于0。
# 函数的返回值是一个元组，即：(商, 模)
# 代码中不得使用"/", "//", "%"等运算符及其它模块的帮助

def mydivmod(dividend, divisor):
    '''Funtion is the same as divmod'''

    if 0 == divisor:
        return 'INF', 0

    if 0 == dividend:
        return 0, 0

    # By dividend and divisor, set step; if all are greater than zero, step is one, or is minus one.
    if dividend * divisor > 0:
        step = 1
    else:
        step = -1

    quotient = step

    # a // b = c, if want to get c, we can use  b * c = a - t to get c and t.
    while if abs(quotient) * abs(divisor) < abs(dividend):
        quotient += step

    # If step is 1 and remainder is not 0, means quotient is bigger one than needed; 
    if 1 == step and quotient * divisor != dividend:
        quotient -= 1

    return quotient, dividend - quotient * divisor

if __name__ == "__main__":
    x = 8
    print ("mydivmod(%d, %d) = %r" % (0, 9, mydivmod(0, 9)))
    print ("mydivmod(%d, %d) = %r" % (-5, 3, mydivmod(-5, 3)))
    for y in range(1, 10):
        print ("mydivmod(%d, %d) = %r" % (x, y, mydivmod(x, y)))
        print ("mydivmod(%d, %d) = %r" % (-x, y, mydivmod(-x, y)))
        print ("mydivmod(%d, %d) = %r" % (x, -y, mydivmod(x, -y)))
        print ("mydivmod(%d, %d) = %r" % (-x, -y, mydivmod(-x, -y)))
