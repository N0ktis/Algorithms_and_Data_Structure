import re
import fileinput

class Stack:
    def __init__(self, size: int):
        self.stack = [None for i in range(size)]
        self.tail = 0

    def push(self, data: str):
        if self.tail == len(self.stack):
            print('overflow')
        self.stack[self.tail] = data
        self.tail += 1

    def pop(self) -> str:
        if self.tail == 0:
            print('overflow')
        self.tail -= 1
        buf = self.stack[self.tail]
        self.stack[self.tail] = None
        return buf

    def print(self):
        if self.tail == 0:
            return 'empty'
        return self.stack[:self.tail]


for i in fileinput.input():


'''
stack_flag = False
tail = 0
while True:
    command = input().split()

    if command[0] == 'set_size' and command[1].isdecimal():
        stack = [None for i in range(int(command[1]))]
        tail = 0
        stack_flag = True
    if stack_flag:
        if command[0] == 'push':
            if tail == len(stack):
                print('overflow')
                continue
            stack[tail] = command[1]
            tail += 1
        if command[0] == 'pop':
            if tail == 0:
                print('overflow')
                continue
            tail -= 1
            print(stack[tail])
            stack[tail] = None
        if command[0] == 'print':
            print(*stack[:tail])
    if command=='':
        break
    else:
        print('overflow')
        continue

'''
