import fileinput
import re
from math import log2, log, sqrt

MERSENN_31 = pow(2, 31) - 1


class BitArray:
    def __init__(self, size: int):
        self.bits = [0b00 for i in range((size + 31) // 32)]
        self.arr_size = size

    def __and__(self, bit_array):
        new_bit_array = []
        for byte1, byte2 in zip(self.bits, bit_array.bits):
            new_bit_array.append(byte1 & byte2)
        return new_bit_array

    def equal_bit(self, bit_index: int) -> bool:
        int_index = (bit_index // 32)
        bit_index = (bit_index % 32)
        return self.bits[int_index] | (1 << (31 - bit_index)) == self.bits[int_index]

    def bit_set(self, index: int):
        int_index = (index // 32)
        bit_index = (index % 32)
        self.bits[int_index] = self.bits[int_index] | (1 << (31 - bit_index))

    def print(self):
        answer = ''
        for byte in self.bits:
            line = str(bin(byte))[2:]
            if len(line) % 32 != 0:
                line = '0' * (32 - len(line)) + line
            answer += line
        print(answer[:self.arr_size])


class BloomFilter:
    def __init__(self, m: int, p: float):
        if m == 0 or p == 0 or p >= 1:
            raise Exception('error')
        self.num_hash = self.__hash_count(p)
        self.size = self.__size_count(m, p)
        self.bit_array = BitArray(self.size)
        self.__prime_numbers = self.__prime_num_generator(self.num_hash)

    @staticmethod
    def __hash_count(p: float) -> int:
        num_hash = int(round(-log2(p)))
        if num_hash == 0:
            raise Exception('error')
        return num_hash

    @staticmethod
    def __size_count(m: int, p: float) -> int:
        return int(round(-m * log2(p) / log(2)))

    @staticmethod
    def __is_prime(number: int) -> bool:
        i = 2
        flag = True
        if number == 2:
            return True
        else:
            while i <= sqrt(number) and flag:
                if number % i == 0:
                    flag = False
                    break
                i += 1
        return flag

    def __prime_num_generator(self, count: int) -> list:
        prime_numbers = []
        i = 0
        p = 2
        while i != count:
            if self.__is_prime(p):
                prime_numbers.append(p)
                i += 1
            p += 1
        return prime_numbers

    def __hash(self, i, value):
        return int((((i + 1) * value + self.__prime_numbers[i]) % MERSENN_31) % self.size)

    def add(self, value: int):
        for i in range(self.num_hash):
            self.bit_array.bit_set(self.__hash(i, value))

    def search(self, value: int):
        buf_bits1 = BitArray(self.size)
        for i in range(self.num_hash):
            index = self.__hash(i, value)
            buf_bits1.bit_set(index)
            if not self.bit_array.equal_bit(index):
                return False
        return True

    def print(self):
        self.bit_array.print()


def parse_cmd(cmd):
    bloom_filter = None
    for line in cmd.input():
        if line == '\n':
            continue
        elif len(re.findall('[^print$]', line)) > 1 and len(re.findall('^search [^ ,-][\d]{0,}$', line)) != 1 and len(
                re.findall('set [^ ,-][\d]{0,} [^ ,-][.+\d]{1,}$', line)) != 1 and len(
            re.findall('^add [^ ,-][\d]{0,}$', line)) != 1:
            print('error')

        elif bloom_filter is None:
            if line[:3] == 'set':
                try:
                    stroke = line[4:-1].split()
                    bloom_filter = BloomFilter(int(stroke[0]), float(stroke[1]))
                    print(bloom_filter.size, bloom_filter.num_hash)
                except Exception as msg:
                    print(msg)
            else:
                print('error')
        else:
            if line[:3] == 'add':
                #try:
                    bloom_filter.add(int(line[4:]))
                #except Exception as msg:
                    #print(msg)

            elif line[:6] == 'search':
                try:
                    print('1' if (bloom_filter.search(int(line[7:]))) else '0')
                except Exception:
                    print('error')

            elif line[:5] == 'print':
                bloom_filter.print()
            else:
                print('error')


if __name__ == '__main__':
    cmd = fileinput
    parse_cmd(cmd)
