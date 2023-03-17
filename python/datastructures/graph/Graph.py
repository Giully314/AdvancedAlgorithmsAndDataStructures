from dataclasses import dataclass, field
from typing import Any, Optional, Callable
from collections import deque
from graphviz import Digraph
from dheap import DHeap

# This file implements a SIMPLE graph, used only for education purpose.


@dataclass(frozen=True)
class Node:
    value: Any
    label: str


@dataclass(frozen=True)
class Edge:
    source: Node
    dest: Node
    value: int
    label: str


@dataclass
class Graph:
    nodes: list[Node] = field(default_factory=list)
    edges: dict[Node, list[Edge]] = field(default_factory=dict)


    def add_node(self, value: Any, label: str ="") -> Node:
        if value in self:
            return 

        node = Node(value, label)
        self.nodes.append(node)
        self.edges[node] = []
        return node


    def add_edge(self, source_node: Node, dest_node: Node, value: int = 1, label= ""):
        if source_node not in self and dest_node not in self:
            return
        
        edge = Edge(source_node, dest_node, value, label)
        self.edges[source_node].append(edge)


    def bfs(self, start_node: Node, goal_func: Callable[[Node], bool] = None) -> tuple[Optional[Node], dict[Node, Optional[Node]]]:
        queue: deque[Node] = deque()
        queue.append(start_node)
        distances: dict[Node, float] = dict()
        parents: dict[Node, Optional[Node]] = dict()

        for node in self.nodes:
            distances[node] = float("inf")
            parents[node] = None
        distances[start_node] = 0
        
        while queue:
            u = queue.popleft()
            if goal_func is not None and goal_func(u):
                return (u, parents)
            
            for e in self.edges[u]:
                v = e.dest
                if distances[v] == float("inf"):
                    distances[v] = distances[u] + 1
                    parents[v] = u
                    queue.append(v)

        return (None, parents)
    

    def dfs(self, start_node: Node) -> tuple[int]:
        stack: list[Node] = []
        stack.append(start_node)
        in_time: dict[Node, float] = {}
        out_time: dict[Node, float] = {}
        time = 0
        for node in self.nodes:
            in_time[node] = None
            out_time[node] = None
    
        while stack:
            time += 1
            u = stack.pop()
            for e in self.edges[u]:
                v = e.dest
                if in_time[v] == None:
                    in_time[v] = time
                    stack.append(v)
            time += 1
            out_time[u] = time
        return (in_time, out_time) 


    def dijkstra(self, start_node: Node, 
                 goal_func: Callable[[Node], bool] = None) -> tuple[Optional[Node], dict[Node, Optional[Node]]]:
        queue = DHeap(comparator="min")
        distances: dict[Node, float] = dict()
        parents: dict[Node, Optional[Node]] = dict()
        for node in self.nodes:
            distances[node] = float("inf")
            parents[node] = None
            queue.insert(node, float("inf"))
        queue.update(start_node, 0)
        distances[start_node] = 0

        while queue:
            u = queue.top()
            if goal_func is not None and goal_func(u):
                return (u, parents)
            
            for e in self.edges[u]:
                v = e.dest
                if distances[v] > distances[u] + e.value:
                    distances[v] = distances[u] + e.value 
                    parents[v] = u
                    queue.update(v, distances[v])

        return (None, parents)


    def a_star(self, start_node: Node, 
                 goal_func: Callable[[Node], bool],
                 distance: Callable[[Edge], float],
                 heuristic: Callable[[Node], float]) -> tuple[Optional[Node], dict[Node, Optional[Node]]]:
        queue = DHeap(comparator="min")
        distances: dict[Node, float] = {}
        parents: dict[Node, Optional[Node]] = {}
        fscore: dict[Node, float] = {} # sum of distance and heuristic, used as priority in the queue
        for node in self.nodes:
            distances[node] = float("inf")
            parents[node] = None
            fscore[node] = float("inf")
            queue.insert(node, float("inf"))
        queue.update(start_node, 0)
        distances[start_node] = 0
        fscore[start_node] = heuristic(start_node)

        while queue:
            u = queue.top()
            if goal_func is not None and goal_func(u):
                return (u, parents)
            
            for e in self.edges[u]:
                v = e.dest
                dist_e = distance(e)
                if distances[v] > distances[u] + dist_e:
                    distances[v] = distances[u] + dist_e
                    parents[v] = u
                    fscore[v] = distances[v] + heuristic(v)
                    queue.update(v, fscore[v])

        return (None, parents)


    def get_node(self, value: Any) -> Optional[Node]:
        for node in self.nodes:
            if node.value == value:
                return node
        return None

    def __contains__(self, value: Any) -> bool:
        for node in self.nodes:
            if node.value == value:
                return True
        return False
    
    def printable_repr(self) -> tuple[set[Node], set[tuple[Node, Node]]]:
        nodes: set[Node] = set()
        edges: set[tuple[Node, Node]] = set()
        for node in self.nodes:
            nodes.add(node)
            for e in self.edges[node]:
                edges.add((e.source, e.dest))

        return nodes, edges
    

def show(graph: Graph, format='svg', rankdir='LR'):
    """
    format: png | svg | ...
    rankdir: TB (top to bottom graph) | LR (left to right)
    """
    assert rankdir in ['LR', 'TB']
    nodes, edges = graph.printable_repr()
    dot = Digraph(format=format, graph_attr={'rankdir': rankdir}) 
    
    for n in nodes:
        dot.node(name=str(id(n)), label = f"{n.label} | {n.value}", shape='record')
        
    for n1, n2 in edges:
        dot.edge(str(id(n1)), str(id(n2)))
    
    return dot