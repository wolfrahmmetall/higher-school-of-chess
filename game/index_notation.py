from typing import Tuple


def index_to_notation(row: int, col: int) -> str:
    """
    Преобразует индексы доски в шахматную нотацию.
    :param row: Номер строки (0-7)
            :param col: Номер столбца (0-7)
            :return: Строка с шахматной нотацией, например 'e4'
            """
    letters = 'abcdefgh'
    return f"{letters[col]}{8 - row}"

def notation_to_index(notation: str) -> Tuple[int, int]:
        """
        Преобразует шахматную нотацию в индексы доски.

        :param notation: Строка с шахматной нотацией, например 'e4'
        :return: Кортеж (row, column)
        :raises ValueError: Если формат нотации некорректен
        """
        if len(notation) != 2:
            raise ValueError("Неверная длина нотации хода.")

        letters = 'abcdefgh'
        letter, number = notation[0], notation[1]

        if letter not in letters or not number.isdigit():
            raise ValueError("Неверные символы в нотации хода.")

        col = letters.index(letter)
        row = 8 - int(number)

        if not (0 <= row < 8 and 0 <= col < 8):
            raise ValueError("Ход выходит за пределы доски.")

        return row, col
