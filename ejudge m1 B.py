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

