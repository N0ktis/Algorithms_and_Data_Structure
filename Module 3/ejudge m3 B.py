import fileinput
import re


def get_count_zero(bin_val: str) -> int:
    """
    Функция ищет количество подряд идущих нуоей справой стороны числа в двоично СС
    :param bin_val: строка, являющаяся двоичной записью числа
    :return: количество нулей
    """
    s = 0
    for i in bin_val[::-1]:
        if i == '0':
            s += 1
        else:
            return s


def optimal_strategy(half_capital: int) -> list:
    """
    Функция ищет выграшную стратегию
    :param half_capital: Сумма половины состояния богача
    :return: последовательность действий(в обратном порядке), необходимая для выиграша

    Алгоритм:
    Идём в обратном направлении, уменьшая состояние богача до 0(разоряем его)
    - если осталось чётная сумма, то делаем dbl
    - если осталось нечётная сумма, то:
        - если осталась 1, то делаем inc
        - если осталась 3, то делаем inc (данный случай рассматриваем так как алгоритм решит,
            что довести до 4(100) лучше, чем до 2(10), что увеличит количество ходов на 1)
        - иначе, доводим число с помощью inc/dec до числа с наибольшим количеством нулей
            в двоичной записи справа(так мы сможем больше раз сделать dbl)
    """

    strategy = list()
    while half_capital != 0:
        if half_capital % 2 == 0:
            strategy.append('dbl')
            half_capital = int(half_capital / 2)
        else:
            if half_capital == 1:
                strategy.append('inc')
                half_capital -= 1
                return strategy
            elif half_capital == 3:
                strategy.append('inc')
                half_capital -= 1
            else:
                bin_inc = bin(half_capital + 1)
                bin_dec = bin(half_capital - 1)
                if get_count_zero(bin_inc) > get_count_zero(bin_dec):
                    strategy.append('dec')
                    half_capital += 1
                else:
                    strategy.append('inc')
                    half_capital -= 1


def parse_cmd(cmd):
    half_capital = None
    for line in cmd.input():
        if line == '\n':
            continue
        if re.search('^\d+$', line) is not None:
            half_capital = int(line)
        else:
            print('error')

    strategy = optimal_strategy(half_capital)

    for i in strategy[::-1]:
        print(i)


if __name__ == '__main__':
    cmd = fileinput
    parse_cmd(cmd)
