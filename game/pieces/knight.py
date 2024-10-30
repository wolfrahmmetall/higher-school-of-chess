from typing import List, Tuple, Optional
from game.pieces.piece import Piece

class Knight(Piece):
    def __init__(self, color: str, position: Tuple[int, int]):
        """
        Инициализация коня.

        :param color: 'white' или 'black'
        :param position: Кортеж (row, column) текущей позиции коня (индексация с 0)
        """
        super().__init__(color, position)

    def name(self) -> str:
        """
        Возвращает обозначение пешки.

        :return: 'P' для белой пешки, 'p' для чёрной пешки.
        """
        return 'N' if self.color == 'white' else 'n'

    def show_possible_moves(self, board: List[List[str]], last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[str]]] = None) -> List[str]:
        """
        Возвращает список возможных ходов для коня в текущей позиции.

        :param board: 8x8 матрица, представляющая шахматную доску.
                      Пустые клетки обозначены '',
                      белые фигуры начинаются с 'W', чёрные с 'B'.
        :param last_move: Не используется для коня, добавлен для совместимости.
        :return: Список строк с возможными ходами в формате 'f3', 'g5' и т.д.
        """
        moves = []
        row, col = self.current_square

        # Если фигура связана, она не может двигаться
        if self.is_tied():
            return moves  # Пустой список, так как фигура связана

        # Все возможные "г"-образные ходы коня
        knight_moves = [
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1)
        ]

        for dr, dc in knight_moves:
            new_row = row + dr
            new_col = col + dc

            # Проверяем, находится ли новая позиция на доске
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board[new_row][new_col]
                if target_piece == '':
                    # Пустая клетка
                    move = self._index_to_notation(new_row, new_col)
                    moves.append(move)
                else:
                    # Проверяем, принадлежит ли фигура противнику
                    if self._is_opponent_piece(target_piece):
                        move = self._index_to_notation(new_row, new_col)
                        moves.append(move)
                    # Если фигура своей, ход невозможен

        return moves

    def move(self, move: str, board: List[List[str]]) -> bool:
        """
        Выполняет ход конем, если он допустим.

        :param move: Строка с ходом, например 'f3', 'g5' и т.д.
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
            else:
                # Это условие уже покрыто в show_possible_moves
                pass

        # Перемещаем коня на новую позицию
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




