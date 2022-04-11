from dataclasses import dataclass, field
from typing import Callable, Any, Optional
import math
import dheap
from python.datastructures.dheap import DHeap
from functools import reduce

#this class is not for use in a program. It doesn't work. I implemented the methods only to understand what is going on.

@dataclass
class Vertex:
    label: str


@dataclass
class Edge:
    source: Vertex
    dest: Vertex
    weight: float
    label: str 

@dataclass 
class Graph:
    vertices: list[Vertex] = field(default_factory=list)

    #i could use a set instaed of list to improve computation complexity some basic operations  
    adjacency_list: dict[Vertex, list[Edge]] = field(default_factory=dict)


    def add_vertex(self, v: Vertex) -> None:
        #TODO: throw or return if the vertex is already in the graph? 

        self.vertices.append(v)
        self.adjacency_list[v] = []


    def remove_vertex(self, v):
        ...


    def add_edge(self, v: Vertex, u: Vertex, weight: float = 0, label: str = "") -> None:
        #TODO: throw or return if v and u are not in the graph?

        if self.are_adjacent(v, u):
            self.remove_edge(v, u)

        self.adjacency_list[v].append(Edge(v, u, weight, label))


    def are_adjacent(self, v: Vertex, u: Vertex) -> bool:
        if u in self.adjacency_list[v]:
            return True
        return False


    def remove_edge(self, v: Vertex, u: Vertex) -> None:
        for edge in self.adjacency_list[v]:
            if edge.source is v and edge.dest is u:
                break 
        self.adjacency_list[v].remove(edge)


    """
    Running time: O(|V| + |E|)
    """
    def bfs(self, source: Vertex, is_goal: Callable[[Vertex], bool]) -> tuple[Vertex, dict[Vertex, Vertex]]:
        queue = []
        queue.append(source)
        distances = {}
        parents = {}

        #init data
        for v in self.vertices:
            distances[v] = math.inf
            parents[v] = None

        distances[source] = 0

        while len(queue) > 0:
            v = queue.pop()

            if is_goal(v):
                return (v, parents)

            for e in self.adjacency_list[v]:
                u = e.dest

                if distances[u] == math.inf:
                    distances[u] = distances[v] + 1
                    parents[u] = v
                    queue.append(u)
        
        return (None, parents)


    def dfs(self) -> tuple[dict[Vertex, int], dict[Vertex, int]]:
        time = 0

        distances = {}
        parents = {}
        for v in self.vertices:
            distances[v] = math.inf
            parents[v] = None

        for v in self.vertices:
            if in_time[v] is None:
                time, in_time, out_time = self._dfs_helper(v, time, in_time, out_time)
        
        return (in_time, out_time)


    def _dfs_helper(self, v: Vertex, time: int , in_time: dict, out_time: dict) -> tuple[int, dict[Vertex, int], dict[Vertex, int]]:
        time += 1
        in_time[v] = time
        
        for e in self.adjacency_list[v]:
            u = e.dest
            if in_time[u] is None:
                time, in_time, out_time = self._dfs_helper(u, time, in_time, out_time)
        
        time += 1
        out_time[v] = time
        return (time, in_time, out_time)



    def dijkstra(self, source: Vertex, is_goal: Callable[[Vertex], bool]):        
        prio_queue = DHeap(2, "min")
        prio_queue.insert(source, 0)
        # distances = {v : math.inf for v in self.vertices}
        # parents = {v : None for v in self.vertices}
        distances = {}
        parents = {}

        for v in self.vertices:
            distances[v] = math.inf
            parents[v] = None

        distances[source] = 0

        while len(prio_queue) > 0:
            v = prio_queue.top()

            if is_goal(v):
                return (v, parents)
            
            for e in self.adjacency_list[v]:
                u = e.dest
                #relax operation
                if distances[u] > distances[v] + e.weight:
                    distances[u] = distances[v] + e.weight
                    parents[u] = v
                    prio_queue.update(u, distances[u])

        return (None, parents)
    

    """
    a_star is complete (finite number of vertices visited) if the heuristic is: 
    1) admissable (never overestimates the cost to reach the goal), 
    2) consistent (heuristic(u) <= heuristic(v) + distance(v, u)) where v is a generic node and u and adjacent node of v.
    heuristic is a function that estimates the cost to reach the goal from a given vertex.
    distance is a function that measure the distance between 2 adjacent vertices.
    """
    def a_star(self, source: Vertex, is_goal: Callable[[Vertex], bool], distance: Callable, heuristic: Callable):        
        prio_queue = DHeap(2, "min")
        prio_queue.insert(source, 0)
        # distances = {v : math.inf for v in self.vertices}
        # parents = {v : None for v in self.vertices}
        distances = {}
        parents = {}
        f_score = {}

        for v in self.vertices:
            distances[v] = math.inf
            parents[v] = None
            f_score[v] = math.inf


        distances[source] = 0
        f_score[source] = heuristic(source)

        while len(prio_queue) > 0:
            v = prio_queue.top()

            if is_goal(v):
                return (v, parents)
            
            for e in self.adjacency_list[v]:
                u = e.dest
                #relax operation
                if distances[u] > distances[v] + distance(e):
                    distances[u] = distances[v] + distance(e)
                    f_score = distances[u] + heuristic(u)
                    parents[u] = v
                    prio_queue.update(u, f_score[u])

        return (None, parents)

    def components(self) -> Optional["Graph"]:
        ...

    def kurtowsky_planarity(self):
        if len(self.vertices) < 5:
            return True 
        
        if self.violates_euler_constraints():
            return False
        
        if self.is_k5() or self.is_k3_3():
            return False

        for v in self.vertices:
            sub_g = self.remove_vertex(v)
            if not sub_g.kurtowsky_planarity():
                return False

        for v in self.vertices:
            for e in self.adjacency_list[v]:
                sub_b = self.remove_edge(e)
                if not sub_g.kurtowsky_planarity():
                    return False

        return True




    def planarity_testing(self):
        components = self.components()
        for g in components:
            if not g.is_planar(g):
                return False
        return True


    def violates_euler_constraints(self) -> bool:
        n, m = len(self.vertices), reduce(lambda count, l: count + len(l), self.adjacency_list.values(), 0)
        if n < 3:
            return True

        if m <= 3 * n - 6:
            return True
        #there is another condition that should be checked, but it is based on cycles and it's hard to compute
        return False


