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
        self.left: Node = None
        self.right: Node = None
        self.parent: Node = None

    def __repr__(self):
        return f'Node({self.value})'

    __str__ = __repr__


class Stack:
    def __init__(self, capacity=None):
        self.capacity = capacity
        self.data = []

    def is_empty(self) -> bool:
        return len(self.data) == 0

    def push(self, val: Node) -> None:
        if self.capacity and len(self.data) >= self.capacity:
            raise RuntimeError('The stack is full')
        self.data.append(val)

    def pop(self) -> Node:
        if len(self.data) <= 0:
            raise RuntimeError('The stack is empty')
        return self.data.pop()

    def peek(self) -> Node:
        if len(self.data) > 0:
            return self.data[-1]


class Queue:
    def __init__(self, capacity=None):
        self.capacity = capacity
        self.data = []

    def is_empty(self) -> bool:
        return len(self.data) == 0

    def push(self, val: Node) -> None:
        if self.capacity and len(self.data) >= self.capacity:
            raise RuntimeError('The queue is full')
        self.data.append(val)

    def poll(self) -> Node:
        if len(self.data) <= 0:
            raise RuntimeError('The queue is empty')
        return self.data.pop(0)

    def peek(self) -> Node:
        if len(self.data) > 0:
            return self.data[0]


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
            # 左孩子的最右节点
            prev = cur.left
            while prev.right and prev.right != cur:
                prev = prev.right

            # prev.right is None 表示还没有走过这个节点
            if prev.right is None:
                prev.right = cur
                cur = cur.left
            # prev.right is not None 表示已经走过这个节点，此次是通过这个指针返回
            else:
                print_non(f'{cur.value} ')
                prev.right = None
                cur = cur.right
    print()


def morris_pre_order_traversal(root: Node) -> None:
    """morris 先序遍历"""
    cur = root

    while cur:
        if cur.left is None:
            print_non(f'{cur.value} ')
            cur = cur.right
        else:
            # cur 的以中序遍历方式的前驱节点
            # 左孩子的最右节点
            prev = cur.left
            while prev.right and prev.right != cur:
                prev = prev.right

            # prev.right is None 表示还没有走过这个节点
            if prev.right is None:
                prev.right = cur
                print_non(f'{cur.value} ')
                cur = cur.left
            # prev.right is not None 表示已经走过这个节点，此次是通过这个指针返回
            else:
                prev.right = None
                cur = cur.right
    print()


def pre_order_traversal_rec(root: Node) -> None:
    if not root:
        return
    print_non(f'{root.value} ')
    pre_order_traversal_rec(root.left)
    pre_order_traversal_rec(root.right)


def in_order_traversal_rec(root: Node) -> None:
    if not root:
        return
    in_order_traversal_rec(root.left)
    print_non(f'{root.value} ')
    in_order_traversal_rec(root.right)


def post_order_traversal_rec(root: Node) -> None:
    if not root:
        return
    post_order_traversal_rec(root.left)
    post_order_traversal_rec(root.right)
    print_non(f'{root.value} ')


def level_order_traversal(root: Node) -> None:
    if not root:
        return

    q = Queue()
    q.push(root)

    while not q.is_empty():
        cur = q.poll()
        print_non(f'{cur.value} ')
        if cur.left:
            q.push(cur.left)
        if cur.right:
            q.push(cur.right)

    print()


def pre_order_traversal(root: Node) -> None:
    if not root:
        return

    stack = Stack()
    stack.push(root)

    while not stack.is_empty():
        cur = stack.pop()
        print_non(f'{cur.value} ')

        if cur.right:
            stack.push(cur.right)

        if cur.left:
            stack.push(cur.left)
    print()


def in_order_traversal(root: Node) -> None:
    if not root:
        return

    cur = root
    stack = Stack()

    while not stack.is_empty() or cur:
        if cur:
            stack.push(cur)
            cur = cur.left
        else:
            cur = stack.pop()
            print_non(f'{cur.value} ')
            cur = cur.right
    print()


def post_order_traversal(root: Node) -> None:
    if not root:
        return

    stack = Stack()
    help_stack = Stack()

    stack.push(root)

    while not stack.is_empty():
        cur = stack.pop()
        help_stack.push(cur)

        if cur.left:
            stack.push(cur.left)

        if cur.right:
            stack.push(cur.right)

    while not help_stack.is_empty():
        data = help_stack.pop()
        print_non(f'{data.value} ')

    print()


def get_after_node(node: Node):
    """计算中序遍历的某节点的后继节点"""
    if not node:
        return

    if node.right:
        return get_left_most_node(node.right)

    parent = node.parent
    while parent and parent.left != node:
        node = parent
        parent = node.parent

    return parent


def get_left_most_node(root: Node) -> Node:
    if not root:
        return root
    while root.left:
        root = root.left
    return root


def test_get_after_node():
    root = Node(5)
    root.left = Node(3)
    root.left.parent = root
    root.right = Node(7)
    root.right.parent = root

    root.left.left = Node(2)
    root.left.left.parent = root.left
    root.left.right = Node(4)
    root.left.right.parent = root.left

    node = get_after_node(root)
    print(node)

    node = get_after_node(root.right)
    print(node)


def get_before_node(node: Node):
    """计算前驱节点"""
    if not node:
        return

    if node.left:
        return get_right_most_node(node.left)

    parent = node.parent
    while parent and parent.right != node:
        node = parent
        parent = node.parent
    return parent


def get_right_most_node(node: Node):
    if not node:
        return node

    while node.right:
        node = node.right

    return node


def test_get_before_node():
    root = Node(5)
    root.left = Node(3)
    root.left.parent = root
    root.right = Node(7)
    root.right.parent = root

    root.left.left = Node(2)
    root.left.left.parent = root.left
    root.left.right = Node(4)
    root.left.right.parent = root.left

    root.right.left = Node(6)
    root.right.left.parent = root.right
    
    node = get_before_node(root)
    print(node)

    node = get_before_node(root.right)
    print(node)

    node = get_before_node(root.right.left)
    print(node)


def is_bst(root: Node):
    """是否是搜索树"""
    if not root:
        return

    stack = Stack()
    cur = root
    last = None
    while not stack.is_empty() or cur:
        if cur:
            stack.push(cur)
            cur = cur.left
        else:
            node = stack.pop()
            if last and node.value < last:
                return False
            else:
                last = node.value
            cur = node.right

    return True


class ReturnData:
    def __init__(self, h, is_b):
        self.height = h
        self.is_balance = is_b


def is_balance_tree(root: Node) -> bool:
    """是否是平衡树"""
    return process(root).is_balance


def process(root: Node) -> ReturnData:
    if not root:
        return ReturnData(0, True)

    left = process(root.left)
    if not left.is_balance:
        return ReturnData(0, False)

    right = process(root.right)
    if not right.is_balance:
        return ReturnData(0, False)

    if abs(left.height - right.height) > 1:
        return ReturnData(0, False)

    return ReturnData(max(left.height, right.height)+1, True)


def is_complet_tree(root: Node):
    """是否是完全二叉树"""
    if not root:
        return True

    is_leaf = False
    q = []
    q.append(root)

    while len(q) > 0:
        node = q.pop(0)
        # 如果有右孩子没有左孩子，一定不是
        if not node.left and node.right:
            return False
        # 开启叶子节点判断，如果有叶子节点，则一定不是
        if is_leaf and (node.left or node.right):
            return False

        if node.left:
            q.append(node.left)
        # 如果没有右孩子，则进入叶子节点判断时期
        if node.right:
            q.append(node.right)
        else:
            is_leaf = True

    return True


def count_complete_tree_node(root: Node) -> int:
    """计算完全二叉树的节点个数"""
    if not root:
        return 0

    max_height = get_height(root)
    right_height = get_height(root.right)

    # 如果高度差=1，说明左树是满的
    if max_height - right_height == 1:
        left = 1 << (max_height - 1)
        right = count_complete_tree_node(root.right)
    # 反之说明，右树是满的，只是高度差=2
    else:
        left = count_complete_tree_node(root.left)
        right = 1 << (max_height - 2)

    return left + right


def get_height(root: Node) -> int:
    if not root:
        return 0

    height = 0

    while root:
        height += 1
        root = root.left

    return height


def test_count_complete_tree_node():
    root = Node(1)
    print(f'count={count_complete_tree_node(root)}')
    root.left = Node(2)
    print(count_complete_tree_node(root))
    root.right = Node(3)
    print(count_complete_tree_node(root))

    root.left.left = Node(4)
    print(count_complete_tree_node(root))
    root.left.right = Node(5)
    print(count_complete_tree_node(root))

    root.right.left = Node(6)
    print(count_complete_tree_node(root))
    root.right.right = Node(7)
    print(count_complete_tree_node(root))

    root.left.left.left = Node(8)
    print(count_complete_tree_node(root))


def trie_tree():
    """前缀树"""


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

    print('morris')
    morris_pre_order_traversal(head)
    morris_in_order_traversal(head)

    print('rec')
    pre_order_traversal_rec(head)
    print()
    in_order_traversal_rec(head)
    print()
    post_order_traversal_rec(head)
    print()

    print('non-rec')
    pre_order_traversal(head)
    in_order_traversal(head)
    post_order_traversal(head)

    level_order_traversal(head)

    test_get_before_node()

    test_count_complete_tree_node()


def fib(n):
    if n in {1, 2}:
        return 1
    a = b = 1
    while n > 2:
        a, b = b, a+b
        n -= 1

    return b
