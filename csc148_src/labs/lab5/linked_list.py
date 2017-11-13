"""Lab 5: Linked List Exercises

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node.

All of the code from lecture is here, as well as some exercises to work on.
"""
from typing import List, Optional, Callable, TypeVar, Generic

T = TypeVar('T')

class _Node(Generic[T]):
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        The next node in the list, or None if there are
        no more nodes in the list.
    """
    item: T
    next: Optional['_Node[T]']

    def __init__(self, item: T, next: Optional['_Node[T]'] = None) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = next  # Initially pointing to nothing


class LinkedList(Generic[T]):
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    # === Representational Invariants ===
    # - You can not add a node with None as an item.
    _first: Optional[_Node[T]]
    _count: int

    def __init__(self, items: List[T]) -> None:
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.
        """
        if len(items) == 0:  # No items, and an empty list!
            self._first = None
        else:
            self._first = _Node(items[0])
            current_node = self._first
            for item in items[1:]:
                current_node.next = _Node(item)
                current_node = current_node.next
        self._count = len(items)

    # ------------------------------------------------------------------------
    # Non-mutating methods: these methods do not change the list
    # ------------------------------------------------------------------------
    def is_empty(self) -> bool:
        """Return whether this linked list is empty.

        >>> LinkedList([]).is_empty()
        True
        >>> LinkedList([1, 2, 3]).is_empty()
        False
        """
        return self._first is None

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        >>> str(LinkedList([1, 2, 3]))
        '[1 -> 2 -> 3]'
        >>> str(LinkedList([]))
        '[]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    def _get_node(self, index: int) -> _Node[T]:
        curr = self._first
        for _ in range(index):
            curr = curr and curr.next
        return curr

    def __getitem__(self, index: int) -> T:
        """Return the item at position <index> in this list.

        Raise IndexError if <index> is >= the length of this list.

        >>> linky = LinkedList([100, 4, -50, 13])
        >>> linky[0]          # Equivalent to linky.__getitem__(0)
        100
        >>> linky[2]
        -50
        >>> linky[100]
        Traceback (most recent call last):
        IndexError
        """
        curr = self._get_node(index)

        if curr is None:
            raise IndexError
        else:
            return curr.item

    def __setitem__(self, index: int, value: T):
        """
        Inserts an item at a given position index

        === Preconditions ===
        - index <= len(LinkedList)

        >>> linky = LinkedList([])
        >>> linky[0] = 10
        >>> linky[0]
        10
        >>> linky = LinkedList([2])
        >>> linky[0] = 3
        >>> linky[0]
        3
        >>> linky[1] = 4
        >>> linky[1]
        4
        >>> linky = LinkedList([1, 2, 3, 4])
        >>> linky[2] = 5
        >>> linky[2]
        5
        >>> linky[3]
        4
        """
        if value is None:
            raise ValueError
        if index is len(self):
            # We are adding a new item
            if len(self) is 0: # Special case: LinkedList is empty.
                self._first = _Node(value)
            else:
                self._get_node(index - 1).next = _Node(value)
            self._count += 1
        elif index is 0:
            next_node = (self._first or None) and self._first.next
            self._first = _Node(value, next_node)
        else:
            next_node = self._get_node(index).next
            prev_node = self._get_node(index - 1)
            prev_node.next = _Node(value, next_node)

    def add(self, item: T):
        """
        Adds an item to the end of the LinkedList
        >>> linky = LinkedList([])
        >>> linky.add(1)
        >>> linky[0]
        1
        >>> linky.add(2)
        >>> linky[1]
        2
        """
        self[len(self)] = item

    def remove(self, item: T):
        """
        >>> linky = LinkedList([])
        >>> linky.add(1)
        >>> 1 in linky
        True
        >>> linky[0]
        1
        >>> linky.remove(1)
        >>> 1 in linky
        False
        >>> linky.add(1)
        >>> linky.add(2)
        >>> linky.add(3)
        >>> linky.remove(2)
        >>> 2 in linky
        False
        >>> linky[1]
        3
        """
        if item not in self:
            raise ValueError("Can not remove nonexistant item.")

        index = self.index(item)
        if index is 0:
            self._first = self._first.next
        else:
            node = self._get_node(index)
            previous = self._get_node(index - 1)
            previous.next = node.next
        self._count -= 1

    # -------------------------------------------------------------------------
    # Lab Exercises
    # -------------------------------------------------------------------------
    def __len__(self) -> int:
        """Return the number of elements in this list.

        >>> lst = LinkedList([])
        >>> len(lst)              # Equivalent to lst.__len__()
        0
        >>> lst = LinkedList([1, 2, 3])
        >>> len(lst)
        3
        """
        return self._count

        # counter = 0
        # node = self._first
        # while node is not None:
        #    counter += 1
        #    node = node.next
        # return counter

    def __contains__(self, node: object) -> bool:
        """Return whether <item> is in this list.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 3])
        >>> 2 in lst                     # Equivalent to lst.__contains__(2)
        True
        >>> 4 in lst
        False
        """
        inode = self._first
        while inode is not None:
            if inode.item == node:
                return True
            inode = inode.next
        return False

    def count(self, item: object) -> int:
        """Return the number of times <item> occurs in this list.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.count(1)
        3
        >>> lst.count(2)
        2
        >>> lst.count(3)
        1
        """
        node = self._first
        counter = 0
        while node is not None:
            if node.item == item:
                counter += 1
            node = node.next
        return counter

    def index(self, item: object) -> int:
        """Return the index of the first occurrence of <item> in this list.

        Raise ValueError if the <item> is not present.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.index(1)
        0
        >>> lst.index(3)
        3
        >>> lst.index(148)
        Traceback (most recent call last):
        ValueError
        """
        index = -1
        node = self._first
        while node is not None:
            if node.item == item:
                return index + 1
            node = node.next
            index += 1
        raise ValueError


if __name__ == '__main__':
    import python_ta
    python_ta.check_all()
    # import doctest
    # doctest.testmod()