#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@contact: zheng.long@shoufuyou.com
@module: kazoo_demo 
@date: 2019-05-20 
"""
import time
import logging

from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.security import OPEN_ACL_UNSAFE, CREATOR_ALL_ACL

logging.basicConfig()
zk_host = '192.168.1.248:2181'
scheme = 'digest'
credential = '12345678'


def get_zk():
    # create : acl=CREATOR_ALL_ACL
    # zk = KazooClient(hosts=zk_host, auth_data=[(scheme, credential)])
    zk = KazooClient(hosts=zk_host)
    zk.start()
    zk.add_auth(scheme, credential)
    return zk


def test1():
    zk = get_zk()

    while zk.state != KazooState.CONNECTED:
        time.sleep(1)

    root = '/zk'
    child = root + '/child1'

    @zk.ChildrenWatch(root, send_event=True)
    def children_watcher(children, event):
        print(f'{root} children_watcher children :{children}, event: {event}')

    @zk.DataWatch(root)
    def root_data_watcher(value, state, event):
        print(f'{root} root_data_watcher value:{value}, '
              f'version :{state.version if state else None},'
              f'event: {event}')

    @zk.DataWatch(child)
    def child_data_watcher(value, state, event):
        print(f'{child} child_data_watcher value:{value}, '
              f'version :{state.version if state else None},'
              f'event: {event}')

    if not zk.exists(root):
        zk.create(root, b'root value', acl=CREATOR_ALL_ACL)

    if not zk.exists(child):
        zk.create(child, b'child value', acl=CREATOR_ALL_ACL)

    def my_process(event):
        print(f'event: {event}')

    # zk.set(root, f'root new value'.encode())
    # root_children = zk.get_children(root, watch=my_process)
    root_children = zk.get_children(root)
    for rc in root_children:
        c = root + '/' + rc
        if zk.exists(c):
            zk.delete(c)
        else:
            zk.set(root + '/' + c, f'root {c} new value'.encode())

    zk.stop()


def test2():
    zk = get_zk()

    @zk.add_listener
    def my_listener(state):
        if state == KazooState.LOST:
            print("State LOST")
        elif state == KazooState.SUSPENDED:
            print("State SUSPENDED")
        else:
            print("State Connected")

    # Creating Nodes
    # Ensure a path, create if necessary
    zk.ensure_path("/my/favorite")
    # Create a node with data
    zk.create("/my/favorite/node", b"")
    zk.create("/my/favorite/node/a", b"A")
    # Reading Data
    # Determine if a node exists
    if zk.exists("/my/favorite"):
        print("/my/favorite is existed")

    @zk.ChildrenWatch("/my/favorite/node")
    def watch_children(children):
        print("Children are now: %s" % children)

    # Above function called immediately, and from then on
    @zk.DataWatch("/my/favorite/node")
    def watch_node(value, state):
        if state:
            print("state.version: %s, data: %s" % (state.version, value.decode("utf-8")))
        else:
            print('state is null')

    # Print the version of a node and its data
    data, stat = zk.get("/my/favorite/node")
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
    # List the children
    children = zk.get_children("/my/favorite/node")
    print("There are %s children with names %s" % (len(children), children))

    # Updating Data
    zk.set("/my/favorite", b"some data")
    # Deleting Nodes
    zk.delete("/my/favorite/node/a")

    # Transactions
    transaction = zk.transaction()
    transaction.check('/my/favorite/node', version=-1)
    transaction.create('/my/favorite/node/b', b"B")
    results = transaction.commit()
    print("Transaction results is %s" % results)
    # zk.delete("/my/favorite/node/b")
    # zk.delete("/my", recursive=True)
    time.sleep(2)
    zk.stop()


def test3():
    """配合终端，添加修改配置"""
    zk = get_zk()

    while zk.state != KazooState.CONNECTED:
        time.sleep(1)

    root = '/config'
    mysql = root + '/mysql'
    passwd = mysql + '/passwd'

    @zk.ChildrenWatch(mysql, send_event=True)
    def children_watcher(children, event):
        print(f'{root} children_watcher children :{children}, event: {event}')

    @zk.DataWatch(passwd)
    def child_data_watcher(value, state, event):
        print(f'{mysql} child_data_watcher value:{value}, '
              f'version :{state.version if state else None},'
              f'event: {event}')

    zk.ensure_path(root)

    if not zk.exists(mysql):
        zk.create(mysql, b'test1 config', acl=CREATOR_ALL_ACL)

    for _ in range(5):
        if zk.exists(passwd):
            print(zk.get(passwd))
        time.sleep(20)

    zk.stop()


if __name__ == "__main__":
    try:
        test3()
    except Exception as e:
        print("Occurred Exception: %s" % str(e))
        quit()

