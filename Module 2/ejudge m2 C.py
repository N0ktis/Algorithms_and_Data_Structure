import fileinput
import re
from collections import deque


class Node:
    def __init__(self, key: int, value: str):
        self.key = key
        self.value = value


class MinBinaryHeap:
    def __init__(self):
        self.data = list()
        self.__key_index = dict()

    def __left_ch(self, index: int) -> int:
        return 2 * index + 1

    def __right_ch(self, index: int) -> int:
        return 2 * index + 2

    def __parent(self, index: int) -> int:
        return int((index - 1) / 2)

    def __swap(self, first_elem: int, second_elem: int):
        self.__key_index[self.data[first_elem].key], self.__key_index[
            self.data[second_elem].key] = second_elem, first_elem
        self.data[first_elem], self.data[second_elem] = self.data[second_elem], self.data[first_elem]

    def __heapify(self, index: int, root=False, direction_up=True):
        if index == 0 and not root:
            return

        if direction_up:
            parent_index = self.__parent(index)
            if self.data[index].key < self.data[parent_index].key:
                self.__swap(index, parent_index)
                self.__heapify(parent_index)
        else:
            left_ch_index = self.__left_ch(index)
            right_ch_index = self.__right_ch(index)
            min_elem_index = index

            if left_ch_index < len(self.data) and self.data[left_ch_index].key < self.data[min_elem_index].key:
                min_elem_index = left_ch_index
            if right_ch_index < len(self.data) and self.data[right_ch_index].key < self.data[min_elem_index].key:
                min_elem_index = right_ch_index

            if min_elem_index != index:
                self.__swap(index, min_elem_index)
                self.__heapify(min_elem_index, direction_up=False)

    def add(self, key: int, value: str):
        new_node = Node(key, value)
        if key in self.__key_index.keys():
            raise Exception('error')
        self.data.append(new_node)
        self.__key_index[key] = len(self.data) - 1
        self.__heapify(self.__key_index[key])

    def set(self, key: int, value: str):
        if key in self.__key_index.keys():
            self.data[self.__key_index[key]].value = value
        else:
            raise Exception('error')

    def search(self, key: int) -> tuple:
        if key in self.__key_index.keys():
            return self.__key_index[key], self.data[self.__key_index[key]].value
        else:
            raise Exception('0')

    def delete(self, key: int):
        root = False
        if key in self.__key_index.keys():
            key_index = self.__key_index[key]
            if key_index == 0:
                root = True
        else:
            raise Exception('error')

        self.__swap(key_index, len(self.data) - 1)

        self.data.pop()
        self.__key_index.pop(key)
        if key_index < len(self.data):
            self.__heapify(key_index)
        self.__heapify(key_index, root=root, direction_up=False)

    def min(self) -> tuple:
        if len(self.data) == 0:
            raise Exception('error')
        return self.data[0].key, '0', self.data[0].value

    def max(self) -> tuple:
        if len(self.data) == 0:
            raise Exception('error')
        max_key = max(self.__key_index)
        index = self.__key_index.get(max_key)
        value = self.data[index].value
        return max_key, index, value

    def extract(self) -> tuple:
        if len(self.data) == 0:
            raise Exception('error')
        answer = (self.data[0].key, self.data[0].value)
        self.delete(self.data[0].key)
        return answer

    def print(self, queue=deque()) -> None:
        new_queue = deque()
        answer = ''
        flag = False  # флаг для того, чтобы знать есть ли у нас ещё вершины для обхода
        while len(queue) != 0:
            queue_elem = queue.popleft()
            if queue_elem == '_':
                answer += '_ '
                continue
            elif queue_elem == 0:
                answer += '[' + str(self.data[queue_elem].key) + ' ' + self.data[queue_elem].value + '] '
            else:
                answer += '[' + str(self.data[queue_elem].key) + ' ' + self.data[queue_elem].value + ' ' + str(
                    self.data[self.__parent(queue_elem)].key) + '] '
            if self.__left_ch(queue_elem) <= len(self.data) - 1:
                flag = True
                new_queue.append(self.__left_ch(queue_elem))
            else:
                new_queue.append('_')

            if self.__right_ch(queue_elem) <= len(self.data) - 1:
                flag = True
                new_queue.append(self.__right_ch(queue_elem))
            else:
                new_queue.append('_')
        print(answer[:-1])
        if flag:
            self.print(new_queue)
        return


def parse_cmd(cmd):
    bin_heap = MinBinaryHeap()
    for line in cmd.input():
        if line == '\n':
            continue
        else:
            if len(re.findall('[^print]', line)) > 1 and len(re.findall('[^min]', line)) > 1 and len(
                    re.findall('[^max]', line)) > 1 and len(re.findall('^delete [^ ]{1,}$', line)) != 1 and len(
                re.findall('^search [^ ]{1,}$', line)) != 1 and len(
                re.findall('^set [^ ]{1,} [^ ]{1,}$', line)) != 1 and len(
                re.findall('^add [^ ]{1,} [^ ]{1,}$', line)) != 1 and len(re.findall('[^extract]', line)) > 1:
                print('error')

            elif line[:3] == 'add':
                stroke = line[4:-1].split()
                try:
                    bin_heap.add(int(stroke[0]), stroke[1])
                except Exception as msg:
                    print(msg)

            elif line[:3] == 'set':
                try:
                    stroke = line[4:-1].split()
                    bin_heap.set(int(stroke[0]), stroke[1])
                except Exception as msg:
                    print(msg)

            elif line[:3] == 'max':
                try:
                    print(*bin_heap.max())
                except Exception as msg:
                    print(msg)

            elif line[:3] == 'min':
                try:
                    print(*bin_heap.min())
                except Exception as msg:
                    print(msg)

            elif line[:6] == 'delete':
                try:
                    bin_heap.delete(int(line[7:-1]))
                except Exception as msg:
                    print(msg)

            elif line[:7] == 'extract':
                try:
                    print(*bin_heap.extract())
                except Exception as msg:
                    print(msg)

            elif line[:6] == 'search':
                try:
                    print('1', *bin_heap.search(int(line[7:])))
                except Exception:
                    print('0')

            elif line[:5] == 'print':
                if len(bin_heap.data) == 0:
                    print('_')
                    continue
                buf = deque()
                buf.append(0)
                bin_heap.print(buf)


if __name__ == '__main__':
    cmd = fileinput
    parse_cmd(cmd)
