# -*- coding: utf-8 -*-

import psycopg2

def add_field(database, user, password=None, host="127.0.0.1", port="5432"):
	# 数据库连接参数
	conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
	if conn:
		cur = conn.cursor()
		if cur:
			# 动态从 all_form_design 读取 design_model 字段为要扩展字段的数据表名，
			cur.execute("select 'alter table '||design_model||' add state_change_date DATE;'  FROM all_form_design WHERE active=true;")
			sqls = cur.fetchall()

			for sql in sqls:
				print("sql = " + sql[0])
				# cur.execute(sql[0])

			cur.close()
			conn.commit()
		conn.close()


if "__main__" == __name__:
	add_field(database="uat", user="linkcheng",  password=None, host="127.0.0.1", port="5432")