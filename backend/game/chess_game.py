import copy
from typing import Union, Literal, cast

from .board import Board
from .index_notation import index_to_notation, notation_to_index
from .pieces.king import King
from .pieces.pawn import Pawn
from .pieces.piece import Piece
from .pieces.rook import Rook

PieceColor = Union[Literal["white"], Literal["black"]]


class ChessGame:
    def __init__(self, game_time, increment) -> None:
        self.white_timer = game_time
        self.black_timer = game_time
        self.white: int | None = None
        self.black: int | None = None
        self.increment = increment
        self.current_player_color: PieceColor = "white"
        self.board = Board()
        self.white_king = (7, 4)
        self.black_king = (0, 4)
        self.result = None

    def invert_current_player_color(self) -> None:
        self.current_player_color = "black" if self.current_player_color == "white" else "white"

    def start_game(self) -> None:
        self.board.start_board()
        self.board.print_board()

    def get_possible_moves(self, from_position: str) -> list[tuple[int, int]]:
        try:
            from_position_index = notation_to_index(from_position)
        except ValueError as ve:
            print(f"Ошибка формата клетки: {ve}")
            return []
        from_square = self.board[from_position_index]
        if from_square is None:
            return []
        elif from_square.color != self.current_player_color:
            return []
        else:
            uncut_possible_moves = from_square.show_possible_moves(self.board.board)
            possible_moves = []
            for move in uncut_possible_moves:
                # Make a deep copy of the board and game state
                board_copy = copy.deepcopy(self.board)
                white_king_pos = self.white_king
                black_king_pos = self.black_king
                current_player_color = self.current_player_color

                # Simulate the move on the copy
                from_square_copy = board_copy[from_position_index]
                from_square_copy.move(move, board_copy.board)
                if isinstance(from_square_copy, King):
                    if current_player_color == 'white':
                        white_king_pos = move
                    else:
                        black_king_pos = move

                # Now check if the king is in check on the copied board
                if current_player_color == 'white':
                    king_piece = board_copy[white_king_pos]
                    if not king_piece.is_in_check(board_copy.board):
                        possible_moves.append(move)
                else:
                    king_piece = board_copy[black_king_pos]
                    if not king_piece.is_in_check(board_copy.board):
                        possible_moves.append(move)

                # No need to undo the move, since we worked on a copy

            return possible_moves

    def move(self, from_position: str, to_position: str) -> bool:
        previous_player_color = self.current_player_color
        try:
            from_position_index = notation_to_index(from_position)
            to_position_index = notation_to_index(to_position)
        except ValueError as ve:
            print(f"Ошибка формата хода: {ve}")
            self.board.print_board()
            return False
        from_square = self.board[from_position_index]
        if to_position_index not in self.get_possible_moves(from_position):
            print("Impossible move")
            self.board.print_board()
            return False
        from_square.move(to_position_index, self.board.board)
        if isinstance(self.board[to_position_index], King):
            if self.current_player_color == "white":
                self.white_king = to_position_index
            else:
                self.black_king = to_position_index

        # Invert the current player color
        self.invert_current_player_color()
        next_player_color = self.current_player_color
        color_change = f"{previous_player_color}->{next_player_color}"
        print(color_change)

        # Add an extra newline to separate output
        print()

        # Print the board
        self.board.print_board()

        # Check if the game is over after the move
        self.check_game_over()

        return True

    def check_game_over(self) -> bool:
        if self.current_player_color == "white":
            king_pos = self.white_king
        else:
            king_pos = self.black_king
        king_piece = self.board[king_pos]
        # Check if any move is possible for the current player
        has_possible_moves = False
        for i in range(8):
            for j in range(8):
                piece = self.board[i, j]
                if piece is not None and piece.color == self.current_player_color:
                    from_notation = index_to_notation(i, j)
                    if self.get_possible_moves(from_notation):
                        has_possible_moves = True
                        break
            if has_possible_moves:
                break

        if has_possible_moves:
            # The player has possible moves; the game continues
            return False
        else:
            # No possible moves, check if the king is in check
            if isinstance(king_piece, King) and king_piece.is_in_check(self.board.board):
                # King is in check, checkmate
                if self.current_player_color == "white":
                    print("Checkmate! Black wins.")
                    self.result = "Мат. Победа черных!"
                else:
                    print("Checkmate! White wins.")
                    self.result = "Мат. Победа белых!"
            else:
                # King is not in check, stalemate
                print("Stalemate! It's a draw.")
                self.result = "Тупик. Ничья!"
            return True