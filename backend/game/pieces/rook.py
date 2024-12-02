from typing import List, Tuple, Optional
from .piece import Piece


class Rook(Piece):
    def __init__(self, color: str, position: Tuple[int, int]):
        """
        Инициализация ладьи.

        :param color: 'white' или 'black'
        :param position: Кортеж (row, column) текущей позиции ладьи (индексация с 0)
        """
        super().__init__(color, position)
        self.has_moved = False  # Атрибут для отслеживания перемещений ладьи

    def name(self) -> str:
        """
        Возвращает обозначение ладьи.

        :return: 'R' для белой ладьи, 'r' для чёрной ладьи.
        """
        return 'R' if self.color == 'white' else 'r'

    def show_possible_moves(
            self,
            board: List[List[Optional[Piece]]],
            last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[str]]] = None
    ) -> List[Tuple[int, int]]:
        """
        Возвращает список возможных ходов для ладьи в текущей позиции.

        :param board: 8x8 матрица, представляющая шахматную доску.
                      Пустые клетки обозначены None,
                      фигуры представлены объектами наследниками класса Piece.
        :param last_move: Не используется для ладьи, добавлен для совместимости.
        :return: Список строк с возможными ходами в формате 'a4', 'b5' и т.д.
        """
        moves = []
        row, col = self.current_square

        # Если фигура связана, она не может двигаться
        if self.is_tied():
            return moves  # Пустой список, так как фигура связана

        # Направления движения ладьи (вертикали и горизонтали)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board[new_row][new_col]
                if target_piece is None:
                    # Пустая клетка
                    move = (new_row, new_col)
                    moves.append(move)
                else:
                    if self._is_opponent_piece(target_piece):
                        # Вражеская фигура может быть взята
                        move = (new_row, new_col)
                        moves.append(move)
                    # Если фигура своей, то дальше двигаться нельзя
                    break

                # Продолжаем двигаться в том же направлении
                new_row += dr
                new_col += dc

        return moves

    def move(
            self,
            move: Tuple[int, int],
            board: List[List[Optional['Piece']]]
    ) -> bool:
        """
        Выполняет ход ладьёй, если он допустим.

        :param move: Кортеж с ходом, например (0, 0), (0, 7) и т.д., где первый элемент — строка, второй — столбец.
        :param board: 8x8 матрица, представляющая шахматную доску.
        :return: True если ход выполнен, иначе False
        """
        possible_moves = self.show_possible_moves(board)
        if move not in possible_moves:
            return False

        new_row, new_col = move
        target_piece = board[new_row][new_col]
        if target_piece is not None:
            if self._is_opponent_piece(target_piece):
                pass
            else:
                # Это условие уже покрыто в show_possible_moves
                pass

        # Перемещаем ладью на новую позицию
        board[self.current_square[0]][self.current_square[1]] = None
        board[new_row][new_col] = self
        self.current_square = (new_row, new_col)

        # Устанавливаем флаг, что ладья уже двигалась
        self.has_moved = True

        return True

    def _is_opponent_piece(self, piece: 'Piece') -> bool:
        """
        Проверяет, принадлежит ли фигура противнику.

        :param piece: Фигура для проверки.
        :return: True если фигура принадлежит противнику, иначе False.
        """
        return piece.color != self.color
