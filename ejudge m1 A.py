import re
import fileinput


def sum(stroke) -> int:
    s = 0  # sum of input numbers
    for i in stroke.input():
        for j in re.findall('[-+]?\d+', i):
            s += int(j)
    return s


A = fileinput
print(sum(A))
