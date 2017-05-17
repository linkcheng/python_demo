# -*- encoding: utf-8 -*-
# ===================
# before_ 表示更新代码前，after_ 表示更新代码后
# ===================

# 1、pull code 前需要卸载的模块列表
before_uninstall_modules = []

# ===================
# 2、pull code 后需要安装的模块列表
after_install_modules = []

# 3、pull code 后需要升级的模块列表，'all' 或 'base' 则升级所有已安装模块
after_update_modules = []

# 4、pull code 后需要卸载的模块列表
after_uninstall_modules = []

# 5、pull code 后需要执行的function tools列表 [(model, method)]
# 示例 after_function_tools = [('all.form.design', 'add_can_recall_field'), ('model2', 'method2')]

after_function_tools = []

# 6、pull code 后指定要加载的data文件
# after_load_files = [
#       'hr_base/data/hr_employee_type_data.xml',
# ]
after_load_files = []

# 6、pull code 前执行的sql语句
before_sql = """
--

"""

# 7、pull code 后执行的sql语句
after_sql = """
--

"""


