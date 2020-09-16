import numpy as np
# 1) Реализовать алгоритм быстрого возведения программно, протестировать его.
def square(m, n: int):
    '''
    :param m: основание
    :param n: степень; целое неотрицательное число
    :return: m^n
    '''

    if not isinstance(m, (int, float)) or not isinstance(n, int):
        return 'ERROR'
    if n == 0:
        return 1
    elif n % 2 == 0:
        return square(m, int(n / 2)) * square(m, int(n / 2))
    elif n % 2 != 0:
        return square(m, n - 1) * m


# 2) Написать алгоритм получения N-того числа Фибоначчи за log(n).
def fibonacci(n: int):
    '''
    :param n: порядковый номер необходимог числа Фибоначчи
    :return: число Фибоначчи
    '''
    if not isinstance(n, int):
        return 'ERROR'
    return np.linalg.matrix_power(np.array([[1,1],[1,0]]),n-1)[0][1]
#    if n == 1:
#        return 0
#    elif n == 2:
#        return 1
#    return fibonacci(n - 1) + fibonacci(n - 2)


# 3) Написать алгоритм генерации подстановок в лексикографическом порядке, оценить его сложность.
#def permutation(n)

# 5) Написать алгоритм проверки числа на простоту.
def prime_number(n: int):
    '''
    :param n: целое число, которое проверяют на простоту
    :return: результат проверки числа n
    '''
    if not isinstance(n, int):
        return 'ERROR'
    i = 2
    flag = True
    while square(i, 2) <= n and flag:
        if n % i == 0:
            flag = False
        i += 1
    if not flag:
        return "Составное число"
    else:
        return "Простое число"


print(prime_number(139))
