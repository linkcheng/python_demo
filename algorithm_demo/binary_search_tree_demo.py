#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: binary_search_tree_demo 
@date: 2020-06-11 
"""
from typing import Optional


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    """
    二叉平衡搜索树，左节点<根节点，右节点>根节点
    """
    def insert(self, root: Node, key):
        """插入数据"""
        if not root:
            return

        if key >= root.data:
            if not root.right:
                root.right = Node(key)
            else:
                self.insert(root.right, key)
        else:
            if not root.left:
                root.left = Node(key)
            else:
                self.insert(root.left, key)

    def find(self, root: Node, key):
        """在以 root 为根节点的树上查找 key"""
        if not root:
            return

        if key > root.data:
            self.find(root.right, key)
        elif key < root.data:
            self.find(root.left, key)
        else:
            return root

    def get_min(self, root: Node) -> Optional[Node]:
        """查找以 root 为根节点的树上的最小节点"""
        if not root:
            return None
        return root if not root.left else self.get_min(root.left)

    def delete(self, root: Node, key) -> Optional[Node]:
        """删除值为 key 的节点，返回新树的头结点"""
        if not root:
            return None
        if root.data > key:
            root.left = self.delete(root.left, key)
        elif root.data < key:
            root.right = self.delete(root.right, key)
        else:
            # 当前节点就是要删除的节点
            # 如果这个节点有两个孩子，则找到跟这个节点大小最接近的位置替换
            # 也就是右孩子的最左节点，也就是右子树上的最小节点
            if root.left and root.right:
                tmp = self.get_min(root.right)
                root.data = tmp.data
                root.right = self.delete(root.right, tmp.data)
            # 最多只有一个孩子的情况
            else:
                root = root.left or root.right

        return root


if __name__ == '__main__':
    pass
