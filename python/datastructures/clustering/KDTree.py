from dataclasses import dataclass, field  
from typing import Optional, Union 


def sign(x) -> int:
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0

PointType = tuple[Union[int, float]]


@dataclass(eq=False)
class KDNode:
    point: PointType
    level: int
    right: Optional["KDNode"] = None 
    left: Optional["KDNode"] = None 


    """
    Other could be a KDNode or a tuple representing a point.
    """
    def __eq__(self, other):
        if isinstance(other, KDNode):
            other = other.point

        return self.point == other


@dataclass 
class KDTree:
    dimension: int
    root: KDNode = field(default=None, init=False)


    #Construct a new KDTree from a list of points. The tree is constructed to be balanced.
    def construct_kdtree(self, points: list[PointType]):
        if points is None:
            root = None
            return 

        assert(len(points[0]) == self.dimension)    


    """
    Search the target point in the KDTree.
    Running time: log(n) in base 2 if the tree is balanced.

    Return: the node associated to the target point if present, None otherwise.
    """
    def search(self, target: PointType) -> Optional[KDNode]:
        return self._search(self.root, target)

    """
    Insert a new point in the tree.
    Running time: log(n) in base 2 if the tree is balanced.
    """
    def insert(self, new_point: PointType) -> KDNode:
        return self._insert(self.root, new_point, level=0)


    def remove(self, point: PointType) -> None:
        self._remove(self.root, point)



    """
    Helper method that retrieves the right node key based on the level of the node.
    """
    def _get_node_key(self, node: KDNode) -> Union[int, float]:
        return self._get_point_key(node.point, node.level)


    def _get_point_key(self, point: PointType, level: int) -> Union[int, float]:
        return point[level % self.dimension]


    """
    return -1 for negative values, +1 for positive values. For equal values the value returned is pseudo random to help to keep the 
    tree balanced.
    """
    def _compare(self, point: PointType, node: KDNode) -> int:
        s = sign(self._get_point_key(point, node.level) - self._get_node_key(node))

        if s == 0:
            return -1 if node.level % 2 == 0 else 1
        else:
            return s  


    def _split_distance(self, point: PointType, node: KDNode) -> int:
        return abs(self._get_point_key(point, node.level) - self._get_node_key(node))

    

    def _search(self, subtree_root: KDNode, target: PointType) -> Optional[KDNode]:
        if subtree_root is None:
            return None
        elif subtree_root == target:
            return subtree_root
        elif self._compare(target, subtree_root) < 0:
            return self._search(subtree_root.left, target)
        else:
            return self._search(target, subtree_root.right) 


    def _insert(self, subtree_root: KDNode, new_point: PointType, level: int) -> KDNode:
        if subtree_root is None:
            return KDNode(new_point, level, None, None)
        elif subtree_root == new_point:
            return subtree_root
        elif self._compare(new_point, subtree_root) < 0:
            subtree_root.left = self._insert(subtree_root.left, new_point, level + 1)
            return subtree_root
        else:
            subtree_root.right = self._insert(subtree_root.right, new_point, level + 1)
            return subtree_root


    def _find_min(self, subtree_root: KDNode, coord_idx: int) -> Optional[KDNode]:
        if subtree_root is None:
            return None
        elif subtree_root.level == coord_idx:
            if subtree_root.left is None:
                return subtree_root
            else:
                return self._find_min(subtree_root.left, coord_idx)
        else:
            left_min = self._find_min(subtree_root.left, coord_idx)
            right_min = self._find_min(subtree_root.right, coord_idx)

            values = [x for x in [subtree_root, left_min, right_min] if x is not None]

            return min(values, key = lambda x: x[coord_idx])

    
    def _remove(self, subtree_root: KDNode, point: PointType) -> Optional[KDNode]:
        if subtree_root is None:
            return None 
        
        #if there is a match with the current node there are 3 cases to handle
        elif subtree_root.point == point:
            #the node has a right child
            if subtree_root.right is not None:
                min_node = self._find_min(subtree_root.right, subtree_root.level)
                new_right = self._remove(subtree_root.right, min_node.point)
                return KDNode(min_node.point, subtree_root.level, subtree_root.left, new_right)
            elif subtree_root.left is not None:
                min_node = self._find_min(subtree_root.left, subtree_root.level)
                new_right = self._remove(subtree_root.left, min_node.level)
                return KDNode(min_node.point, subtree_root.level, None, new_right)
            else:
                return None
        
        #if the current node is not a match, check if we need to go in the left or right branch of the tree.
        elif self._compare(point, subtree_root) < 0: 
            subtree_root.left = self._remove(subtree_root.left, point)
            return subtree_root
        else:
            subtree_root.right = self._remove(subtree_root.right, point)
            return subtree_root
