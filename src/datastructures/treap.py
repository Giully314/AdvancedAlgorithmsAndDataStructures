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


    def is_root(self) -> bool:
        return self._parent == None

    def is_leaf(self) -> bool:
        return self._left == None and self._right == None



class Treap:
    """
    A treap is a data structure that unites the concept of heap and balanced tree. It keeps keys and priorities.
    """


    def __init__(self, heap_comparator: str = "max"):
        """
        Args:
            heap_comparator: 'max' for a max heap, 'min' for a min heap. 
            Note: if comparator(x, y) is true it means that x has "higher" priority than y, where "higher" means that x is more important
            than y. 
        """

        self._root = None
        self._comparator: Callable[[int, int], bool] = None
        if heap_comparator == "max":
            self._comparator = lambda x, y: x > y
        elif heap_comparator == "min":
            self._comparator = lambda x, y: x < y
        else:
            raise ValueError("The comparator should be 'max' or 'min'.")

    # ******************************* PUBLIC INTERFACE *****************************************

    def insert(self, key: Any, priority: int) -> None:
        """
        Insert a node respecting the BST invariant and then rotate to adjust the heap invariant.
        Running time: O(log(N) base 2).

        Args:
            key: Key to insert. (Should be of the same type of the other keys and should provide a comparator method)
            priority: priority associated to the key.
        """

        node = self._root
        parent = None
        new_node = Node(key, priority)

        #First we go through the whole tree to search the right place of the node based on the key.
        while node != None:
            parent = node
            if node.key <= key:
                node = node.left
            else:
                node = node.right
            
        if parent == None:
            self._root = new_node
            return
        elif key <= parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        #After inserting the node in the right place, we use rotation to restore the heap invariant.
        while new_node.parent != None and self._comparator(new_node.priority, new_node.parent.priority):
            if new_node == new_node.parent.left:
                self.__right_rotate(new_node)
            else:
                self.__left_rotate(new_node)
        
        if new_node.parent == None:
            self._root = new_node
        

    def remove(self, key) -> bool:
        """
        Remove the node with the passed key, if present.
        Running time: O(log(N) base 2).

        Args:
            key: Key of the node.
        Return:
            True if there is a node with key and it is removed, else False.
        """
        
        #First, we search through the treap to find if the there exists a node with the passed key. 
        node = self.search(self._root, key)
        if node == None: #If the node is not present, return false
            return False
        
        if node.is_root() and node.is_leaf(): #If the treap has only one node
            self._root = None
            return True
        
        #Here we push down (in the sense of the heap operation) the node that we want to erase, 
        # until the node become a leaf so we can erase it easily. 
        while not node.is_leaf():
            if node.left != None and (node.right == None or self._comparator(node.left.priority, node.right.priority)):
                self.__right_rotate(node.left)
            else:
                self.__left_rotate(node.right)

            if node.parent.is_root():
                self._root = node.parent

        #Remove the node.
        if node.parent.left == node:
            node.parent.left = None
        else:
            node.parent.right = None
        return True


    def peek(self) -> Any:
        """
        Return (without removing) the key of the node with the highest priority (the root).
        Running time: O(1).
        Return:
            the key of the node.
        """
        if self._root == None:
            raise IndexError("The treap is empty.")
        return self._root.key

    
    def top(self) -> Any:
        """
        Return (by removing the node from the treap) the key of the node with the highest priority (the root).
        Running time: O(log(N) base 2).
        Return:
            the key of the node.
        """
        if self._root == None:
            raise IndexError("The treap is empty.")
            
        key = self._root.key
        self.remove(key)
        return key


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


    def update(self, key, new_priority):
        pass 


    def empty(self) -> bool:
        return self._root == None


    def min(self) -> Any:
        if self._root == None:
            raise IndexError("The treap is empty.")

        node = self._root
        while node.left != None:
            node = node.left
        return node.key


    def max(self) -> Any:
        if self._root == None:
            raise IndexError("The treap is empty.")

        node = self._root
        while node.right != None:
            node = node.right
        return node.key

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
