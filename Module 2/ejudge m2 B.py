import fileinput
import re
from collections import deque


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.parent = None
        self.left_ch = self.right_ch = None


class SplayTree:
    def __init__(self):
        self.root = None

    def __zig(self, node):
        # происходит Санта-Барбара
        node.parent.left_ch = node.right_ch
        if node.right_ch is not None:
            node.right_ch.parent = node.parent
        node.right_ch = node.parent
        if node.right_ch.parent is not None:
            if node.right_ch.parent.left_ch == node.right_ch:
                node.right_ch.parent.left_ch = node
            else:
                node.right_ch.parent.right_ch = node
        node.parent = node.right_ch.parent
        node.right_ch.parent = node
        return node

    def __zag(self, node):
        # происходит Санта-Барбара
        node.parent.right_ch = node.left_ch
        if node.left_ch is not None:
            node.left_ch.parent = node.parent
        node.left_ch = node.parent
        if node.left_ch.parent is not None:
            if node.left_ch.parent.left_ch == node.left_ch:
                node.left_ch.parent.left_ch = node
            else:
                node.left_ch.parent.right_ch = node
        node.parent = node.left_ch.parent
        node.left_ch.parent = node
        return node

    def __splay(self, node) -> None:
        while node.parent is not None:
            if node.parent.parent is None:
                if node == node.parent.left_ch:
                    # zig
                    node = self.__zig(node)
                else:
                    # zag
                    node = self.__zag(node)

            elif node == node.parent.left_ch and node.parent == node.parent.parent.left_ch:
                # zig-zig
                node.parent = self.__zig(node.parent)
                node = self.__zig(node)

            elif node == node.parent.right_ch and node.parent == node.parent.parent.right_ch:
                # zag-zag
                node.parent = self.__zag(node.parent)
                node = self.__zag(node)

            elif node == node.parent.right_ch and node.parent == node.parent.parent.left_ch:
                # zig-zag
                node = self.__zag(node)
                node = self.__zig(node)

            else:
                # zag-zig
                node = self.__zig(node)
                node = self.__zag(node)

            if node.parent is None:
                # назначаем вершину корнем дерева
                self.root = node

    def add(self, key: int, value: str) -> None:
        node = Node(key, value)
        root = self.root
        parent = None

        if self.root is None:
            self.root = node
            return
        while root is not None:
            parent = root
            if key < root.key:
                root = root.left_ch
            elif key > root.key:
                root = root.right_ch
            else:
                # исключаем возможность добавления такого же ключа
                self.search(key)
                raise Exception('error')
        if node.key < parent.key:
            parent.left_ch = node
        else:
            parent.right_ch = node
        node.parent = parent
        self.__splay(node)

    def set(self, key: int, value: str) -> None:
        if self.root is None:
            raise Exception('error')
        if self.search(key) is not None:
            self.root.value = value
        else:
            raise Exception('error')

    def search(self, key: int):
        node = self.root
        buf = None  # буферная переменная для хранения родителя текущей следующей вершины(если она есть) в цикле
        while node is not None:
            buf = node
            if node.key == key:
                self.__splay(node)
                return node
            else:
                if key < node.key:
                    node = node.left_ch
                else:
                    node = node.right_ch
        self.__splay(buf)
        raise Exception('error')

    def delete(self, key: int) -> None:
        if self.root is None:
            raise Exception('error')
        if self.search(key) is not None:  # выталкиваем удаляемую вершину в корень
            if self.root.right_ch is None and self.root.left_ch is None:  # в дереве только корень
                self.root = None
            elif self.root.right_ch is None:  # у корня есть только левое поддерево
                self.root.left_ch.parent = None
                self.root = self.root.left_ch
            elif self.root.left_ch is None:  # у корня есть только правое поддерево
                self.root.right_ch.parent = None
                self.root = self.root.right_ch
            else:  # у корня есть оба поддерева
                self.max(self.root.left_ch)
                self.root.right_ch.parent = None
                self.root.right_ch = self.root.right_ch.right_ch
                self.root.right_ch.parent = self.root
        else:
            raise Exception('error')

    def min(self, tree):
        if self.root is None:
            raise Exception('error')
        while tree.left_ch is not None:
            tree = tree.left_ch
        self.__splay(tree)
        return tree

    def max(self, tree):
        if self.root is None:
            raise Exception('error')
        while tree.right_ch is not None:
            tree = tree.right_ch
        self.__splay(tree)
        return tree

    def print(self, queue=deque()) -> None:
        new_queue = deque()
        answer = ''
        flag = False  # флаг для того, чтобы знать есть ли у нас ещё вершины для обхода
        while len(queue) != 0:
            queue_elem = queue.popleft()
            if queue_elem == '_':
                new_queue.append('_')
                new_queue.append('_')
                answer += '_ '
                continue
            elif queue_elem.parent is None:
                answer += '[' + str(queue_elem.key) + ' ' + queue_elem.value + '] '
            else:
                answer += '[' + str(queue_elem.key) + ' ' + queue_elem.value + ' ' + str(
                    queue_elem.parent.key) + '] '
            if queue_elem.left_ch is not None:
                flag = True
                new_queue.append(queue_elem.left_ch)
            else:
                new_queue.append('_')

            if queue_elem.right_ch is not None:
                flag = True
                new_queue.append(queue_elem.right_ch)
            else:
                new_queue.append('_')
        print(answer[:-1])
        if flag:
            self.print(new_queue)
        return


def parse_cmd(cmd):
    spl_tree = SplayTree()
    for line in cmd.input():
        if line == '\n':
            continue
        else:
            if len(re.findall('[^print]', line)) > 1 and len(re.findall('[^min]', line)) > 1 and len(
                    re.findall('[^max]', line)) > 1 and len(re.findall('^delete [^ ]{1,}$', line)) != 1 and len(
                re.findall('^search [^ ]{1,}$', line)) != 1 and len(
                re.findall('^set [^ ]{1,} [^ ]{1,}$', line)) != 1 and len(
                re.findall('^add [^ ]{1,} [^ ]{1,}$', line)) != 1:
                print('error')

            elif line[:3] == 'add':
                stroke = line[4:-1].split()
                try:
                    spl_tree.add(int(stroke[0]), stroke[1])
                except Exception as msg:
                    print(msg)

            elif line[:3] == 'set':
                try:
                    stroke = line[4:-1].split()
                    spl_tree.set(int(stroke[0]), stroke[1])
                except Exception as msg:
                    print(msg)

            elif line[:3] == 'max':
                try:
                    node = spl_tree.max(spl_tree.root)
                    print(node.key, node.value)
                except Exception as msg:
                    print(msg)

            elif line[:3] == 'min':
                try:
                    node = spl_tree.min(spl_tree.root)
                    print(node.key, node.value)
                except Exception as msg:
                    print(msg)

            elif line[:6] == 'delete':
                try:
                    spl_tree.delete(int(line[7:-1]))
                except Exception as msg:
                    print(msg)

            elif line[:6] == 'search':
                try:
                    print('1 ' + spl_tree.search(int(line[7:-1])).value)
                except Exception:
                    print('0')

            elif line[:5] == 'print':
                if spl_tree.root is None:
                    print('_')
                    continue
                buf = deque()
                buf.append(spl_tree.root)
                spl_tree.print(buf)


cmd = fileinput
parse_cmd(cmd)
