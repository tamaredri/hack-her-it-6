class Node:
    def __init__(self, value, is_decision_node):
        self.value = value
        self.edges = []
        self.is_decision_node = is_decision_node

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)
