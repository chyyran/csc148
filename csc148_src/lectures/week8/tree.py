"""Trees

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code for a
general tree implementation.
"""
import random
from typing import Optional, List, Union, Tuple


class Tree:
    """A recursive tree data structure.
    """
    # === Private Attributes ===
    # The item stored at this tree's root,
    # or None if the tree is empty.
    _root: Optional[object]
    # The list of all subtrees of this tree.
    _subtrees: List['Tree']

    # === Representation Invariants ===
    # - If self._root is None
    #   then self._subtrees is an empty list.
    #   This setting of attributes represents
    #   an empty Tree.
    # - self._subtrees may be empty when
    #   self._root is not None.
    #   This setting of attributes represents
    #   a tree consisting of just one node.

    # === Methods ===
    def __init__(self, root: object,
                 subtrees: List['Tree']) -> None:
        """Initialize a new Tree with the given
        root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition:
        - if <root> is None,
          then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return True if this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    # Worked the first time.  Thinking ahead wins again!!
    def height(self) -> int:
        """Return the height of this tree.

        >>> t1 = Tree(None, [])
        >>> t1.height()
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> t2.height()
        2
        >>> t3 = Tree(18, [Tree(55, []), \
                        Tree(3, [Tree(4, []), Tree(1, [])])])
        >>> t3.height()
        3
        """

        if self.is_empty():
            return 0

        return max([n.height() for n in self._subtrees], default=0) + 1

    def __len__(self) -> int:
        """Return the length of this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        >>> t3 = Tree(18, [Tree(55, []), \
                        Tree(3, [Tree(4, []), Tree(1, [])])])
        >>> len(t3)
        5
        """
        if self.is_empty():
            return 0

        return sum([len(n) for n in self._subtrees], 1)


    def count(self, item: object) -> int:
        """Return the length of this tree.

        >>> t1 = Tree(None, [])
        >>> t1.count(3)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> t2.count(3)
        1
        >>> t3 = Tree(18, [Tree(4, []), \
                        Tree(3, [Tree(4, []), Tree(1, [])])])
        >>> t3.count(4)
        2
        """
        return sum([n.count(item) for n in self._subtrees]) \
               + (1 if self._root == item else 0)


if __name__ == '__main__':
    import doctest
    doctest.testmod()