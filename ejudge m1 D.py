import re
import fileinput
import sys

sys.setrecursionlimit(10000)


class Graph:
    def __init__(self, type: str, node: str, bypass_type: str):
        self.__graph = dict()
        self.__type = type
        self.__node = node
        self.bypass_type = bypass_type

    def add_edge(self, start: str, end, ):
        self.__graph.setdefault(start, []).append(end)
        if self.__type == 'u':
            self.__graph.setdefault(end, []).append(start)

    def breadth_bypass(self):
        print(self.__node)
        mas = self.__graph.get(self.__node)
        while len(mas) != 0:
            print(*mas)
            buf = mas[::-1]
            mas = []
            while len(buf) != 0:
                mas += self.__graph.get(buf.pop(), '')

    # def depth_bypass(self):


def parse_cmd(cmd):
    A = None
    for line in cmd.input():
        if line == '\n':
            continue
        if A is None:
            A = Graph(*line[:-1].split())
            continue
        A.add_edge(*line[:-1].split())
    A.breadth_bypass()


cmd = fileinput
parse_cmd(cmd)
