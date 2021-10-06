from typing import Any, Iterable

class DisjointSetArray:
    """
    The naive implementation of disjoint set using an array.
    This implementation is the worst, because merging 2 subsets requires O(n).
    """
    def __init__(self, initial_set: Iterable[Any]):
        """
        The init method initialize a partion for every element.

        Running time: O(n) where n is the number of elements in the initial set.
        Args:
            initial_set: an initial set of element for initialize the partions.
        """
        self.partions_map: dict[Any, list[Any]] = {}

        for elem in set(initial_set):
            self.partions_map[elem] = [elem]
        

    def add(self, elem: Any) -> bool:
        """
        Running time: O(1).
        Args:
            elem: the element should be of the same type as the others.
        Return:
            true if the element is inserted, false if the element is already present.
        """

        if elem in self.partions_map:
            return False

        self.partions_map[elem] = [elem]
        return True


    def find_partition(self, elem: Any) -> list[Any]:
        """
        Return the partition of the passed element.
        Running time: O(1).
        Args:
            elem: element to check the partition. If not present, the method raise an exception.
        Return:
            return the partition associated to the element.
        """

        if elem not in self.partions_map:
            raise KeyError("The passed argument is not presented.")
        
        return self.partions_map[elem]


    def are_disjoint(self, elem1: Any, elem2: Any) -> bool:
        """
        Check if the 2 elements are in the same partition.
        Running time: O(N) if the arrays have the same length, O(1) otherwise.
        Args:
            elem1 and elem2 should have the same type.
        Return:
            Return true if the elements are not in the same partion, false otherwise.
        """

        p1 = self.find_partition(elem1)
        p2 = self.find_partition(elem2)
        return p1 != p2

    
    def merge(self, elem1: Any, elem2: Any) -> bool:
        """
        Merge the 2 partions associated with the 2 passed elements.
        Running time: O(n).
        Args:
            elem1 and elem2 are used to retrieve the associated partions.
        Return:
            True if the merge success, false if the 2 partions are equal.
        """

        p1 = self.find_partition(elem1)
        p2 = self.find_partition(elem2)

        if p1 == p2:
            return False
        
        #Check which partion is smaller so we can get better practial performance for the merge.
        if len(p1) < len(p2):
            for elem in p1:
                p2.append(elem)
                self.partions_map[elem] = p2
        else:
             for elem in p2:
                p1.append(elem)
                self.partions_map[elem] = p1
        
        return True


