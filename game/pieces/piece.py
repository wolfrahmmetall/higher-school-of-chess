from typing import List, Tuple, Optional
from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color: str, position: Tuple[int, int]):
        """
        Инициализация фигуры.

        :param color: 'white' или 'black'
        :param position: Кортеж (row, column) текущей позиции фигуры (индексация с 0)
        """
        if color.lower() not in ['white', 'black']:
            raise ValueError("Color must be 'white' or 'black'")
        self.color = color.lower()
        self.current_square = position  # (row, column)
        self._is_tied = False  # Изначально фигура не связана

    def get_current_square(self) -> Tuple[int, int]:
        """
        Возвращает текущую позицию фигуры.

        :return: Кортеж (row, column)
        """
        return self.current_square

    @abstractmethod
    def show_possible_moves(self, board: List[List[str]], last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[str]]] = None) -> List[str]:
        """
        Возвращает список возможных ходов для фигуры в текущей позиции.

        :param board: 8x8 матрица, представляющая шахматную доску.
                      Пустые клетки обозначены '',
                      белые фигуры начинаются с 'W', чёрные с 'B'.
        :param last_move: Последний совершённый ход в формате ((from_row, from_col), (to_row, to_col), promotion_piece)
        :return: Список строк с возможными ходами в формате 'a4', 'b5Q' и т.д.
        """
        pass

    @abstractmethod
    def name(self) -> str:
        """
        Возвращает обозначение фигуры.

        :return: Строка с обозначением фигуры (например, 'P' для пешки).
        """
        pass

    def is_tied(self) -> bool:
        """
        Проверяет, связана ли фигура.

        :return: True если фигура связана, иначе False
        """
        return self._is_tied

    def set_is_tied(self, tied: bool):
        """
        Устанавливает состояние связи фигуры.

        :param tied: True если фигура должна быть связана, иначе False
        """
        self._is_tied = tied

    def move(self, new_position: Tuple[int, int], board: List[List[str]]) -> None:
        """
        Перемещает фигуру на новую позицию на доске.

        :param new_position: Кортеж (row, column) новой позиции.
        :param board: 8x8 матрица, представляющая шахматную доску.
        """
        current_row, current_col = self.current_square
        new_row, new_col = new_position

        # Удаление фигуры с текущей позиции
        board[current_row][current_col] = ''

        # Установка фигуры на новую позицию
        board[new_row][new_col] = ('W_' if self.color == 'white' else 'B_') + self.name()

        # Обновление позиции фигуры
        self.current_square = new_position
    def _is_opponent_piece(self, piece: str) -> bool:
        """
        Проверяет, является ли фигура противником.

        :param piece: Строка, представляющая фигуру на доске
        :return: True если фигура противника, иначе False
        """
        if not piece:
            return False
        if self.color == 'white':
            return piece.startswith('B')
        else:
            return piece.startswith('W')
