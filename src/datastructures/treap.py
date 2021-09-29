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
    parent: Optional["Node"] = None
    left: Optional["Node"] = None
    right: Optional["Node"] = None


    @property.setter
    def left(self, node: Optional["Node"]) -> None:
        self.left = node
        if node is not None:
            node.parent = self

    @property.setter
    def right(self, node: Optional["Node"]) -> None:
        self.right = node
        if node is not None:
            node.parent = self


@dataclass
class Treap:
    root: Node = None

    