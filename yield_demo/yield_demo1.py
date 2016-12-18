# -*- coding: utf-8 -*-


def g():
	print('1')
	x = yield 'hello'
	print('2')
	print('x=%s' % x)
	y = 5 + (yield x + 5)
	print('3')
	print('y=%s' % y)

if '__main__' == __name__:
	f = g()
	print(f.next())
	print(f.send(5))
	f.send(2)


