from typing import Union, Literal, cast

from fastapi import HTTPException

from .board import Board
from .index_notation import index_to_notation
from .pieces.king import King
from .pieces.pawn import Pawn
from .pieces.piece import Piece
from .pieces.rook import Rook
from .index_notation import notation_to_index

PieceColor = Union[Literal["white"], Literal["black"]]


class ChessGame:
    def __init__(self, game_time, increment) -> None:
        self.white_timer = game_time
        self.black_timer = game_time
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
                last_move = (from_position_index, move)
                if self.board[move] is not None:
                    enemy_square = self.board[move]
                    if self.current_player_color == "white":
                        color = "black"
                    else:
                        color = "white"

                    if type(enemy_square) == Pawn:
                        enemy_eaten = (Pawn, color, move, cast(Pawn, enemy_square).en_passant_available, cast(Pawn, enemy_square).already_moved)
                    elif type(enemy_square) == Rook:
                        enemy_eaten = (Rook, color, move, cast(Rook, enemy_square).has_moved)
                    else:
                        enemy_eaten = (type(enemy_square), color, move)
                else:
                    enemy_eaten = ()

                from_square.move(move, self.board.board)
                if self.current_player_color == "white":
                    if not cast(King, self.board[self.white_king]).is_in_check(self.board.board):
                        possible_moves.append(move)
                elif not cast(King, self.board[self.black_king]).is_in_check(self.board.board):
                    possible_moves.append(move)

                self.unmove(last_move, enemy_eaten)

            return possible_moves

    def unmove(self, last_move: tuple[tuple[int, int], tuple[int, int]], enemy_eaten: tuple) -> None:
        self.board[last_move[1]].move(last_move[0], self.board.board)
        if len(enemy_eaten) == 0:
            return
        piece_type: Piece = enemy_eaten[0]
        self.board[last_move] = piece_type(enemy_eaten[1], enemy_eaten[2])
        if piece_type == Pawn:
            cast(Pawn, self.board[last_move[1]]).en_passant_available = enemy_eaten[3]
            cast(Pawn, self.board[last_move[1]]).already_moved = enemy_eaten[4]
        elif piece_type == Rook:
            cast(Rook, self.board[last_move[1]]).has_moved = enemy_eaten[3]



    def move(self, from_position: str, to_position: str) -> bool:
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
        else:
            if from_square.move(to_position_index, self.board.board):
                if type(self.board[to_position_index]) == King:
                    if self.current_player_color == "white":
                        self.white_king = to_position_index
                    else:
                        self.black_king = to_position_index
                self.invert_current_player_color()
                self.check_game_over()
        self.board.print_board()
        return True

    def check_game_over(self) -> bool:
        if self.current_player_color == "white":
            i, j = self.white_king
        else:
            i, j = self.black_king
        if self.board[i, j].show_possible_moves(self.board.board):
            return False
        for k in range(8):
            for t in range(8):
                board_k_t = self.board[k, t]
                if board_k_t is not None:
                    if board_k_t.color == self.current_player_color and board_k_t.show_possible_moves(self.board.board):
                        return False

        if cast(King, self.board[i, j]).is_in_check(self.board.board):
            if self.current_player_color == "white":
                self.result = "black won"
            else:
                self.result = "white won"
        else:
            self.result = "draw"
