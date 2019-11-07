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

    sol.test_merge(5)
    sol.test_merge(6)
    sol.test_merge(7)
    sol.test_merge(8)
