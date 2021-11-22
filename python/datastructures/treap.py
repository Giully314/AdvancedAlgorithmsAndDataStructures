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


    def set_left(self, node: Optional["Node"]) -> None:
        self._left = node
        if node is not None:
            node._parent = self

    def set_right(self, node: Optional["Node"]) -> None:
        self._right = node
        if node is not None:
            node._parent = self


    def is_root(self) -> bool:
        return self._parent is None

    def is_leaf(self) -> bool:
        return self._left is None and self._right is None

    
    def __eq__(self, other: Optional["Node"]) -> bool:
        return self.key == other.key and self.priority == other.priority


    def __str__(self, level=0):
        ret = "\t"*level+ f"({self.key} {self.priority})" +"\n"
        for child in [self._left, self._right]:
            if child is None:
                ret += "\n"
                continue
            ret += child.__str__(level+1)
        return ret


class Treap:
    """
    A treap is a data structure that unites the concept of heap and balanced tree. It keeps keys and priorities.
    The invariants of a treap are:
    1) Every left subtree of a node N has key valus less than N.key (for the right subtree is greater).
    2) Given a node N, the priority of N is greater than the subtree rooted at N. 
    3) Each node has at most 2 children.
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
        self.size = 0
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

        node: Node = self._root
        parent: Node = None
        new_node = Node(key, priority)
        self.size += 1

        #First we go through the whole tree to search the right place of the node based on the key.
        while node is not None:
            parent = node
            if key <= node.key:
                node = node._left
            else:
                node = node._right
            
        if parent is None:
            self._root = new_node
            return
        elif key <= parent.key:
            parent.set_left(new_node)
        else:
            parent.set_right(new_node)
           
        #After inserting the node in the right place, we use rotation to restore the heap invariant.
        while new_node._parent is not None and self._comparator(new_node.priority, new_node._parent.priority):
            if new_node is new_node._parent._left:
                new_node = self.__right_rotate(new_node)
            else:
                new_node = self.__left_rotate(new_node)

        if new_node._parent is None:
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
        if node is None: #If the node is not present, return false
            return False
        
        self.size -= 1
        if node.is_root() and node.is_leaf(): #If the treap has only one node
            self._root = None
            return True
        
        #Here we push down (in the sense of the heap operation) the node that we want to erase, 
        # until the node become a leaf so we can erase it easily. 
        while not node.is_leaf():
            if node._left is not None and (node._right is None or self._comparator(node._left.priority, node._right.priority)):
                self.__right_rotate(node._left)
            else:
                self.__left_rotate(node._right)

            if node._parent.is_root():
                self._root = node._parent

        #Remove the node.
        if node._parent._left is node:
            node._parent._left = None
        else:
            node._parent._right = None
        return True


    def peek(self) -> Any:
        """
        Return (without removing) the key of the node with the highest priority (the root).
        Running time: O(1).
        Return:
            the key of the node.
        """
        if self._root is None:
            raise IndexError("The treap is empty.")
        return self._root.key

    
    def top(self) -> Any:
        """
        Return (by removing the node from the treap) the key of the node with the highest priority (the root).
        Running time: O(log(N) base 2).
        Return:
            the key of the node.
        """
        if self._root is None:
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
        
        if node is None:
            return None
        
        if node.key is target_key:
            return node
        elif target_key < node.key:
            return self.search(node._left, target_key)
        else:
            return self.search(node._right, target_key)
        
    
    def contains(self, key: Any) -> bool:
        """
        Check if the treap contains a key.
        Running time: O(log(N) base 2).
        """
        return self.search(self._root, key) is not None


    #TODO: This method is wrong. Solve the issue.
    def update(self, key, new_priority) -> bool:
        """
        Running time: O(log(N) base 2).

        Args:
            key: key associated to the node that we want to update.
            new_priority: new priority to use to update.
        Return:
            True if the node is updated with the new priority, else false.
        """
        node = self.search(self._root, key)
        if node is None:
            return False
        
        old_priority = node.priority

        if old_priority == new_priority:
            return False

        node.priority = new_priority
        
        #We might have violated the priority with respect to the parent (the child has higher priority than the parent).
        if self._comparator(new_priority, old_priority):  
            while node._parent is not None and self._comparator(node.priority, node._parent.priority):
                if node is node._parent._left:
                    node = self.__right_rotate(node)
                else:
                    node = self.__left_rotate(node)
        
            if node._parent is None:
                self._root = node
        else: #one of the child might have higher priority than the updated node.
            while not node.is_leaf():
                if node._left is not None and (node._right is None or self._comparator(node._left.priority, node._right.priority)):
                    node = self.__right_rotate(node._left)
                else:
                    self.__left_rotate(node._right)

                if node._parent.is_root():
                    self._root = node._parent

        return True


    def empty(self) -> bool:
        return self._root is None


    def min(self) -> Any:
        """
        Return the smaller key.
        Running time: O(log(N) base 2).
        """
        if self._root is None:
            raise IndexError("The treap is empty.")

        node = self._root
        while node._left is not None:
            node = node._left
        return node.key


    def max(self) -> Any:
        """
        Return the biggest key.
        Running time: O(log(N) base 2).
        """
        if self._root is None:
            raise IndexError("The treap is empty.")

        node = self._root
        while node._right is not None:
            node = node._right
        return node.key


    def __len__(self):
        return self.size

    # ******************************* END PUBLIC INTERFACE *****************************************
    


    def __right_rotate(self, x: Node) -> Node:
        if x is None or x.is_root():
            raise Exception("Passed node is null or is root.")

        y: Node = x._parent
        if y._left is not x:
            raise Exception("Right rotation can only be applied to a left child.")

        p: Node = y._parent
        if p is None:
            self._root = x
            x._parent = None
        else:
            if p._left is y:
                p.set_left(x)
            else:
                p.set_right(x)

        y.set_left(x._right)
        x.set_right(y)

        return x


    def __left_rotate(self, x: Node) -> Node:
        if x is None or x.is_root():
            raise Exception("Passed node is null or is root.")

        y: Node = x._parent
        if y._right is not x:
            raise Exception("Left rotation can only be applied to a right child.")

        p: Node = y._parent
        if p is None:
            self._root = x
            x._parent = None
        else:
            if p._left is y:
                p.set_left(x)
            else:
                p.set_right(x)

        y.set_right(x._left)
        x.set_left(y)

        return x


    def _validate(self):
        """
        Validate the treap. Check:
        1) the key of the left/right children is less/greater than the parent.
        2) the priority of the parent is higher than the priority of the children.
        """
        def tree_walk(node: Node):
            if node is None:
                return

            if node._left is not None:
                if node.key < node._left.key:
                    print(f"Violation of key invariant node left {node}")
                    return
                if self._comparator(node._left.priority, node.priority):
                    print(f"Violation of priority invariant node left{node}")
                    return
                
                tree_walk(node._left)

            if node._right is not None:
                if node.key > node._right.key:
                    print(f"Violation of key invariant node right {node}")
                    return
                if self._comparator(node._right.priority, node.priority):
                    print(f"Violation of priority invariant node right{node}")
                    return
            
                tree_walk(node._right)


        tree_walk(self._root)
