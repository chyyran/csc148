from typing import Optional, List


class BinaryTree:
    """A class representing a binary tree.

    A binary tree is either empty, or a root connected to
    a *left* binary tree and a *right* binary tree (which could be empty).
    """
    # === Private Attributes ===
    _root: Optional[object]
    _left: Optional['BinaryTree']
    _right: Optional['BinaryTree']

    def __str__(self) -> str:
        return self._str_indent(0)

    def _str_indent(self, depth: int) -> str:
        if self.is_empty():
            return ""
        str_builder: List[str] = []
        str_builder.append(depth * " " + str(self._root))
        str_builder.append(self._left._str_indent(depth+1))
        str_builder.extend(self._right._str_indent(depth+1))
        return '\n'.join(str_builder)

    # === Representation Invariants ===
    # _root, _left, _right are either ALL None, or none of them are None.
    #   If they are all None, this represents an empty BinaryTree.

    def __init__(self, root: Optional[object],
                 left: Optional['BinaryTree'],
                 right: Optional['BinaryTree']) -> None:
        """Initialise a new binary tree with the given values.

        If <root> is None, this represents an empty BinaryTree
        (<left> and <right> are ignored in this case).

        Precondition: if <root> is not None, then neither <left> nor <right>
                      are None.
        """
        if root is None:
            # store an empty BinaryTree
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = left
            self._right = right

    def is_empty(self) -> bool:
        """Return True if this binary tree is empty.

        Note that only empty binary trees can have left and right
        attributes set to None.
        """
        return self._root is None

    def preorder(self) -> list:
        """Return a list of this tree's items using a *preorder* traversal.
        """
        if self.is_empty():
            return []
        base = [self._root]
        base.extend(self._left.preorder())
        base.extend(self._right.preorder())
        return base

    def inorder(self) -> list:
        """Return a list of this tree's items using an *inorder* traversal.
        """
        if self.is_empty():
            return []
        base = []
        base.extend(self._left.inorder())
        base.append(self._root)
        base.extend(self._right.inorder())
        return base

    def postorder(self) -> list:
        """Return a list of this tree's items using a *postorder* traversal.
        """
        if self.is_empty():
            return []
        base = []
        base.extend(self._left.postorder())
        base.extend(self._right.postorder())
        base.append(self._root)
        return base