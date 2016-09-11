#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random

def get_nums():
	return [random.randint(0, 255) for x in range(0,32)]
	

def show_nums(nums):
	bin_num = []
	for index, num in enumerate(nums):
		b_num = str(bin(num))[2:]
		list_num = ['*'] * 8

		for i, b in enumerate(b_num):
			if b == '1':
				list_num[i] = '.'


		bin_num.append(''.join(list_num))

		# list_bin_num[k] = '.' for k,v in enumerate(bin_num) if v == '1'

		# print('%s %s' % (''.join(list_bin_num),num))

	z = zip(nums, bin_num)

	for i in range(len(z)//2):
		print('%02d %s %s %s %s' % (i, z[i*2][1], z[i*2+1][1], z[i*2][0], z[i*2+1][0]))


if __name__ == '__main__':
	num_list = get_nums()
	show_nums(num_list)