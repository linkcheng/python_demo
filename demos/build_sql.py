# -*- coding: utf-8 -*-

import xlrd

def read_xl(filename='员工离职申请.xls'):
	try:
		data = xlrd.open_workbook(filename)
	except Exception,e:
		print str(e)

	# table = data.sheets()[0]          #通过索引顺序获取
 
	table = data.sheet_by_index(0)    #通过索引顺序获取

	# table = data.sheet_by_name(u'Sheet1')  #通过名称获取
	
	nrows = table.nrows # 行数

	ncols = table.ncols # 列数

	colnames = table.row_values(0) #某一行数据 

	list =[]
	# 循环行列表数据
	for rownum in range(1,nrows):
		row = table.row_values(rownum)
		if row:
			app = {}
			for i in range(len(colnames)):
				app[colnames[i]] = row[i] 
				list.append(app)
			print app
	return list

if __name__=="__main__":
	read_xl('员工离职申请.xlsx')