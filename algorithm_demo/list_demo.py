#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class ListNode:
    def __init__(self, val: int):
        self.val = val
        self.next = None


class Solution:
    def __init__(self):
        self.successor = None

    def reverse(self, root: ListNode):
        if not root:
            return root

        size = 1
        cur = root
        while cur.next:
            cur = cur.next
            size += 1

        return self._reverse(root, size)

    def _reverse(self, root: ListNode, size: int):
        """翻转从 root 开始的 size 个节点"""
        if not root.next:
            return root

        # 翻转一个
        if size == 1:
            self.successor = root.next
            return root

        prev = self._reverse(root.next, size-1)
        root.next.next = root
        root.next = self.successor
        return prev


if __name__ == '__main__':
    so = Solution()
    head = ListNode(1)
    so.reverse(head)
