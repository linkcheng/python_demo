#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: tree_demo
@date: 2020-06-09 
"""
from functools import partial

print_non = partial(print, end='')


class Node:
    def __init__(self, val: int):
        self.value = val
        self.left = None
        self.right = None


def morris_in_order_traversal(root: Node) -> None:
    """
    * morris 中序遍历
    * 1. 如果当前节点的左孩子为空，则输出当前节点并将其右孩子作为当前节点。
    * 2. 如果当前节点的左孩子不为空，在当前节点的左子树中找到当前节点在 中序遍历下的前驱节点。
    *    a) 如果前驱节点的右孩子为空，将它的右孩子设置为当前节点。
    *          当前节点更新为当前节点的左孩子。
    *    b) 如果前驱节点的右孩子为当前节点，将它的右孩子重新设为空（恢复树的形状）。
    *          输出当前节点。当前节点更新为当前节点的右孩子。
    * 3. 重复以上1、2直到当前节点为空。
    """
    # 要打印的节点
    cur = root

    while cur:
        if cur.left is None:
            print_non(f'{cur.value} ')
            cur = cur.right
        else:
            # cur 的以中序遍历方式的前驱节点
            prev = cur.left
            while prev.right and prev.right != cur:
                prev = prev.right
            if prev.right is None:
                prev.right = cur
                cur = cur.left
            else:
                print_non(f'{cur.value} ')
                prev.right = None
                cur = cur.right


if __name__ == '__main__':
    head = Node(5)
    head.left = Node(3)
    head.left.left = Node(2)
    head.left.right = Node(4)
    head.left.left.left = Node(1)
    head.right = Node(8)
    head.right.left = Node(7)
    head.right.left.left = Node(6)
    head.right.right = Node(10)
    head.right.right.left = Node(9)
    head.right.right.right = Node(11)

    # morris_in_order_traversal(head)


    class Field:
        def __init__(self):
            print(f'Field __init__')

        def __get__(self, instance, owner):
            print(f'Field __get__ {instance}, {owner}')
            return self.value

        def __set__(self, instance, value):
            print(f'Field __set__ {instance}, {value}')
            self.value = value

        def __del__(self):
            self.value = None
            del self.value

    class NonDataField:
        def __init__(self):
            print(f'Field __init__')

        def __get__(self, instance, owner):
            print(f'Field __get__ {instance}, {owner}')
            return "NonDataField"


    class Model:
        age = Field()
        non_data = NonDataField()

        def __init__(self, name):
            self.name = name
            self.age = 1

        def __getattribute__(self, item):
            print(f'Model __getattribute__ {self} {item}')
            return object.__getattribute__(self, item)

        def __getattr__(self, item):
            print(f'Model __getattr__ {item}')
            return self.age

    obj = Model("hello")
    print(f'\nModel={Model}')
    print(f'obj={obj}\n')
    print(f'Model.__dict__ {Model.__dict__}\n')
    print(f'obj.__dict__ {obj.__dict__}\n')
    print(f'obj.age={obj.age}\n')
    print(f'obj.non_data={obj.non_data}\n')
    print(f'obj.name={obj.name}\n')
    print(f'obj.invalid={obj.invalid}\n')

