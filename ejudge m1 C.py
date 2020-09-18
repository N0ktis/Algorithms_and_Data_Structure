import re
from sys import argv


class Queue:
    def __init__(self, size: int):
        self.__queue = [None for i in range(size)]
        self.__tail = 0
        self.__head = 0

    def push(self, data: str):
        if self.__tail == self.__head and self.__queue[self.__head] is not None:
            return 'overflow'
        self.__queue[self.__tail] = data
        self.__tail = (self.__tail + 1) % len(self.__queue)

    def pop(self) -> str:
        if self.__queue[self.__head] is None:
            return 'underflow'
        buf = self.__queue[self.__head]
        self.__queue[self.__head] = None
        self.__head = (self.__head + 1) % len(self.__queue)
        return buf

    def print(self):
        if self.__queue[self.__head] is None:
            return 'empty'
        if self.__head < self.__tail:
            return self.__queue[self.__head:self.__tail]
        else:
            return self.__queue[self.__head:len(self.__queue)] + self.__queue[0:self.__tail]


def output_print(output_file, msg):
    if msg is None:
        return
    with open(output_file, 'a') as output_file:
        if isinstance(msg, list):
            output_file.write(' '.join(msg) + '\n')
        else:
            output_file.write(msg + '\n')


def parse_file(input_file, output_file):
    A = None
    with open(input_file, 'r') as input_file:
        for line in input_file:
            if line == '\n':
                continue
            elif re.search('set_size \d+', line) is not None and len(line.split()) == 2 and A is None:
                A = Queue(int(re.search('set_size \d+', line).group(0)[9:]))
            elif A is not None:
                if len(re.findall('[^print]', line)) > 1 and len(re.findall('[^pop]', line)) > 1 and len(
                        re.findall('^push [^ ]{2,}', line)) != 1:
                    output_print(output_file, 'error')
                elif line[:4] == 'push':
                    output_print(output_file, A.push(line[5:-1]))
                elif line[0:3] == 'pop':
                    output_print(output_file, A.pop())
                elif line[0:5] == 'print':
                    output_print(output_file, A.print())
            else:
                output_print(output_file, 'error')


input_file, out_file = argv[1:]
parse_file(input_file, out_file)
