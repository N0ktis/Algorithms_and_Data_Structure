import fileinput
import sys

sys.setrecursionlimit(10000)


class Graph:
    def __init__(self, type: str, vertex: str, bypass_type: str):
        self.__graph = dict()
        self.__type = type
        self.vertex = vertex
        self.bypass_type = bypass_type

    def add_edge(self, start: str, end: str) -> None:
        self.__graph.setdefault(start, []).append(end)
        if self.__type == 'u':
            self.__graph.setdefault(end, []).append(start)

    def breadth_bypass(self, queue=list()) -> None:
        if len(queue) == 0:
            return
        visited = set()
        while len(queue) != 0:
            curr_node = queue.pop(0)
            if curr_node in visited:
                continue
            print(curr_node)
            visited.add(curr_node)
            nodes_to_add = list(set(self.__graph.get(curr_node, [])) - visited)
            nodes_to_add.sort()
            queue += nodes_to_add

    def depth_bypass(self, node: str, visited=set()) -> None:
        print(node)
        visited.add(node)
        self.__graph.get(node, []).sort()
        for i in self.__graph.get(node, []):
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
