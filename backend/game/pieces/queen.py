from typing import List, Tuple, Optional
from .piece import Piece


class Queen(Piece):
    def __init__(self, color: str, position: Tuple[int, int]):
        """
        Инициализация ферзя.

        :param color: 'white' или 'black'
        :param position: Кортеж (row, column) текущей позиции ферзя (индексация с 0)
        """
        super().__init__(color, position)

    def name(self) -> str:
        """
        Возвращает обозначение ферзя.

        :return: 'Q' для белого ферзя, 'q' для чёрного ферзя.
        """
        return '\u2655' if self.color == 'white' else '\u265B'

    def show_possible_moves(
            self,
            board: List[List[Optional['Piece']]],
            last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[str]]] = None
    ) -> List[Tuple[int, int]]:
        """
        Возвращает список возможных ходов для ферзя в текущей позиции.

        :param board: 8x8 матрица, представляющая шахматную доску.
                      Пустые клетки обозначены None,
                      фигуры представлены объектами наследниками класса Piece.
        :param last_move: Не используется для ферзя, добавлен для совместимости.
        :return: Список строк с возможными ходами в формате 'a4', 'b5' и т.д.
        """
        moves = []
        row, col = self.current_square

        # Если фигура связана, она не может двигаться
        if self.is_tied():
            return moves  # Пустой список, так как фигура связана

        # Направления движения ферзя (комбинация направлений ладьи и слона)
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

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
        Выполняет ход ферзем, если он допустим.

        :param move: Кортеж с ходом, например (0, 3), (4, 7) и т.д., где первый элемент — строка, второй — столбец.
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

        # Перемещаем ферзя на новую позицию
        super().move((new_row, new_col), board)

        return True
