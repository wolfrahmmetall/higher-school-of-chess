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
        """
        Returns the representation of the pawn.

        :return: 'P' for white pawn, 'p' for black pawn.
        """
        return 'P' if self.color == 'white' else 'p'

    def move(
        self,
        move: Tuple[int, int],
        board: List[List[Optional['Piece']]]
    ) -> bool:
        """
        Executes a pawn move if it's valid, including en passant and promotion.

        :param move: Tuple with the move in format (new_row, new_col).
        :param board: 8x8 matrix representing the chessboard.
        :return: True if the move was made, else False.
        """
        new_row, new_col = move
        old_row, old_col = self.current_square

        # If the piece is pinned, it cannot move
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
                print("Error: No pawn to capture en passant.")
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

        # Check for promotion
        if self._is_promotion(new_row):
            self._promote(board, new_row, new_col)

        return True

    def _is_promotion(self, new_row: int) -> bool:
        """
        Checks if the pawn should be promoted.

        :param new_row: The new row after the move.
        :return: True if promotion is needed, else False.
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
            new_col: int
    ):
        """
        Promotes the pawn to the chosen piece. Supports Queen, Rook, Bishop, and Knight.

        :param board: The current board.
        :param new_row: The new row after the move.
        :param new_col: The new column after the move.
        """
        # Mapping symbols to piece classes
        piece_classes = {
            'Q': Queen,
            'R': Rook,
            'B': Bishop,
            'N': Knight
        }

        # Prompt the user for promotion choice
        while True:
            promotion_choice = input("Choose promotion piece (Q, R, B, N): ").upper()
            if promotion_choice in piece_classes:
                break
            else:
                print("Invalid choice. Please try again.")

        # Create a new object of the chosen piece
        promoted_piece = piece_classes[promotion_choice](self.color, (new_row, new_col))

        # Place the new piece on the board
        board[new_row][new_col] = promoted_piece

        # The pawn is already removed from the old position in the move method

    def show_possible_moves(
        self,
        board: List[List[Optional['Piece']]]
    ) -> List[Tuple[int, int]]:
        """
        Returns a list of valid moves for the pawn, considering the current board state.

        :param board: The current board.
        :return: List of tuples with valid moves (new_row, new_col).
        """
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
        """
        Checks if the piece belongs to the opponent.

        :param piece: The piece to check.
        :return: True if the piece belongs to the opponent, else False.
        """
        return piece.color != self.color

    def is_tied(self) -> bool:
        """
        Checks if the piece is pinned and cannot move.

        :return: True if the piece is pinned, else False.
        """
        # Implement the logic to check if the piece is pinned
        return False