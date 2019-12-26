#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: algorithm_demo
@date: 2019-11-05
"""
import time
import random


class ListNode:
    def __init__(self, data):
        self.val = data
        self.next = None


class RandomListNode:
    def __init__(self, data):
        self.val = data
        self.next = None
        self.random = None


class Solution:

    def find_kth_to_tail(self, head, k):
        """
        从单链表的尾部找倒数第 k 个节点的值, k > 0

        初始化两个指针，使他们间距为 k 个节点，然后遍历链表，
        当前边的链表走到尾的时候，后边的指针就是在倒数第 k 个节点的位置
        """
        first_ptr = second_ptr = head
        for i in range(k):
            if not first_ptr:
                return None
            first_ptr = first_ptr.next

        while first_ptr:
            first_ptr = first_ptr.next
            second_ptr = second_ptr.next

        return second_ptr

    def test_find_kth_to_tail(self, k):
        head = ListNode(0)
        ptr = head
        for i in range(1, 10):
            node = ListNode(i)
            ptr.next = node
            ptr = node

        ret = self.find_kth_to_tail(head, k)
        print(ret.val if ret else ret)

    def reverse_linked_list(self, head):
        """翻转列表
        从第二个 node 开始，循环将 next 指向前一个
        需要一直有一个指针指向还没有翻转的链表的头部
        也需要一个指针指向已经翻转的新链表的头部
        """
        ptr = head
        next_ptr = head.next
        while next_ptr:
            tmp_ptr = next_ptr
            next_ptr = next_ptr.next
            tmp_ptr.next = ptr
            ptr = tmp_ptr

        head.next = None
        return ptr

    def test_reverse_linked_list(self, length):
        head = ListNode(0)
        ptr = head
        for i in range(1, length):
            node = ListNode(i)
            ptr.next = node
            ptr = node

        ptr = head
        while ptr:
            print(ptr.val)
            ptr = ptr.next
        print('====')
        new_head = self.reverse_linked_list(head)
        ptr = new_head
        while ptr:
            print(ptr.val)
            ptr = ptr.next
        print('====')

    def merge(self, head1, head2):
        """两个单调递增链表，合并后仍是单调递增的
        """
        if not head1:
            return head2

        if not head2:
            return head1

        if head1.val <= head2.val:
            new_head = head1
            ptr1 = head1.next
            ptr2 = head2
        else:
            new_head = head2
            ptr1 = head1
            ptr2 = head2.next

        new_ptr = new_head

        while ptr1 and ptr2:
            if ptr1.val <= ptr2.val:
                new_ptr.next = ptr1
                new_ptr = ptr1
                ptr1 = ptr1.next
            else:
                new_ptr.next = ptr2
                new_ptr = ptr2
                ptr2 = ptr2.next

        if ptr1:
            new_ptr.next = ptr1
        elif ptr2:
            new_ptr.next = ptr2

        return new_head

    def test_merge(self, length):
        head1 = ListNode(0)
        ptr = head1
        for i in range(2, length, 2):
            node = ListNode(i)
            ptr.next = node
            ptr = node

        ptr = head1
        while ptr:
            print(ptr.val)
            ptr = ptr.next
        print('====')

        head2 = ListNode(1)
        ptr = head2
        for i in range(3, length, 2):
            node = ListNode(i)
            ptr.next = node
            ptr = node

        ptr = head2
        while ptr:
            print(ptr.val)
            ptr = ptr.next
        print('====')

        new_head = self.merge(head1, head2)
        ptr = new_head
        while ptr:
            print(ptr.val)
            ptr = ptr.next
        print('####')

    def clone(self, head):
        """复制复杂链表
        所谓复杂链表就是，除了自己的值以及next指针外，还有一个random指针，指向链表中任意的节点
        """
        if not head:
            return None

        # 在原来链表的每一个节点后都复制一个节点，并保证 next 指向像一个节点
        ptr = head
        while ptr:
            new_node = RandomListNode(ptr.val)
            new_node.next = ptr.next
            ptr.next = new_node
            ptr = ptr.next.next

        # 假设 a' = a.next，即表示上一次循环新生成的 node
        # 则 a'.random.val == a.random.next.val
        ptr = head
        while ptr:
            ptr.next.random = ptr.random.next
            ptr = ptr.next.next

        # 断开原来的 node 与新生成 node 之间的链接
        ptr = head
        new_head = ptr.next
        new_ptr = new_head

        ptr.next = new_ptr.next
        ptr = ptr.next
        while ptr:
            ptr.next = ptr.next.next
            new_ptr.next = new_ptr.next.next
            ptr = ptr.next

        return new_head

    def test_clone(self, length):
        head = RandomListNode(1)
        ptr = head
        for i in range(2, length):
            ptr.next = RandomListNode(i)
            ptr = ptr.next

        ptr = head
        for i in range(1, length-2):
            ptr.random = ptr.next.next
            ptr = ptr.next
        ptr.random = head
        ptr.next.random = head.next

        ptr = head
        for i in range(length-1):
            print(ptr.val)
            print(ptr.random.val)
            print('======')
            ptr = ptr.next
        print('#####')
        new_head = self.clone(head)

        ptr = head
        new_ptr = new_head
        for i in range(length-1):
            print(ptr.val)
            print(new_ptr.val)
            print(ptr.random.val)
            print(new_ptr.random.val)
            print('======')
            ptr = ptr.next
            new_ptr = new_ptr.next

    def find_first_common_node(self, head1, head2):
        """寻找两个链表的相交节点"""
        ptr1 = head1
        ptr2 = head2

        # 先确定两个链表的长度差 k，与 find_kth_to_tail 类似
        while ptr1 and ptr2:
            # 特殊处理相交前相等的情况
            if ptr1 == ptr2:
                return ptr1
            ptr1 = ptr1.next
            ptr2 = ptr2.next

        tmp_ptr = ptr1 if ptr1 else ptr2
        k = 0
        while tmp_ptr:
            k += 1
            tmp_ptr = tmp_ptr.next

        # 让长的链表的从第 k 个节点开始与短链表一一比较，知道遇到相等的为止
        ptr1 = head1
        ptr2 = head2
        if ptr1:
            for i in range(k):
                ptr1 = ptr1.next
        else:
            for i in range(k):
                ptr2 = ptr2.next

        while ptr1 != ptr2:
            ptr1 = ptr1.next
            ptr2 = ptr2.next

        return ptr1

    def test_find_first_common_node(self, common_val):
        common_head = ListNode(common_val)
        ptr = common_head
        for i in range(1, 3):
            node = ListNode(common_val+i)
            ptr.next = node
            ptr = node

        ptr = common_head
        while ptr:
            print(ptr.val)
            ptr = ptr.next
        print('====')

        head1 = ListNode(1)
        ptr = head1
        for i in range(2, common_val):
            node = ListNode(i)
            ptr.next = node
            ptr = node
        ptr.next = common_head

        ptr = head1
        while ptr:
            print(ptr.val)
            ptr = ptr.next
        print('====')

        head2 = ListNode(3)
        ptr = head2
        for i in range(4, common_val):
            node = ListNode(i)
            ptr.next = node
            ptr = node
        ptr.next = common_head

        ptr = head2
        while ptr:
            print(ptr.val)
            ptr = ptr.next
        print('====')

        ret = self.find_first_common_node(head1, head2)

        print(ret.val if ret else ret)
        print('####')


if __name__ == '__main__':
    sol = Solution()

    # sol.test_find_kth_to_tail(1)
    # sol.test_find_kth_to_tail(2)
    # sol.test_find_kth_to_tail(3)
    # sol.test_find_kth_to_tail(4)
    # sol.test_find_kth_to_tail(5)
    # sol.test_find_kth_to_tail(6)
    # sol.test_find_kth_to_tail(7)
    # sol.test_find_kth_to_tail(8)
    # sol.test_find_kth_to_tail(9)
    # sol.test_find_kth_to_tail(10)
    # sol.test_find_kth_to_tail(11)
    # sol.test_find_kth_to_tail(12)

    # sol.test_reverse_linked_list(0)
    # sol.test_reverse_linked_list(1)
    # sol.test_reverse_linked_list(2)
    # sol.test_reverse_linked_list(3)
    # sol.test_reverse_linked_list(4)
    # sol.test_reverse_linked_list(5)

    # sol.test_merge(5)
    # sol.test_merge(6)
    # sol.test_merge(7)
    # sol.test_merge(8)

    # sol.test_clone(5)

    # sol.test_find_first_common_node(4)
    # sol.test_find_first_common_node(5)
    # sol.test_find_first_common_node(6)
    # sol.test_find_first_common_node(7)


import tushare

