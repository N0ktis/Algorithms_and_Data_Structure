import fileinput
import re


class Stack:
    def __init__(self, size: int):
        self.__stack = [None for i in range(size)]
        self.__tail = 0

    def push(self, data: str) -> None:
        if self.__tail == len(self.__stack):
            print('overflow')
            return
        self.__stack[self.__tail] = data
        self.__tail += 1

    def pop(self) -> str:
        if self.__tail == 0:
            return 'underflow'
        self.__tail -= 1
        buf = self.__stack[self.__tail]
        self.__stack[self.__tail] = None
        return buf

    def print(self):
        if self.__tail == 0:
            print('empty')
            return
        print(*self.__stack[:self.__tail])


def parse_cmd(cmd):
    A = None
    for line in cmd.input():
        if line == '\n':
            continue
        elif re.search('set_size \d+', line) is not None and len(line.split()) == 2 and A is None:
            A = Stack(int(re.search('set_size \d+', line).group(0)[9:]))
        elif A is not None:
            if len(re.findall('[^print]', line)) > 1 and len(re.findall('[^pop]', line)) > 1 and len(
                    re.findall('^push [^ ]{2,}', line)) != 1:
                print('error')
            elif line[:4] == 'push':
                A.push(line[5:-1])
            elif line[0:3] == 'pop':
                print(A.pop())
            elif line[0:5] == 'print':
                A.print()
        else:
            print('error')


cmd = fileinput
parse_cmd(cmd)
