from typing import List, Tuple, Optional
from game.pieces.piece import Piece
from game.pieces.queen import Queen
from game.pieces.rook import Rook
from game.pieces.knight import Knight
from game.pieces.bishop import Bishop
from game.index_notation import index_to_notation  # Предполагается, что этот модуль существует


class Pawn(Piece):
    def move(
            self,
            move: Tuple[int, int],
            board: List[List[Optional['Piece']]],
            last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[str]]] = None
    ) -> bool:
        """
        Выполняет ход пешкой, если он допустим, включая взятие на проходе и превращение.

        :param move: Кортеж с ходом в формате (new_row, new_col).
                     Например: (4, 0), (0, 0)
        :param board: 8x8 матрица, представляющая шахматную доску.
        :param last_move: Последний совершённый ход в формате ((from_row, from_col), (to_row, to_col), promotion_piece)
        :return: True если ход выполнен, иначе False
        """
        new_row, new_col = move

        # Если фигура связана, она не может двигаться
        if self.is_tied():
            print("Пешка связана и не может двигаться.")
            return False

        # Получаем список допустимых ходов с учётом последнего хода
        possible_moves = self.show_possible_moves(board, last_move)
        if move not in possible_moves:
            print("Недопустимый ход.")
            return False

        # Определяем направление движения пешки
        direction = -1 if self.color == 'white' else 1

        # Проверка на взятие на проходе
        en_passant = False
        if last_move and self._is_en_passant(move, last_move, board):
            en_passant = True
            captured_row = new_row + direction
            captured_col = new_col
            captured_piece = board[captured_row][captured_col]
            if captured_piece and isinstance(captured_piece, Pawn) and captured_piece.color != self.color:
                board[captured_row][captured_col] = None
                print(f"Пешка на {self.index_to_notation(captured_row, captured_col)} взята на проходе.")
            else:
                print("Ошибка: Нет пешки для взятия на проходе.")
                return False

        # Перемещаем пешку на новую позицию
        board[self.current_square[0]][self.current_square[1]] = None
        target_piece = board[new_row][new_col]

        # Если это обычное взятие
        if target_piece and not en_passant:
            if self._is_opponent_piece(target_piece):
                print(f"Вражеская фигура {target_piece.name()} взята.")
            else:
                # Это условие уже покрыто в show_possible_moves
                pass

        # Превращение пешки, если достигнута последняя горизонталь
        if self._is_promotion(new_row):
            self._promote(board, new_row, new_col)
        else:
            board[new_row][new_col] = self
            self.current_square = (new_row, new_col)
            self.already_moved = True

            # Установка флага en_passant_available, если пешка сделала ход на два поля
            if abs(new_row - self.current_square[0]) == 2:
                self.en_passant_available = True
            else:
                self.en_passant_available = False

        return True

    def _is_en_passant(self, move: Tuple[int, int], last_move: Tuple[Tuple[int, int], Tuple[int, int], Optional[str]],
                       board: List[List['Piece']]) -> bool:
        """
        Проверяет, является ли текущий ход взятием на проходе.

        :param move: Текущий ход в формате (new_row, new_col).
        :param last_move: Последний совершённый ход.
        :param board: Текущая доска.
        :return: True если это взятие на проходе, иначе False.
        """
        new_row, new_col = move
        last_from, last_to, _ = last_move
        last_piece = board[last_to[0]][last_to[1]]

        # Проверяем, что последним ходом был пешка, сделавшая ход на два поля
        if not isinstance(last_piece, Pawn):
            return False
        if abs(last_to[0] - last_from[0]) != 2:
            return False

        # Проверяем, находится ли наша пешка рядом с пешкой, которая сделала двойной ход
        if last_to[0] != self.current_square[0]:
            return False
        if abs(last_to[1] - self.current_square[1]) != 1:
            return False

        # Проверяем, что текущий ход является диагональным
        if abs(new_col - self.current_square[1]) != 1:
            return False
        if new_row - self.current_square[0] != (-1 if self.color == 'white' else 1):
            return False

        return True

    def _is_promotion(self, new_row: int) -> bool:
        """
        Проверяет, должна ли пешка превратиться в другую фигуру.

        :param new_row: Новая строка после хода.
        :return: True если необходимо превращение, иначе False.
        """
        if self.color == 'white' and new_row == 0:
            return True
        if self.color == 'black' and new_row == 7:
            return True
        return False

    def _promote(
        self,
        board: List[List['Piece']],
        new_row: int,
        new_col: int,
        promotion_choice: Optional[str] = 'Q'
    ):
        """
        Превращает пешку в указанную фигуру. Поддерживаются ферзь, ладья, слон и конь.

        :param board: Текущая доска.
        :param new_row: Новая строка после хода.
        :param new_col: Новый столбец после хода.
        :param promotion_choice: Символ новой фигуры ('Q', 'R', 'B', 'N'). По умолчанию 'Q'.
        """
        # Сопоставление символов с классами фигур
        piece_classes = {
            'Q': Queen,
            'R': Rook,
            'B': Bishop,
            'N': Knight
        }

        # Приводим выбор к верхнему регистру для согласованности
        promotion_choice = promotion_choice.upper()

        # Проверяем корректность выбора фигуры
        if promotion_choice not in piece_classes:
            print("Недопустимая фигура для превращения. Превращаемся в ферзя по умолчанию.")
            promotion_choice = 'Q'

        # Создаём новый объект выбранной фигуры
        promoted_piece = piece_classes[promotion_choice](self.color, (new_row, new_col))

        # Размещаем новую фигуру на доске
        board[new_row][new_col] = promoted_piece

        # Удаляем пешку с доски
        board[self.current_square[0]][self.current_square[1]] = None

        print(f"Пешка на {self.index_to_notation(new_row, new_col)} превращена в {promoted_piece.name()}.")

    def show_possible_moves(self, board: List[List['Piece']],
                            last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[str]]] = None) -> List[
        Tuple[int, int]]:
        """
        Возвращает список допустимых ходов для пешки, учитывая текущее состояние доски и последний ход.

        :param board: Текущая доска.
        :param last_move: Последний совершённый ход.
        :return: Список кортежей с допустимыми ходами (new_row, new_col).
        """
        possible_moves = []
        row, col = self.current_square
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        # Обычный ход вперед
        forward_row = row + direction
        if 0 <= forward_row < 8 and board[forward_row][col] is None:
            possible_moves.append((forward_row, col))
            # Двойной ход с начальной позиции
            double_forward_row = row + 2 * direction
            if row == start_row and board[double_forward_row][col] is None:
                possible_moves.append((double_forward_row, col))

        # Взятие по диагонали
        for delta_col in [-1, 1]:
            new_col = col + delta_col
            if 0 <= new_col < 8:
                target_piece = board[forward_row][new_col]
                if target_piece and self._is_opponent_piece(target_piece):
                    possible_moves.append((forward_row, new_col))
                # Взятие на проходе
                if last_move and self._is_en_passant((forward_row, new_col), last_move, board):
                    possible_moves.append((forward_row, new_col))

        return possible_moves

    def _is_opponent_piece(self, piece: 'Piece') -> bool:
        """
        Проверяет, принадлежит ли фигура противнику.

        :param piece: Фигура для проверки.
        :return: True если фигура принадлежит противнику, иначе False.
        """
        return piece.color != self.color

    def is_tied(self) -> bool:
        """
        Проверяет, связана ли фигура и не может ли она двигаться.

        :return: True если фигура связана, иначе False.
        """
        # Реализуйте логику проверки связности фигуры
        return False



