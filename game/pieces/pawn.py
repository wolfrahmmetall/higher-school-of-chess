from typing import List, Tuple, Optional
from game.pieces.piece import Piece
from game.index_notation import index_to_notation  # Предполагается, что этот модуль существует

class Pawn(Piece):
    def __init__(self, color: str, position: Tuple[int, int]):
        """
        Инициализация пешки.

        :param color: 'white' или 'black'
        :param position: Кортеж (row, column) текущей позиции пешки (индексация с 0)
        """
        super().__init__(color, position)
        self.already_moved = False
        self.en_passant_available = False  # Флаг, указывающий, может ли пешка быть взятой на проходе

    def name(self) -> str:
        """
        Возвращает обозначение пешки.

        :return: 'P' для белой пешки, 'p' для чёрной пешки.
        """
        return 'P' if self.color == 'white' else 'p'

    def show_possible_moves(
        self,
        board: List[List[Optional[Piece]]],
        last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[str]]] = None
    ) -> List[str]:
        """
        Возвращает список возможных ходов для пешки в текущей позиции, включая взятие на проходе и превращение.

        :param board: 8x8 матрица, представляющая шахматную доску.
                      Пустые клетки обозначены None,
                      фигуры представлены объектами наследниками класса Piece.
        :param last_move: Последний совершённый ход в формате ((from_row, from_col), (to_row, to_col), promotion_piece)
        :return: Список строк с возможными ходами в формате 'a4', 'b5Q' и т.д.
        """
        moves = []
        row, col = self.current_square

        # Если фигура связана, она не может двигаться
        if self.is_tied():
            return moves  # Пустой список, так как фигура связана

        # Определяем направление движения пешки
        direction = -1 if self.color == 'white' else 1
        promotion_row = 0 if self.color == 'white' else 7

        # Один шаг вперед
        next_row = row + direction
        if 0 <= next_row < 8:
            if board[next_row][col] is None:
                if next_row == promotion_row:
                    for promo in ['Q', 'R', 'B', 'N']:
                        move = self._index_to_notation(next_row, col) + promo
                        moves.append(move)
                else:
                    move = self._index_to_notation(next_row, col)
                    moves.append(move)

                # Два шага вперед с начальной позиции
                starting_row = 6 if self.color == 'white' else 1
                if not self.already_moved and row == starting_row:
                    next_row_two = row + 2 * direction
                    if board[next_row_two][col] is None:
                        move = self._index_to_notation(next_row_two, col)
                        moves.append(move)

        # Взятие по диагонали влево
        if col - 1 >= 0 and 0 <= next_row < 8:
            target_piece = board[next_row][col - 1]
            if target_piece is not None and self._is_opponent_piece(target_piece):
                if next_row == promotion_row:
                    for promo in ['Q', 'R', 'B', 'N']:
                        move = self._index_to_notation(next_row, col - 1) + promo
                        moves.append(move)
                else:
                    move = self._index_to_notation(next_row, col - 1)
                    moves.append(move)

        # Взятие по диагонали вправо
        if col + 1 < 8 and 0 <= next_row < 8:
            target_piece = board[next_row][col + 1]
            if target_piece is not None and self._is_opponent_piece(target_piece):
                if next_row == promotion_row:
                    for promo in ['Q', 'R', 'B', 'N']:
                        move = self._index_to_notation(next_row, col + 1) + promo
                        moves.append(move)
                else:
                    move = self._index_to_notation(next_row, col + 1)
                    moves.append(move)

        # Взятие на проходе (en passant)
        if last_move:
            ((from_row, from_col), (to_row, to_col), promotion_piece) = last_move
            moved_piece = board[to_row][to_col]
            # Проверяем, что последний ход был пешкой противника, которая переместилась на два поля
            if self.color == 'white':
                opponent_color = 'black'
                en_passant_row = 3  # Белая пешка может взять на проходе, если чёрная пешка находится на 5-й линии (индекс 3)
                capture_row = to_row
                direction_e_p = -1
            else:
                opponent_color = 'white'
                en_passant_row = 4  # Чёрная пешка может взять на проходе, если белая пешка находится на 4-й линии (индекс 4)
                capture_row = to_row
                direction_e_p = 1

            if (
                moved_piece is not None
                and isinstance(moved_piece, Pawn)
                and moved_piece.color == opponent_color
                and abs(to_row - from_row) == 2
                and to_row == en_passant_row
                and row == en_passant_row + direction_e_p
                and abs(to_col - col) == 1
            ):
                target_col = to_col
                target_move_notation = self._index_to_notation(row + direction_e_p, target_col) + 'e.p.'
                moves.append(target_move_notation)

        return moves

    def move_piece(
        self,
        move: str,
        board: List[List[Optional[Piece]]],
        last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[str]]] = None
    ) -> bool:
        """
        Выполняет ход пешкой, если он допустим, включая взятие на проходе и превращение.

        :param move: Строка с ходом, например 'a4', 'b5Q' или 'd6e.p.' для взятия на проходе
        :param board: 8x8 матрица, представляющая шахматную доску.
        :param last_move: Последний совершённый ход в формате ((from_row, from_col), (to_row, to_col), promotion_piece)
        :return: True если ход выполнен, иначе False
        """
        # Если фигура связана, она не может двигаться
        if self.is_tied():
            print("Пешка связана и не может двигаться.")
            return False

        possible_moves = self.show_possible_moves(board, last_move)
        if move not in possible_moves:
            print("Недопустимый ход.")
            return False

        # Обработка взятия на проходе
        if move.endswith('e.p.'):
            # Взятие на проходе
            target_notation = move[:-4]  # Убираем 'e.p.'
            new_row, new_col = self._notation_to_index(target_notation)

            # Определяем позицию взятой пешки
            if self.color == 'white':
                captured_row = new_row + 1
            else:
                captured_row = new_row - 1
            captured_col = new_col

            # Удаляем взятую пешку
            captured_piece = board[captured_row][captured_col]
            board[captured_row][captured_col] = None

            # Перемещаем пешку на новую позицию
            board[self.current_square[0]][self.current_square[1]] = None
            board[new_row][new_col] = self
            self.current_square = (new_row, new_col)
            self.already_moved = True

            print(f"Пешка перемещена на {index_to_notation(new_row, new_col)} и взята на проходе.")
            return True

        # Обработка превращения, если необходимо
        promotion = None
        if len(move) == 3:
            promotion = move[2].upper()
            if promotion not in ['Q', 'R', 'B', 'N']:
                print("Недопустимая фигура для превращения.")
                return False

        # Преобразование нотации хода в индексы
        try:
            new_row, new_col = self._notation_to_index(move[:2])
        except ValueError as ve:
            print(f"Ошибка формата хода: {ve}")
            return False

        target_piece = board[new_row][new_col]

        # Перемещение пешки на новую позицию
        board[self.current_square[0]][self.current_square[1]] = None
        board[new_row][new_col] = self
        self.current_square = (new_row, new_col)
        self.already_moved = True

        # Обработка взятия
        if target_piece is not None:
            if self._is_opponent_piece(target_piece):
                print(f"Вражеская фигура {target_piece.name()} взята.")

        # Обработка превращения, если необходимо
        if promotion:
            promoted_piece_class = {
                'Q': Queen,
                'R': Rook,
                'B': Bishop,
                'N': Knight
            }.get(promotion)
            if promoted_piece_class:
                promoted_piece = promoted_piece_class(self.color, (new_row, new_col))
                board[new_row][new_col] = promoted_piece
                print(f"Пешка превращена в {promoted_piece.name()}.")
            else:
                print("Неизвестная фигура для превращения.")
                return False

        # Если пешка перемещается на два поля, устанавливаем флаг en_passant_available
        if abs(new_row - (new_row - self.already_moved * (2 * (-1 if self.color == 'white' else 1)))) == 2:
            self.en_passant_available = True
        else:
            self.en_passant_available = False

        return True



