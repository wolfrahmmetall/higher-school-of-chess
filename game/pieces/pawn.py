from typing import List, Tuple, Optional
from game.pieces.piece import Piece
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

    def has_already_moved(self) -> bool:
        """
        Проверяет, была ли пешка уже перемещена.

        :return: True если перемещена, иначе False
        """
        return self.already_moved

    def show_possible_moves(self, board: List[List[str]], last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[str]]] = None) -> List[str]:
        """
        Возвращает список возможных ходов для пешки в текущей позиции, включая взятие на проходе.

        :param board: 8x8 матрица, представляющая шахматную доску.
                      Пустые клетки обозначены '',
                      белые фигуры начинаются с 'W', чёрные с 'B'.
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
            if board[next_row][col] == '':
                if next_row == promotion_row:
                    for promo in ['Q', 'R', 'B', 'N']:
                        move = self._index_to_notation(next_row, col) + promo
                        moves.append(move)
                else:
                    move = self._index_to_notation(next_row, col)
                    moves.append(move)

                # Два шага вперед с начальной позиции
                if not self.already_moved:
                    next_row_two = row + 2 * direction
                    if board[next_row_two][col] == '':
                        move = self._index_to_notation(next_row_two, col)
                        moves.append(move)

        # Взятие по диагонали влево
        if col - 1 >= 0 and 0 <= next_row < 8:
            target_piece = board[next_row][col - 1]
            if self._is_opponent_piece(target_piece):
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
            if self._is_opponent_piece(target_piece):
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
                opponent_pawn = 'B_P'
                en_passant_row = 3  # Белая пешка может взять на проходе, если чёрная пешка находится на 5-й линии (индекс 3)
                capture_row = to_row
                direction = -1
            else:
                opponent_color = 'white'
                opponent_pawn = 'W_P'
                en_passant_row = 4  # Чёрная пешка может взять на проходе, если белая пешка находится на 4-й линии (индекс 4)
                capture_row = to_row
                direction = 1

            if moved_piece.startswith(opponent_pawn) and abs(to_row - from_row) == 2 and to_row == en_passant_row:
                # Проверяем, находится ли пешка рядом с текущей пешкой
                if row == en_passant_row and abs(to_col - col) == 1:
                    capture_col = to_col
                    capture_position = (capture_row, capture_col)
                    # Определяем позицию, куда переместится текущая пешка
                    target_capture_row = row + direction
                    target_capture_col = capture_col
                    move = self._index_to_notation(target_capture_row, target_capture_col) + 'e.p.'
                    moves.append(move)

        return moves

    def move_pawn(self, move: str, board: List[List[str]], last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[str]]] = None) -> bool:
        """
        Выполняет ход пешки, если он допустим, включая взятие на проходе.

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
            board[captured_row][captured_col] = ''

            # Перемещаем пешку на новую позицию
            self.move((new_row, new_col), board)

        else:
            # Обработка превращения, если необходимо
            promotion = None
            if len(move) == 3:
                promotion = move[2].upper()
                if promotion not in ['Q', 'R', 'B', 'N']:
                    print("Недопустимая фигура для превращения.")
                    return False

            # Преобразование нотации хода в индексы
            new_row, new_col = self._notation_to_index(move[:2])

            # Перемещаем пешку на новую позицию
            self.move((new_row, new_col), board)

            # Обработка превращения, если необходимо
            if promotion:
                board[new_row][new_col] = ('W_' if self.color == 'white' else 'B_') + promotion

            # Если пешка перемещается на два поля, устанавливаем флаг en_passant_available
            if abs(new_row - self.current_square[0]) == 2:
                self.en_passant_available = True
            else:
                self.en_passant_available = False

        # Обновляем флаг уже перемещена
        self.already_moved = True

        return True

    def en_passant(self, board: List[List[str]], last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[str]]] = None) -> bool:
        """
        Выполняет взятие на проходе, если оно возможно.

        :param board: 8x8 матрица, представляющая шахматную доску.
        :param last_move: Последний совершённый ход в формате ((from_row, from_col), (to_row, to_col), promotion_piece)
        :return: True если взятие выполнено, иначе False
        """
        # Проверяем, может ли быть выполнено взятие на проходе
        possible_moves = self.show_possible_moves(board, last_move)
        for move in possible_moves:
            if move.endswith('e.p.'):
                return self.move_pawn(move, board, last_move)
        print("Взятие на проходе невозможно.")
        return False
    def _is_opponent_piece(self, piece: str) -> bool:
        """
        Проверяет, является ли фигура противником.
        Наследуется из базового класса Piece.

        :param piece: Строка, представляющая фигуру на доске
        :return: True если фигура противника, иначе False
        """
        return super()._is_opponent_piece(piece)


