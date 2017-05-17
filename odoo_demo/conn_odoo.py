# -*- encoding: utf-8 -*-
import odoorpc
import ConfigParser
import ssl

config = ConfigParser.ConfigParser()
config.read('./server.conf')


def connect_odoo(section):
    # 获取实例连接参数
    url = config.get(section, 'url')
    port = config.getint(section, 'port')
    db = config.get(section, 'db')
    login = config.get(section, 'login')
    password = config.get(section, 'password')

    # 跟进ssl参数，使用相应协议进行连接
    ssl._create_default_https_context = ssl._create_unverified_context
    protocol = 'jsonrpc+ssl' if config.getboolean(section, 'ssl') else 'jsonrpc'
    # 连接数据库
    odoo = odoorpc.ODOO(url, port=port, protocol=protocol, version='9.0', timeout=10000)
    # 登录远程系统:数据库/用户名/密码
    odoo.login(db, login, password)

    user = odoo.env.user
    print 'Welcome login %s: %s' % (section, user.name)

    return odoo

if __name__ == '__main__':
    # test
    odoo = connect_odoo('localhost')
    tools = odoo.env['function.tool']
    result = tools.odoo_go_live()
    print 'Return: \n%s' % result



