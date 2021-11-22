from datastructures.treap import Node

n1 = Node("ciao", 1)
n2 = Node("come", 2)
n3 = Node("stai", 3)

n1.left = n2
n1.right = n3

print(n2.parent.key)