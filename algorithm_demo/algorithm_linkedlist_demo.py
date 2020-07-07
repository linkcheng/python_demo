#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link
@module: algorithm_demo
@date: 2019-11-05
"""
from typing import Optional
from collections import namedtuple

DNode = namedtuple('DNode', ('length', 'end'))


class ListNode:
    def __init__(self, data):
        self.val = data
        self.next: ListNode = None

    def __repr__(self):
        return f'ListNode({self.val})'

    __str__ = __repr__


class RandomListNode:
    def __init__(self, data):
        self.val = data
        self.next = None
        self.random = None

    def __hash__(self):
        return hash(self.val)

    def __eq__(self, other):
        return all([self.val == other.val,
                   self.next == other.next,
                   self.random == other.random])


class Solution:

    def get_loop_node(self, head: ListNode) -> Optional[ListNode]:
        """找到链表入环节点，没有返回 None"""
        if not head or not head.next or not head.next.next:
            return

        slow = head.next
        fast = head.next.next

        # 如果有环，快指针一定会追上慢指针
        while fast != slow:
            if not fast.next or not fast.next.next:
                return
            slow = slow.next
            fast = fast.next.next

        # 相遇后，快指针再次从头开始，与慢指针一起一步一次，当再次相遇时，就是入环节点
        fast = head
        while fast != slow:
            fast = fast.next
            slow = slow.next

        return slow

    def test_get_loop_node(self):
        head = ListNode(1)
        head.next = ListNode(2)
        head.next.next = ListNode(3)
        head.next.next.next = ListNode(4)
        head.next.next.next.next = ListNode(5)
        # 制造环
        head.next.next.next.next.next = head.next

        loop = self.get_loop_node(head)

        print(loop)

    def get_cross_node_when_no_loop(self, head1: ListNode, head2: ListNode,
                                    length1: int, length2: int) -> Optional[ListNode]:
        """为两个无环链表找到相交节点，没有返回 None"""
        if not head1 or not head2:
            return

        delta = length1 - length2
        longer = head1 if delta >= 0 else head2
        shorter = head2 if longer == head1 else head1
        delta = abs(delta)

        # longer 链表先走
        for i in range(delta):
            longer = longer.next

        # 再同时走，直到相遇
        while longer != shorter:
            longer = longer.next
            shorter = shorter.next

        return longer

    def test_get_cross_node_when_no_loop(self):
        head1 = ListNode(1)
        head1.next = ListNode(2)
        head1.next.next = ListNode(3)
        head1.next.next.next = ListNode(4)
        head1.next.next.next.next = ListNode(5)
        head1.next.next.next.next.next = ListNode(6)

        head2 = ListNode(11)
        head2.next = ListNode(12)
        head2.next.next = ListNode(13)
        head2.next.next.next = ListNode(14)
        head2.next.next.next.next = ListNode(15)
        head2.next.next.next.next.next = ListNode(16)
        head2.next.next.next.next.next.next = ListNode(17)

        # 构造交叉节点
        head2.next.next.next.next.next.next.next = head1.next

        cur = head1
        length1 = 1
        while cur:
            cur = cur.next
            length1 += 1

        cur = head2
        length2 = 1
        while cur:
            cur = cur.next
            length2 += 1

        node = self.get_cross_node_when_no_loop(head1, head2, length1, length2)
        print(node)

    def get_length_and_end_node(self, head: ListNode, tail: ListNode = None) -> DNode:
        """获取链表从 head 到 tail 的长度以及最后一个非空节点"""
        if not head:
            return DNode(0, head)

        cur = head
        length = 1
        while cur.next != tail:
            length += 1
            cur = cur.next

        if tail:
            length += 1
            cur = cur.next

        return DNode(length, cur)

    def test_get_length_and_end_node(self):
        head = ListNode(1)
        head.next = ListNode(2)
        head.next.next = ListNode(3)
        head.next.next.next = ListNode(4)
        head.next.next.next.next = ListNode(5)
        # 设置尾节点
        tail = head.next.next.next.next.next = ListNode(6)

        dn = self.get_length_and_end_node(head, tail)

        print(f'length={dn.length}, end={dn.end}')

    def no_loop(self, head1: ListNode, head2: ListNode):
        """无环链表相交问题，可能相交也可能不相交"""
        # 先分别拿到它们的长度跟最后一个节点，如果最后一个节点不相同，则不相交
        dnode1 = self.get_length_and_end_node(head1)
        dnode2 = self.get_length_and_end_node(head2)

        # 最后一个节点不相同，则表示不会相交
        if dnode1.end != dnode2.end:
            return

        return self.get_cross_node_when_no_loop(head1, head2, dnode1.length, dnode2.length)

    def test_no_loop(self):
        head1 = ListNode(1)
        head1.next = ListNode(2)
        head1.next.next = ListNode(3)
        head1.next.next.next = ListNode(4)
        head1.next.next.next.next = ListNode(5)

        head2 = ListNode(11)
        head2.next = ListNode(12)
        head2.next.next = ListNode(13)
        head2.next.next.next = ListNode(14)
        head2.next.next.next.next = ListNode(15)

        # 制造交点
        head2.next.next.next.next.next = head1.next.next.next

        node = self.no_loop(head1, head2)
        print(node)

    def is_in_same_loop(self, node1: ListNode, node2: ListNode):
        """判断两个节点是否在同一个环"""
        if not node1 or not node2:
            return False

        cur = node1.next

        while cur and cur != node1:
            if cur == node2:
                return True
            cur = cur.next

        return False

    def both_loop(self, head1: ListNode, head2: ListNode):
        """两个有环链表的相交问题，可能相交也可能不相交
        如果相交，可能交在环上，也可能在环外"""
        node1 = self.get_loop_node(head1)
        node2 = self.get_loop_node(head2)

        # 有相同交点，则表示环外相交
        if node1 == node2:
            dn1 = self.get_length_and_end_node(head1, node1)
            dn2 = self.get_length_and_end_node(head2, node2)
            return self.get_cross_node_when_no_loop(head1, head2, dn1.length, dn2.length)
        else:
            # 如果在同一个环上，返回 node1 与 node2 任意一个节点即可
            if self.is_in_same_loop(node1, node2):
                return node1
            else:
                return

    def test_both_loop(self):
        head1 = ListNode(1)
        head1.next = ListNode(2)
        head1.next.next = ListNode(3)
        head1.next.next.next = ListNode(4)
        head1.next.next.next.next = ListNode(5)
        head1.next.next.next.next.next = ListNode(6)
        head1.next.next.next.next.next.next = head1.next.next

        head2 = ListNode(11)
        head2.next = ListNode(12)
        head2.next.next = ListNode(13)
        head2.next.next.next = ListNode(14)
        head2.next.next.next.next = ListNode(15)
        head2.next.next.next.next.next = ListNode(16)

        # 无环
        # head2.next.next.next.next.next.next = head2.next.next
        # 环外相交
        head2.next.next.next.next.next.next = head1.next.next
        # 环上相交
        # head2.next.next.next.next.next.next = head1.next.next.next

        node = self.both_loop(head1, head2)
        print(node)

    def get_intersect_node(self, head1, head2):
        """返回两个链表的交点，不存在返回 None"""
        node1 = self.get_loop_node(head1)
        node2 = self.get_loop_node(head2)

        # 两个无环链表相交
        if not node1 and not node2:
            return self.no_loop(head1, head2)
        # 两个有环的链表相交
        elif node1 and node2:
            return self.both_loop(head1, head2)
        # 一个链表有环，一个无环
        else:
            return

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

    def clone_by_map(self, head: RandomListNode):
        if not head:
            return

        list_map = {}
        cur = head
        while cur:
            list_map[cur] = RandomListNode(cur.val)
            cur = cur.next
        print(f'list_map length = {len(list_map)}')
        for k, v in list_map.items():
            print(k.val, v.val)
        cur = head
        while cur:
            list_map[cur].next = list_map.get(cur.next)
            list_map[cur].random = list_map.get(cur.random)
            cur = cur.next

        return list_map[head]

    def clone(self, head: RandomListNode):
        """复制复杂链表
        所谓复杂链表就是，除了自己的值以及next指针外，还有一个random指针，指向链表中任意的节点
        """
        if not head:
            return None

        # 在原来链表的每一个节点后都复制一个节点，并保证 next 指向像一个节点
        cur = head
        while cur:
            node = RandomListNode(cur.val)
            node.next = cur.next
            cur.next = node
            cur = cur.next.next

        # 假设 a' = a.next，即表示上一次循环新生成的 node
        # 则 a'.random.val == a.random.next.val
        cur = head
        while cur:
            cur.next.random = cur.random.next
            cur = cur.next.next

        # 断开原来的 node 与新生成 node 之间的链接
        cur = head
        new_head = cur.next
        while cur:
            new_cur = cur.next
            cur.next = new_cur.next
            cur = cur.next

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
        # new_head = self.clone_by_map(head)
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
    # sol.test_get_loop_node()
    # sol.test_get_cross_node_when_no_loop()
    # sol.test_get_length_and_end_node()
    sol.test_no_loop()
    sol.test_both_loop()

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

