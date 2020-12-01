import fileinput
import re
from collections import deque, defaultdict


class Word:
    def __init__(self, word):
        self.word = word
        self.children = dict()


class BK_tree:
    def __init__(self):
        self.__root = None

    def insert_word(self, word: str, vertex=None) -> None:
        """
        Функция рекурсивно добавляет новую вершину в BK-дерево
        :param word: слово, которые будет находиться в вершине
        :param vertex: вершина, к которой планируется присоеденить новую(если параметр не указан, то добавляем в корень)
        :return: None
        """
        word = word.lower()
        if vertex is None:
            if self.__root is None:
                self.__root = Word(word)
                return
            self.insert_word(word, self.__root)
            return

        dist = self.__damerau_levenshtein(word, vertex.word)

        if dist in vertex.children:
            self.insert_word(word, vertex.children[dist])
        else:
            vertex.children.setdefault(dist, Word(word))
            return

    def autocorrection(self, incorrect_word: str, k=1) -> list:
        """
        Функция определяет набор слов из BK-дерева, правописание которых схоже со входным словом
        :param incorrect_word: слово для проверки правильности его написания
        :param k: дистанция редактирования; максимально количество ошибок, допущенных во входном слове(по умолчанию равно 1)
        :return: список слов, правописание которых похоже на входное;
        если входное слово написано правильно - возвращает "ok", если не удалось найти похожие слова - возвращает - "?"
        """
        if self.__root is None:
            raise Exception('error')

        answer = []
        queue = deque()
        queue.append(self.__root)
        while len(queue) != 0:
            curr_node = queue.popleft()
            if curr_node.word == incorrect_word.lower():
                return [' ok']

            dist = self.__damerau_levenshtein(incorrect_word.lower(), curr_node.word)
            if dist <= k:
                answer.append(curr_node.word)
            for i in curr_node.children:
                if dist - k <= i <= dist + k:
                    '''
                    Чтобы минимизировать время поиска точного совпадения с входным словом в BK-дереве, посещаем при 
                    обходе сначала те вершины, которые могут его содержать это слово. 
                    Для текущего узла таким является только дочерний узел с таким же расстоянием Дамерау-Левенштейна,
                    что и текущий узел.
                    '''
                    if i == dist:
                        queue.appendleft(curr_node.children[i])
                    else:
                        queue.append(curr_node.children[i])

        if len(answer) == 0:
            return ['?']
        else:
            return answer

    @staticmethod
    def __damerau_levenshtein(word1: str, word2: str) -> int:
        """
        Функция определяет расстояние Дамерау-Левенштейна между двумя строками.
        Используется корректный(не упрощённый) алгоритм расчёта.
        :param word1: первое слово для расчёта расстояния
        :param word2: второе слово для расчёта расстояния
        :return: расстояние Дамерау-Левенштейна
        """
        len_word1 = len(word1)
        len_word2 = len(word2)
        max_dist = len_word1 + len_word2
        alph_dict = defaultdict(int)  # словарь встреченных букв в слове word1 с указание позиции буквы в слове

        dist_matrix = [[0] * (len_word2 + 2) for i in range(len_word1 + 2)]

        for i in range(len_word1 + 1):
            dist_matrix[i + 1][1] = i
            dist_matrix[i + 1][0] = max_dist

        for j in range(len_word2 + 1):
            dist_matrix[1][j + 1] = j
            dist_matrix[0][j + 1] = max_dist

        dist_matrix[0][0] = max_dist

        for i in range(1, len_word1 + 1):
            letter_pos = 0
            for j in range(1, len_word2 + 1):
                k = alph_dict[word2[j - 1]]
                l = letter_pos
                value = 1
                if word1[i - 1] == word2[j - 1]:
                    value = 0
                    letter_pos = j
                dist_matrix[i + 1][j + 1] = min(
                    dist_matrix[i][j] + value,  # замена
                    dist_matrix[i + 1][j] + 1,  # вставка
                    dist_matrix[i][j + 1] + 1,  # удаление
                    dist_matrix[k][l] + (i - k - 1) + 1 + (j - l - 1))  # транспозиция
            alph_dict[word1[i - 1]] = i
        return dist_matrix[len_word1 + 1][len_word2 + 1]

    @staticmethod
    def print(word: str, answer: list) -> None:
        """
        Функция печатает переданные параметры в установленном формате
        :param word: слово, поданное на проверку
        :param answer: список, полученный после выполнения функции autocorrection
        :return: None
        """
        if answer[0] == ' ok' or answer[0] == '?':
            print(word, '-' + answer[0])
        else:
            answer.sort()
            print(word, '->', ', '.join(answer))


def parse_cmd(cmd):
    bk_tree = BK_tree()
    dict_size = None
    i = 0
    for line in cmd.input():
        if line == '\n':
            continue
        if dict_size is None:
            if re.search('^\d+$', line) is not None:
                dict_size = int(line)
            else:
                print('error')
        else:
            if i < dict_size:  # не костыль, а протез
                bk_tree.insert_word(line[:-1])
                i += 1
            else:
                try:

                    correction = bk_tree.autocorrection(line[:-1])
                    bk_tree.print(line[:-1], correction)
                except Exception as msg:
                    print(msg)


if __name__ == '__main__':
    cmd = fileinput
    parse_cmd(cmd)
