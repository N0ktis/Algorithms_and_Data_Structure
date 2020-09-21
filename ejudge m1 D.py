import fileinput
import sys

sys.setrecursionlimit(10000)


class Graph:
    def __init__(self, type: str, vertex: str, bypass_type: str):
        self.__graph = dict()
        self.__type = type
        self.vertex = vertex
        self.bypass_type = bypass_type

    def add_edge(self, start: str, end, ) -> None:
        self.__graph.setdefault(start, []).append(end)
        self.__graph[start].sort()
        if self.__type == 'u':
            self.__graph.setdefault(end, []).append(start)
            self.__graph[end].sort()

    def breadth_bypass(self, stack=list(), visited=set()) -> None:
        massive = []
        stack.reverse()
        if len(stack) == 0:
            return
        while len(stack) != 0:
            curr_node = stack.pop()
            if curr_node in visited:
                continue
            print(curr_node)
            visited.add(curr_node)
            massive += self.__graph.get(curr_node, '')
        self.breadth_bypass(massive, visited)

    def depth_bypass(self, node: str, visited=set()) -> None:
        print(node)
        visited.add(node)
        for i in self.__graph.get(node, ''):
            if i in visited:
                continue
            self.depth_bypass(i, visited)


def bypass(graph):
    if graph.bypass_type == 'd':
        graph.depth_bypass(graph.vertex)
    elif graph.bypass_type == 'b':
        graph.breadth_bypass([graph.vertex])


def parse_cmd(cmd):
    graph = None
    for line in cmd.input():
        if line == '\n':
            continue
        elif graph is None:
            graph = Graph(*line[:-1].split())
            continue
        graph.add_edge(*line[:-1].split())
    return graph


cmd = fileinput
my_graph = parse_cmd(cmd)
bypass(my_graph)
