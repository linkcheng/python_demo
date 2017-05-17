# -*- encoding: utf-8 -*-

from conn_odoo import connect_odoo


class GoLiveMethod(object):
    """
    常用的外部调用封装。
        install_modules：安装模块列表；
        update_modules： 升级模块列表；
        uninstall_modules： 卸载模块列表；
        execute_sql：执行sql语句，参数return_value：根据sql内容，表示是否需要返回值；
        load_translation： 加载已安装模块的所有系统语言翻译；
        run_function_tool：运行function tool函数记录，参数格式： [(model, method)]
    """
    def __init__(self, section):
        odoo = connect_odoo(section)
        self.section = section
        self.odoo = odoo
        self.tools = odoo.env['function.tool']

    def install_modules(self, install_list):
        # 安装模块
        if isinstance(install_list, list) and install_list:
            result = self.tools.superuser_module_operator('install', install_list)
            print '%s install module result: %s' % (self.section, result)
            return result

    def update_modules(self, update_list):
        # 升级模块，存在'all'（base） 则 update all
        if isinstance(update_list, list) and update_list:
            if 'all' in update_list:
                update_list = ['base']
            result = self.tools.superuser_module_operator('upgrade', update_list)
            print '%s update module result: %s' % (self.section, result)
            return result

    def uninstall_modules(self, uninstall_list):
        # 卸载模块
        if isinstance(uninstall_list, list) and uninstall_list:
            result = self.tools.superuser_module_operator('uninstall', uninstall_list)
            print '%s uninstall module result: %s' % (self.section, result)
            return result

    def execute_sql(self, sql_exp, return_value=False):
        # 执行的sql语句
        if sql_exp:
            result = self.tools.superuser_execute(sql_exp, return_value=return_value)
            print '%s execute sql result: %s' % (self.section, result)
            return result

    def load_files(self, load_files):
        if isinstance(load_files, list) and load_files:
            for load_file in load_files:
                module, filename = load_file.split('/', 1)
                result = self.tools.superuser_load_file(module, filename)
                print '%s load file %s, result: %s' % (self.section, load_file, result)

    def load_translation(self):
        # 加载所有翻译
        result = self.tools.load_translation()
        print '%s load translation result: %s' % (self.section, result)
        return result

    def run_function_tool(self, methods):
        # 运行function tool函数，格式 [(model, method)]
        for model, method in methods:
            result = self.tools.remote_run_function(model, method)
            print '%s run function tool (%s,%s), result: %s' % (self.section, model, method, result)
