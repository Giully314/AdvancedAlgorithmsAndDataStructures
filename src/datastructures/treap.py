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

    key: Any
    priority: float
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
    root: Node = None

