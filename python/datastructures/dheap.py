from typing import Any, Callable


#For the moment, i treat every element as a tuple (element, priority). However i think that, because the class manipulate only the 
#priorities, a better implementation could be to divide into 2 arrays the elements and the priorities and work only with the last for 
#the actual move around.
#TODO: run test to examine this theory.
#TODO: think if it's better to raise an exception or return a boolean in: update, remove.

class DHeap:
    """
    A DHeap data structure. The data structure assume that there are no equals priorities (TODO: support equals priorities (SOLVED)).
    This implementation doesn't use auxiliary data structure for speed up search (with an hash table for example); if you need to
    do a lot of search, update priorities or remove elements, this implementation is not good for your case.
    """

    def __init__(self, branching_factor: int = 2, comparator: str = "max", 
                    elements: list[Any]= None, priorities: list[int] = None):
        """
        Args:
        branching_factor: how many childrens has a parent.
        comparator: 'max' for max heap and 'min' for min heap.
        elements(optional): list of elements. Note that elements[i] should correspond to the element associated to the priority priorities[i].
        priorities(optional): list of prioritities. Note that priority[i] should correspond to the prioririty associated to the element elements[i].
        """

        self.d = branching_factor 
        self.comparator: Callable[[int, int], bool] = None
        
        if comparator == "max":
            self.comparator = lambda x, y: x > y
        elif comparator == "min":
            self.comparator = lambda x, y: x < y
        else:
            raise ValueError("The comparator should be 'max' or 'min'.")


        self._pairs: list[tuple[Any, int]] = []

        if elements is not None and priorities is not None:
            self._heapify(elements, priorities)


    # ******************************* PUBLIC INTERFACE *****************************************

    def insert(self, element: Any, priority: int) -> None:
        """
        Insert an element with an associated priority. 
        Running time: O(log(N) in base branching factor).

        Args:
            element: element to insert.
            priority: priority associated.
        """
        
        pair = (element, priority)
        self._pairs.append(pair)
        self.__bubble_up(len(self) - 1)


    def top(self) -> Any:
        """
        Extract the root of the heap (that is the element with the min/max priority).
        Running time: O(log(N) in base branching factor).

        Return:
            the root of the heap if the heap is not empty or raise an expection.
        """

        if self.empty():
            raise IndexError("Empty heap.")
        
        last_leaf = self._pairs.pop()
        if self.empty():
            return last_leaf[0]

        root = self._pairs[0]
        self._pairs[0] = last_leaf
        self.__push_down(0)

        return root[0]


    def remove(self, element: Any) -> None:
        """
        Remove the given element if present. Use this function with caution, because it's slow. (There is a search, possible reallocation
        of the underlying list and a call to function which restores the heap invariants.)
        Running time: O(n).

        Args:
            element: the element to remove.
        """

        idx = self.__find(element)

        if idx == -1:
            raise IndexError("The element is not in the heap.")

        last_leaf = self._pairs.pop()
        _, priority = self._pairs[idx]
        self._pairs[idx] = last_leaf

        
        if self.comparator(priority, last_leaf[1]):
            self.__push_down(idx)
        else:
            self.__bubble_up(idx)


    def peek(self) -> Any:
        """
        Running time: O(1).
        Return:
            Return the element at the root of the heap without extracting it.
        """

        if self.empty():
            raise IndexError("Empty heap.")

        return self._pairs[0][0]


    def contains(self, element: Any) -> bool:
        """
        Running time: O(n).

        Args:
            element: the element to search.
        Return:
            return true if the element is present else false.
        """
        return self.__find(element) >= 0


    def update(self, element: Any, new_priority: int) -> None:
        """
        Update the priority of an element.

        Args:
            element: an object.
            new_priority: the new priority.
        """

        element_idx = self.__find(element)

        if element_idx == -1:
            raise IndexError("The element is not in the heap.")


        old_priority = self._pairs[element_idx][1]
        self._pairs[element_idx] = (element, new_priority)

        if self.comparator(new_priority, old_priority):
            self.__bubble_up(element_idx)
        else:
            self.__push_down(element_idx)



    def empty(self) -> bool:
        return len(self) == 0
    
    def __len__(self):
        return len(self._pairs)

    # ******************************* END OF PUBLIC INTERFACE *****************************************


    def __find(self, element: Any) -> int:
        """
        Find a specific element. 
        Running time: O(n).

        Args:
            element: element to search.
        Return:
            return the position of the element if is present else -1.
        """

        for i, pair in enumerate(self._pairs):
            if pair[0] == element:
                return i
        return -1


    def __get_parent_index(self, children_idx: int) -> int:
        return (children_idx - 1) // self.d 


    def __get_first_children_idx(self, parent_idx: int) -> int:
        return self.d * parent_idx + 1 


    def __get_first_priority_children_idx(self, parent_idx: int) -> int:
        """
        Return:
            The children with the highest/lower priority (depends if the heap is max or min).
            If there are multiple children with the same priority, return the leftmost.
        """
        first_children_idx = self.__get_first_children_idx(parent_idx)
        last_children_idx = min(first_children_idx + self.d, len(self))

        current_priority = self._pairs[first_children_idx][1]
        current_idx = first_children_idx
        for i in range(first_children_idx, last_children_idx):
            if not self.comparator(current_priority, self._pairs[i][1]):
                current_priority = self._pairs[i][1]
                current_idx = i
        
        return current_idx

        
    def __get_first_leaf_idx(self) -> int:
        return (len(self) - 2) // self.d + 1

    
    def __bubble_up(self, idx: int) -> None:
        """
        Fix the problem of a child with higher/lower priority than the parent.
        
        Args:
            idx: index of the node to check.
        """

        current = self._pairs[idx]

        parent_idx = self.__get_parent_index(idx)
        while idx > 0:
            #remember that self._pairs is a list of tuple where tuple[1] is the priority
            if self.comparator(current[1], self._pairs[parent_idx][1]): 
                self._pairs[idx] = self._pairs[parent_idx]
                idx = parent_idx
                parent_idx = self.__get_parent_index(idx)
            else:
                break

        self._pairs[idx] = current

    
    def __push_down(self, idx: int) -> None:
        """
        Fix the problem of a parent with lower/higher priority than a child.
        
        Args:
            idx: index of the node to check.
        """

        current = self._pairs[idx]
        first_leaf_idx = self.__get_first_leaf_idx()
        while idx < first_leaf_idx:
            first_priority_children_idx = self.__get_first_priority_children_idx(idx)
            first_priority_children = self._pairs[first_priority_children_idx]

            if not self.comparator(current[1], first_priority_children[1]):
                self._pairs[idx] = self._pairs[first_priority_children_idx]
                idx = first_priority_children_idx
            else:
                break

        self._pairs[idx] = current

    
    def _heapify(self, elements: list[Any], priorities: list[int]) -> None:
        """
        Construct an heap from a list of elements and priorities.

        Args:
            elements: list of objects.
            priorities: list of priorities associated to the elements.
        """

        assert(len(elements) == len(priorities))

        self._pairs = list(zip(elements, priorities))
        first_leaf_idx = self.__get_first_leaf_idx() - 1
        for i in range(first_leaf_idx, -1, -1):
            self.__push_down(i)
        

    #this function is taken from: 
    # https://github.com/mlarocca/AlgorithmsAndDataStructuresInAction/blob/master/Python/mlarocca/datastructures/heap/dway_heap.py
    def _validate(self) -> bool:
        """Checks that the three invariants for heaps are abided by.
        1.	Every node has at most `D` children. (Guaranteed by construction)
        2.	The heap tree is complete and left-adjusted.(Also guaranteed by construction)
        3.	Every node holds the highest priority in the subtree rooted at that node.
        Returns: True if all the heap invariants are met.
        """
        current_index = 0
        first_leaf = self.__get_first_leaf_idx()
        while current_index < first_leaf:
            current_priority: float = self._pairs[current_index][1]
            first_child = self.__get_first_children_idx(current_index)
            last_child_guard = min(first_child + self.d, len(self))
            for child_index in range(first_child, last_child_guard):
                if current_priority < self._pairs[child_index][1]:
                    return False
            current_index += 1
        return True
    