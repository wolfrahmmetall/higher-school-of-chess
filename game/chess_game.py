from typing import Union, Literal, cast

from board import Board
from game.pieces.king import King
from index_notation import notation_to_index

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

    def start_game(self):
        self.board.start_board()
        self.board.print_board()
        while self.result is None:
            print(f"{self.current_player_color}'s turn")
            args = input().split()
            if len(args) != 2:
                if len(args) == 1 and args[0].lower() == "draw":
                    print("Write 'accept' to accept the draw.\n"
                          "Otherwise suggestion will be declined")
                    ans_to_draw = input()
                    if ans_to_draw.lower() == "accept":
                        self.result = "draw"
                else:
                    pass
                    # self.help()
            elif args[0].lower() + " " + args[1].lower() == "give up":
                if self.current_player_color == "white":
                    self.result = "black won"
                else:
                    self.result = "white won"
            else:
                from_position, to_position = args
                self.move(from_position, to_position)

    def move(self, from_position: str, to_position: str):
        try:
            from_position_index = notation_to_index(from_position)
            to_position_index = notation_to_index(to_position)
        except ValueError as ve:
            print(f"Ошибка формата хода: {ve}")
            self.board.print_board()
            return
        from_square = self.board[from_position_index]
        if from_square is None:
            print("Square is empty")
        elif from_square.color != self.current_player_color:
            print("Can not move opponent's piece")
        else:
            to_square = self.board[to_position_index]
            if from_square.move(to_position_index, self.board.board):
                if type(to_square) == King:
                    if self.current_player_color == "white":
                        self.white_king = to_position_index
                    else:
                        self.black_king = to_position_index
                self.invert_current_player_color()
                self.check_game_over()
        self.board.print_board()

    def check_game_over(self):
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
