"""CSC148 Exercise 5: Tree Practice

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Exercise 5.

NOTE: the hypothesis tests here use some helper functions to create
random instances of the data types we want (trees and binary trees).
We've provided helper functions to do this---you don't need to
understand how they work, but we do encourage you to use them to
write your own hypothesis tests.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

For more information on hypothesis (one of the testing libraries we're using),
please see
<http://www.teach.cs.toronto.edu/~csc148h/fall/software/hypothesis.html>.

Note: this file is for support purposes only, and is not part of your
submission.
"""
import copy
import unittest
from hypothesis import given, assume
from hypothesis.strategies import integers, lists, recursive, builds, just

from btree import BinaryTree


##############################################################################
# Helper functions and custom Hypothesis strategies for generating inputs
##############################################################################
def _binary_tree_size(bt: BinaryTree) -> int:
    """Return the size of the given binary tree.
    """
    if bt.is_empty():
        return 0
    else:
        return 1 + _binary_tree_size(bt._left) + _binary_tree_size(bt._right)

def item():
    """Generate an integer between -10000 and 10000."""
    return integers(min_value=-10000, max_value=10000)


def bt_empty():
    """Generate an empty BinaryTree."""
    return just(BinaryTree(None, None, None))


def binary_trees():
    """Generate a BinaryTree with integer items between -10000 and 10000."""
    return recursive(bt_empty(),
                     lambda s: builds(BinaryTree, root=item(), left=s, right=s))


##############################################################################
# The actual tests
##############################################################################
def test_orders_empty():
    """Test binary tree orderings when given an empty tree."""
    btree = BinaryTree(None, None, None)
    assert btree.preorder() == []
    assert btree.postorder() == []
    assert btree.inorder() == []


@given(binary_trees())
def test_root_position(btree):
    """Test preorder and postorder positioning of the tree root."""
    assume(not btree.is_empty())
    assert btree.preorder()[0] == btree._root
    assert btree.postorder()[-1] == btree._root


@given(binary_trees())
def test_orders_have_correct_length(btree):
    """Test that the binary tree orderings have the correct length."""
    pre_len = len(btree.preorder())
    in_len = len(btree.inorder())
    post_len = len(btree.postorder())
    assert pre_len == _binary_tree_size(btree)
    assert in_len == _binary_tree_size(btree)
    assert post_len == _binary_tree_size(btree)
    print(btree)


if __name__ == '__main__':
    import pytest

    pytest.main()
