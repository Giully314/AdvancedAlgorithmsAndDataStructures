from typing import Any, Callable


#For the moment, i treat every element as a tuple (element, priority). However i think that, because the class manipulate only the 
#priorities, a better implementation could be to divide into 2 arrays the elements and the priorities and work only with the last for 
#the actual move around.
#TODO: run test to examine this theory.

class DHeap:
    """
    A DHeap data structure. The data structure assume that there are no equals priorities (TODO: support equals priorities).
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


        self.pairs: list[tuple[Any, int]] = []

        if elements is not None and priorities is not None:
            self.__heapify(elements, priorities)


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
        self.pairs.append(pair)
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
        
        last_leaf = self.pairs.pop()
        if self.empty():
            return last_leaf

        root = self.pairs[0]
        self.pairs[0] = last_leaf
        self.__push_down(0)

        return root[0]


    def remove(self, element: Any) -> None:
        pass 


    def peek(self) -> Any:
        """
        Running time: O(1).
        Return:
            Return the element at the root of the heap without extracting it.
        """

        if self.empty():
            raise IndexError("Empty heap.")

        return self.pairs[0][0]


    def contains(self, element: Any) -> bool:
        pass 

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


        old_priority = self.pairs[element_idx][1]
        self.pairs[element_idx] = (element, new_priority)

        if self.comparator(new_priority, old_priority):
            self.__bubble_up(element_idx)
        elif not self.comparator(new_priority, old_priority):
            self.__push_down(element_idx)



    def empty(self) -> bool:
        return len(self) == 0
    
    def __len__(self):
        return len(self.pairs)

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

        for i, pair in enumerate(self.pairs):
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
        """
        first_children_idx = self.__get_first_children_idx(parent_idx)
        last_children_idx = min(first_children_idx + self.d, len(self))

        current_priority = self.pairs[first_children_idx][1]
        current_idx = first_children_idx
        for i in range(first_children_idx, last_children_idx + 1):
            if not self.comparator(current_priority, self.pairs[i][1]):
                current_priority = self.pairs[i][1]
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

        current = self.elements[idx]

        while parent_idx > 0:
            parent_idx = self.__get_parent_index(idx)

            #remember that self.pairs is a list of tuple where tuple[1] is the priority
            if self.comparator(current[1], self.elements[parent_idx][1]): 
                self.elements[idx] = self.elements[parent_idx]
                idx = self.__get_parent_index(parent_idx)
            else:
                break

        self.elements[idx] = current

    
    def __push_down(self, idx: int) -> None:
        """
        Fix the problem of a parent with lower/higher priority than a child.
        
        Args:
            idx: index of the node to check.
        """

        current = self.elements[idx]
        while idx < self.__get_first_leaf_idx():
            first_priority_children_idx = self.__get_first_priority_children_idx(idx)
            first_priority_children = self.elements[first_priority_children_idx]

            if not self.comparator(current[1], first_priority_children[1]):
                self.elements[idx] = self.elements[first_priority_children_idx]
                idx = first_priority_children
            else:
                break

        self.elements[idx] = current

    
    def __heapify(self, elements: list[Any], priorities: list[int]) -> None:
        """
        Construct an heap from a list of elements and priorities.

        Args:
            elements: list of objects.
            priorities: list of priorities associated to the elements.
        """

        assert(len(elements) == len(priorities))

        self.pairs = list(zip(elements, priorities))
        first_leaf_idx = self.__get_first_leaf_idx() - 1
        for i in range(first_leaf_idx, -1, -1):
            self.__push_down(i)
    