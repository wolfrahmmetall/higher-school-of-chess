from typing import List, Tuple, Optional
import Piece
import Pawn
import Knight
import Bishop
import Rook
import Queen


class King(Piece):
    def __init__(self, color: str, position: Tuple[int, int]):
        """
        Инициализация короля.

        :param color: 'white' или 'black'
        :param position: Кортеж (row, column) текущей позиции короля (индексация с 0)
        """
        super().__init__(color, position)
        self.has_moved = False  # Флаг, указывающий, ходил ли король

    def name(self) -> str:
        """
        Возвращает обозначение короля.

        :return: 'K' для белого короля, 'k' для чёрного короля.
        """
        return 'K' if self.color == 'white' else 'k'

    def show_possible_moves(self, board: List[List[str]], last_move: Optional[Tuple] = None) -> List[str]:
        """
        Возвращает список возможных ходов для короля в текущей позиции, включая рокировки.

        :param board: 8x8 матрица, представляющая шахматную доску.
                      Пустые клетки обозначены '',
                      белые фигуры начинаются с 'W', чёрные с 'B'.
        :param last_move: Не используется для короля, добавлен для совместимости.
        :return: Список строк с возможными ходами в формате 'e2', 'f1', 'g1' (для рокировки) и т.д.
        """
        moves = []
        row, col = self.current_square
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board[new_row][new_col]
                if target_piece == '' or self._is_opponent_piece(target_piece):
                    # Проверяем, что поле не под атакой
                    if not self.is_square_under_attack(board, new_row, new_col):
                        moves.append(self._index_to_notation(new_row, new_col))

        # Проверка на рокировку
        if not self.has_moved and not self.is_in_check(board):
            # Короткая рокировка (kingside)
            if self.can_castle_short(board):
                moves.append(self._index_to_notation(row, col + 2))
            # Длинная рокировка (queenside)
            if self.can_castle_long(board):
                moves.append(self._index_to_notation(row, col - 2))

        return moves

    def move_king(self, move: str, board: List[List[str]]) -> bool:
        """
        Выполняет ход королём, если он допустим, включая рокировки.

        :param move: Строка с ходом, например 'e2', 'f1', 'g1' (для рокировки) и т.д.
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

        # Проверка на рокировку
        if abs(new_col - self.current_square[1]) == 2:
            # Рокировка
            if new_col > self.current_square[1]:
                # Короткая рокировка
                rook = self.get_rook(board, 'kingside')
                if rook and not rook.has_moved:
                    self.castle(board, rook, 'kingside')
            else:
                # Длинная рокировка
                rook = self.get_rook(board, 'queenside')
                if rook and not rook.has_moved:
                    self.castle(board, rook, 'queenside')

        # Перемещаем короля на новую позицию
        self.move((new_row, new_col), board)
        self.has_moved = True
        return True

    def is_in_check(self, board: List[List[str]]) -> bool:
        """
        Проверяет, находится ли король под шахом.

        :param board: 8x8 матрица, представляющая шахматную доску.
        :return: True если король под шахом, иначе False
        """
        king_row, king_col = self.current_square
        return self.is_square_under_attack(board, king_row, king_col)

    def is_square_under_attack(self, board: List[List[str]], target_row: int, target_col: int) -> bool:
        """
        Проверяет, атакуется ли заданная клетка на доске.

        :param board: 8x8 матрица, представляющая шахматную доску.
        :param target_row: Индекс строки клетки.
        :param target_col: Индекс столбца клетки.
        :return: True если клетка атакуется, иначе False
        """
        for row in range(8):
            for col in range(8):
                piece_str = board[row][col]
                if not piece_str:
                    continue  # Пустая клетка

                piece_color = 'white' if piece_str.startswith('W_') else 'black'
                if piece_color == self.color:
                    continue  # Не проверяем свои фигуры

                piece_type = piece_str[2:].lower()

                # Создаём экземпляр фигуры противника
                if piece_type == 'p':
                    opponent_piece = Pawn(color=piece_color, position=(row, col))
                elif piece_type == 'n':
                    opponent_piece = Knight(color=piece_color, position=(row, col))
                elif piece_type == 'b':
                    opponent_piece = Bishop(color=piece_color, position=(row, col))
                elif piece_type == 'r':
                    opponent_piece = Rook(color=piece_color, position=(row, col))
                elif piece_type == 'q':
                    opponent_piece = Queen(color=piece_color, position=(row, col))
                elif piece_type == 'k':
                    opponent_piece = King(color=piece_color, position=(row, col))
                else:
                    continue  # Неизвестная фигура

                # Получаем возможные ходы фигуры противника
                possible_moves = opponent_piece.show_possible_moves(board)

                # Проверяем, атакует ли фигура короля
                if self._index_to_notation(target_row, target_col) in possible_moves:
                    return True  # Клетка атакуется

        return False  # Клетка не атакуется

    def can_castle_short(self, board: List[List[str]]) -> bool:
        """
        Проверяет, может ли быть выполнена короткая рокировка.

        :param board: 8x8 матрица, представляющая шахматную доску.
        :return: True если короткая рокировка возможна, иначе False
        """
        row, col = self.current_square
        rook_col = 7  # Позиция ладьи для короткой рокировки (h1/h8)
        rook = self.get_rook(board, 'kingside')
        if rook is None or rook.has_moved:
            return False
        # Проверяем, свободны ли поля между королём и ладьёй
        for c in range(col + 1, rook_col):
            if board[row][c] != '':
                return False
        # Проверяем, что поля, через которые проходит король, не под атакой
        for c in range(col, col + 3):
            if self.is_square_under_attack(board, row, c):
                return False
        return True

    def can_castle_long(self, board: List[List[str]]) -> bool:
        """
        Проверяет, может ли быть выполнена длинная рокировка.

        :param board: 8x8 матрица, представляющая шахматную доску.
        :return: True если длинная рокировка возможна, иначе False
        """
        row, col = self.current_square
        rook_col = 0  # Позиция ладьи для длинной рокировки (a1/a8)
        rook = self.get_rook(board, 'queenside')
        if rook is None or rook.has_moved:
            return False
        # Проверяем, свободны ли поля между королём и ладьёй
        for c in range(rook_col + 1, col):
            if board[row][c] != '':
                return False
        # Проверяем, что поля, через которые проходит король, не под атакой
        for c in range(col - 2, col + 1):
            if self.is_square_under_attack(board, row, c):
                return False
        return True

    def get_rook(self, board: List[List[str]], side: str):
        """
        Получает ладью для рокировки.

        :param board: 8x8 матрица, представляющая шахматную доску.
        :param side: 'kingside' или 'queenside'
        :return: Объект ладьи или None
        """
        row, col = self.current_square
        if side == 'kingside':
            rook_col = 7
        elif side == 'queenside':
            rook_col = 0
        else:
            return None
        piece_str = board[row][rook_col]
        if not piece_str:
            return None
        piece_color = 'white' if piece_str.startswith('W_') else 'black'
        if piece_color != self.color:
            return None
        piece_type = piece_str[2:].lower()
        if piece_type != 'r':
            return None
        # Предполагается, что вы храните ссылки на все фигуры
        # Здесь необходимо получить объект ладьи, соответствующий позиции (row, rook_col)
        # Например, через глобальный список или другой механизм хранения фигур
        # Для примера возвращаем None
        return None  # Замените на реальное получение объекта ладьи

    def castle(self, board: List[List[str]], rook: Rook, side: str) -> None:
        """
        Выполняет рокировку, перемещая короля и ладью.

        :param board: 8x8 матрица, представляющая шахматную доску.
        :param rook: Объект ладьи, участвующей в рокировке.
        :param side: 'kingside' или 'queenside'
        """
        row, col = self.current_square
        if side == 'kingside':
            # Перемещаем короля на g1/g8 и ладью на f1/f8
            new_king_col = col + 2
            new_rook_col = col + 1
        elif side == 'queenside':
            # Перемещаем короля на c1/c8 и ладью на d1/d8
            new_king_col = col - 2
            new_rook_col = col - 1
        else:
            return

        # Перемещаем короля
        board[row][col] = ''
        board[row][new_king_col] = ('W_' if self.color == 'white' else 'B_') + self.name()
        self.current_square = (row, new_king_col)
        self.has_moved = True

        # Перемещаем ладью
        rook_move_notation = self._index_to_notation(row, new_rook_col)
        rook.move_rook(rook_move_notation, board)

    def is_in_check(self, board: List[List[str]]) -> bool:
        """
        Проверяет, находится ли король под шахом.

        :param board: 8x8 матрица, представляющая шахматную доску.
        :return: True если король под шахом, иначе False
        """
        return self.is_square_under_attack(board, self.current_square[0], self.current_square[1])