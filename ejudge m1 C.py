queue_flag = False
tail = 0
head=0
while True:
    command = input().split()

    if command[0] == 'set_size' and command[1].isdecimal():
        queue = [None for i in range(int(command[1]))]
        tail = 0
        head=0
        queue_flag = True
    if queue_flag:

        if command[0] == 'push':
            if tail == len(queue):
                print('overflow')
                continue
            queue[tail] = command[1]
            tail += 1
        if command[0] == 'pop':
            if queue is None:
                print('overflow')
                continue
            tail -= 1
            print(queue[tail])
            queue[tail] = None
        if command[0] == 'print':
            print(*queue[head:tail])#dont work
    else:
        print('overflow')
        continue

