from dataclasses import dataclass

from typing import Any, Optional

@dataclass
class Node:
    """
    A node class for Treap data structure.
    key: an object that can be compared with other objects of the same type.
    priority: a number that describe the priority of the key.
    left, right, parent: objects of class Node. They can also be None.
    """

    _key: Any
    _priority: float
    _parent: Optional["Node"] = None
    _left: Optional["Node"] = None
    _right: Optional["Node"] = None

    
    @property
    def parent(self) -> Optional["Node"]:
        return self._parent
    
    @property
    def left(self) -> Optional["Node"]:
        return self._left

    @property
    def right(self) -> Optional["Node"]:
        return self._right


    @left.setter
    def left(self, node: Optional["Node"]) -> None:
        self._left = node
        if node is not None:
            node.parent = self

    @right.setter
    def right(self, node: Optional["Node"]) -> None:
        self._right = node
        if node is not None:
            node.parent = self

    @parent.setter
    def parent(self, node: Optional["Node"]) -> None:
        self._parent = node


@dataclass
class Treap:
    _root: Node = None

    
    def is_root(self, node: Node) -> bool:
        return node.parent == None


    def _right_rotate(self, x: Node):
        #maybe just return?
        if x == None or self.is_root(x):
            raise Exception("Passed node is null or is root.")

        y = x.parent
        if y.left != x:
            raise Exception("Right rotation can only be applied to a left child.")

        p = y.parent
        if p == None:
            self._root = x
        else:
            if p.left == y:
                p.left = x
            else:
                p.right = x

        y.left = x.right
        x.right = y


    def _left_rotate(self, x: Node):
        #maybe just return?
        if x == None or self.is_root(x):
            raise Exception("Passed node is null or is root.")

        y = x.parent
        if y.right != x:
            raise Exception("Left rotation can only be applied to a right child.")

        p = y.parent
        if p == None:
            self._root = x
        else:
            if p.left == y:
                p.left = x
            else:
                p.right = x

        y.right = x.left
        x.left = y
