# Data structures for graphs.
# Based on code from here:
#  * https://www.python.org/doc/essays/graphs/
#  * https://www.python-course.eu/graphs_python.php

class Graph():
    def __init__(self, graph=None):
        self._graph = graph

    # Find any isolated nodes.
    def find_isolated(self):
        isolated = []
        for node in self._graph:
            if not self._graph[node]:
                isolated += node
        return isolated

    # Add a (blank) vertex.
    def add_vertex(self, vertex):
        if vertex not in self._graph:
            self._graph[vertex] = []

    # Add an edge between two vertices.
    def add_edge(self, edge):
        # edge could be set, tuple, or list.
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self._graph:
            self._graph[vertex1].append(vertex2)
        else:
            self._graph[vertex1] = [vertex2]

    # Finds the shortest path between two vertices.
    def shortest_path(self, v_start, v_end, path=[]):
        path = path + [v_start]
        if v_start == v_end:
            return path
        if v_start not in self._graph:
            return None

        shortest = None
        for vertex in self._graph[v_start]:
            if vertex not in path:
                newpath = self.shortest_path(vertex, v_end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest


def test_graph():
    return { "a" : ["c"],
             "b" : ["c", "e"],
             "c" : ["a", "b", "d", "e"],
             "d" : ["c"],
             "e" : ["c", "b"],
             "f" : []
            }

if __name__ == '__main__':
    graph = Graph(test_graph())
    print graph.shortest_path('a', 'f')

