from typing import List, Tuple, Optional
from .piece import Piece
from .queen import Queen
from .rook import Rook
from .knight import Knight
from .bishop import Bishop


class Pawn(Piece):
    def __init__(self, color: str, position: Tuple[int, int]):
        super().__init__(color, position)
        self.can_be_captured_en_passant = False
        self.already_moved = False

    def name(self) -> str:
        return 'P' if self.color == 'white' else 'p'

    def move(
        self,
        move: Tuple[int, int],
        board: List[List[Optional['Piece']]]
    ) -> bool:
        new_row, new_col = move
        old_row, old_col = self.current_square

        # If the piece is tied (pinned), it cannot move
        if self.is_tied():
            return False

        # Get the list of possible moves
        possible_moves = self.show_possible_moves(board)
        if move not in possible_moves:
            return False

        # Determine the direction of movement
        direction = -1 if self.color == 'white' else 1

        # Determine if this is an en passant capture
        is_en_passant = False
        if new_col != old_col and board[new_row][new_col] is None:
            # En passant capture
            captured_row = old_row
            captured_col = new_col
            captured_piece = board[captured_row][captured_col]
            if (captured_piece and
                isinstance(captured_piece, Pawn) and
                self._is_opponent_piece(captured_piece) and
                captured_piece.can_be_captured_en_passant):
                board[captured_row][captured_col] = None
                is_en_passant = True
            else:
                print("Ошибка: Нет пешки для взятия на проходе.")
                return False

        # Move the pawn
        board[old_row][old_col] = None
        board[new_row][new_col] = self
        self.current_square = (new_row, new_col)
        self.already_moved = True

        # Reset en passant flags for all pawns
        for row_pieces in board:
            for piece in row_pieces:
                if isinstance(piece, Pawn):
                    piece.can_be_captured_en_passant = False

        # If the pawn moved two squares forward, set can_be_captured_en_passant to True
        if abs(new_row - old_row) == 2:
            self.can_be_captured_en_passant = True

        return True

    def show_possible_moves(
        self,
        board: List[List[Optional['Piece']]]
    ) -> List[Tuple[int, int]]:
        possible_moves = []
        row, col = self.current_square
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        # One square forward
        forward_row = row + direction
        if 0 <= forward_row < 8 and board[forward_row][col] is None:
            possible_moves.append((forward_row, col))

            # Two squares forward from starting position
            if row == start_row:
                double_forward_row = row + 2 * direction
                if board[double_forward_row][col] is None:
                    possible_moves.append((double_forward_row, col))

        # Captures
        for delta_col in [-1, 1]:
            new_col = col + delta_col
            if 0 <= new_col < 8:
                target_row = row + direction
                if 0 <= target_row < 8:
                    target_piece = board[target_row][new_col]
                    if target_piece and self._is_opponent_piece(target_piece):
                        possible_moves.append((target_row, new_col))
                    else:
                        # En passant capture
                        adjacent_piece = board[row][new_col]
                        if (adjacent_piece and
                            isinstance(adjacent_piece, Pawn) and
                            self._is_opponent_piece(adjacent_piece) and
                            adjacent_piece.can_be_captured_en_passant):
                            possible_moves.append((target_row, new_col))

        return possible_moves

    def _is_opponent_piece(self, piece: 'Piece') -> bool:
        return piece.color != self.color

    def is_tied(self) -> bool:
        # Implement logic to check if the piece is pinned (currently not implemented)
        return False
