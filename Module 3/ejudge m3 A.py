import fileinput
import math
import re
from functools import reduce


class Backpack:
    def __init__(self, max_weight: int):
        self.max_weight = max_weight
        self.total_value = 0
        self.total_weight = 0
        self.answer = list()
        self.__gcd = 1

    def __str__(self) -> str:
        """
        Перегружаем магический метод str, чтобы при вызове метода print корректно выводить данные
        :return: строка с ответом
        """
        answer = ''
        answer += str(self.total_weight) + ' ' + str(self.total_value) + '\n'
        for elem in self.answer:
            answer += str(elem) + '\n'
        return answer[:-1]

    @staticmethod
    def __find_gcd(weight: list) -> int:
        """
        Ищем НОД всего списка весов в функциональном стиле
        :param weight: список всех весов, используемых в задаче
        :return: общий НОД
        """
        return reduce(math.gcd, weight)

    @staticmethod
    def __normalize_weight(weight: list, gcd: int) -> list:
        """
        Функция, пропорционально уменьшающая каждый вес предмета
        :param weight: Список весов предметов, которые можно укладывать в рюкзак
        :param gcd: ранее вычесленный НОД
        :return: обновлённый список весов предметов
        """
        for i in range(len(weight)):
            weight[i] = int(weight[i] / gcd)
        return weight

    def knapsack_dp(self, value: list, weight: list) -> None:
        """
        Функция ищет максимально доступнную суммарную ценность предметов в рюкзаке.
        Используется метод динамического программирования
        :param value: список с ценностью каждого предмета
        :param weight: спсиок с весом каждого предмета
        :return: None; значение максимальной ценности заносится в атрибут self.total_value
        """
        self.__gcd = self.__find_gcd(weight + [self.max_weight])
        n = len(weight)
        max_weight = int(self.max_weight / self.__gcd)
        weight = self.__normalize_weight(weight, self.__gcd)
        m = [[0] * (max_weight + 1) for i in range(n + 1)]

        for i in range(1, n + 1):
            for j in range(0, max_weight + 1):  # начинаем с 0, чтобы учитывать предметы без массы
                if weight[i - 1] <= j:
                    m[i][j] = max(m[i - 1][j], value[i - 1] + m[i - 1][j - weight[i - 1]])
                else:
                    m[i][j] = m[i - 1][j]

        self.total_value = m[n][max_weight]
        self.find_ans(m, n, max_weight, weight)

    def find_ans(self, m: list, n: int, max_weight: int, weight: list) -> None:
        """
        Функция рекрсивно ищет предемты, которые составлют итоговую ценность рюкзака
        :param m: матрица с ценностью рюкзака при различных суммарном весе и предметах
        :param n: количество предметов, среди которых ищатся предметы, образующие итоговую ценность рюкзака
        :param max_weight: максимальная вместимость рюкзака для n предметов
        :param weight: список весов всех предметов
        :return: None; выбранные предметы заносятся в атрибут self.answer
        """
        if m[n][max_weight] == 0:
            return
        if m[n - 1][max_weight] == m[n][max_weight]:
            self.find_ans(m, n - 1, max_weight, weight)
        else:
            self.find_ans(m, n - 1, max_weight - weight[n - 1], weight)
            self.total_weight += weight[n - 1] * self.__gcd
            self.answer.append(n)


def parse_cmd(cmd):
    backpack = None
    value = list()
    weight = list()
    for line in cmd.input():
        if line == '\n':
            continue
        if backpack is None:
            if re.search('^\d+$', line) is not None and backpack is None:
                backpack = Backpack(int(line))
            else:
                print('error')
        else:
            if re.search('^\d+.\d+$', line) is not None:
                stroke = line.split()
                weight.append(int(stroke[0]))
                value.append(int(stroke[1]))
            else:
                print('error')
    backpack.knapsack_dp(value, weight)
    print(backpack)


if __name__ == '__main__':
    cmd = fileinput
    parse_cmd(cmd)
