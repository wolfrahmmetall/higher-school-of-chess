from typing import List, Tuple, Optional
import Piece
class Bishop(Piece):
    def __init__(self, color: str, position: Tuple[int, int]):
        """
        Инициализация слона.

        :param color: 'white' или 'black'
        :param position: Кортеж (row, column) текущей позиции слона (индексация с 0)
        """
        super().__init__(color, position)

    def name(self) -> str:
        """
        Возвращает обозначение пешки.

        :return: 'P' для белой пешки, 'p' для чёрной пешки.
        """
        return 'B' if self.color == 'white' else 'b'

    def show_possible_moves(self, board: List[List[str]], last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[str]]] = None) -> List[str]:
        """
        Возвращает список возможных ходов для слона в текущей позиции.

        :param board: 8x8 матрица, представляющая шахматную доску.
                      Пустые клетки обозначены '',
                      белые фигуры начинаются с 'W', чёрные с 'B'.
        :param last_move: Не используется для слона, добавлен для совместимости.
        :return: Список строк с возможными ходами в формате 'c4', 'd5' и т.д.
        """
        moves = []
        row, col = self.current_square

        # Если фигура связана, она не может двигаться
        if self.is_tied():
            return moves  # Пустой список, так как фигура связана

        # Направления движения слона (диагонали)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board[new_row][new_col]
                if target_piece == '':
                    # Пустая клетка
                    move = self._index_to_notation(new_row, new_col)
                    moves.append(move)
                else:
                    if self._is_opponent_piece(target_piece):
                        # Вражеская фигура может быть взята
                        move = self._index_to_notation(new_row, new_col)
                        moves.append(move)
                    # Если фигура своей, то дальше двигаться нельзя
                    break

                # Продолжаем двигаться в том же направлении
                new_row += dr
                new_col += dc

        return moves

    def move_bishop(self, move: str, board: List[List[str]]) -> bool:
        """
        Выполняет ход слоном, если он допустим.

        :param move: Строка с ходом, например 'c4', 'd5' и т.д.
        :param board: 8x8 матрица, представляющая шахматную доску.
        :return: True если ход выполнен, иначе False
        """
        possible_moves = self.show_possible_moves(board)
        if move not in possible_moves:
            print("Недопустимый ход.")
            return False

        # Преобразование нотации хода в индексы
        try:
            new_row, new_col = self._notation_to_index(move)
        except ValueError as ve:
            print(f"Ошибка формата хода: {ve}")
            return False

        # Проверка, занята ли клетка вражеской фигурой
        target_piece = board[new_row][new_col]
        if target_piece != '':
            if self._is_opponent_piece(target_piece):
                print(f"Вражеская фигура {target_piece} взята.")

        # Перемещаем слона на новую позицию
        self.move((new_row, new_col), board)

        return True

    def _is_opponent_piece(self, piece: str) -> bool:
        """
        Проверяет, является ли фигура противником.
        Наследуется из базового класса Piece.

        :param piece: Строка, представляющая фигуру на доске
        :return: True если фигура противника, иначе False
        """
        return super()._is_opponent_piece(piece)