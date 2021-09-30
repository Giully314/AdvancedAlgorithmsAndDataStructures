from dataclasses import dataclass

from typing import Any, Optional, Callable

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


    def is_root(self) -> bool:
        return self._parent == None

    def is_leaf(self) -> bool:
        return self._left == None and self._right == None


@dataclass
class Treap:
    """
    A treap is a data structure that unites the concept of heap and balanced tree. It keeps keys and priorities.
    """
    _comparator: str = "max"

    def __post_init__(self):
        self._root = None
        
        if self._comparator == "max":
            self._comparator = lambda x, y: x > y
        elif self._comparator == "min":
            self._comparator = lambda x, y: x < y
        else:
            raise ValueError("The comparator should be 'max' or 'min'.")

    # ******************************* PUBLIC INTERFACE *****************************************

    def search(self, node: Node, target_key: Any) -> Optional[Node]:
        """
        Search the target key starting from a node.
        Running time: O(log(N) base 2).

        Args:
            node: Node from which to start the search.
            target_key: key of the node.
        Return:
            return the node if the target_key is present, else None.
        """
        
        if node == None:
            return None
        
        if node._key == target_key:
            return node
        elif target_key < node._key:
            return self.search(node.left, target_key)
        else:
            return self.search(node.right, target_key)
        


        
    
    def contains(self, key: Any) -> bool:
        """
        Check if the treap contains a key.
        Running time: O(log(N) base 2).
        """
        return self.search(self._root, key) != None


    def empty(self) -> bool:
        return self._root == None



    # ******************************* END PUBLIC INTERFACE *****************************************
    


    def __right_rotate(self, x: Node):
        #maybe just return?
        if x == None or x.is_root():
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


    def __left_rotate(self, x: Node):
        #maybe just return?
        if x == None or x.is_root():
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
