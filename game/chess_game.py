from tkinter.constants import FALSE

from board import Board
from game.pieces.king import King
from index_notation import notation_to_index

class ChessGame:
    def __init__(self, game_time, increment) -> None:
        self.white_timer = game_time
        self.black_timer = game_time
        self.increment = increment
        self.turn = "white"
        self.board = Board()
        self.white_king = (7, 4)
        self.black_king = (0, 4)
        self.result = None

    def start_game(self):
        self.board.start_board()
        self.board.print_board()

    def move(self, from_position: str, to_position: str):
        i, j = notation_to_index(from_position)
        from_square = self.board.board[i][j]
        if from_square is None:
            print("Square is empty")
        elif from_square.color != self.turn:
            print("Can not move opponent's piece")
        else:
            try:
                to_position_index = tuple(notation_to_index(to_position))
                to_square = self.board.board[to_position_index[0]][to_position_index[1]]
                if from_square.move(to_position_index, self.board.board):
                    if type(to_square) == King:
                        if self.turn == "white":
                            self.white_king = to_position_index
                        else:
                            self.black_king = to_position_index
                    if self.turn == "white":
                        self.turn = "black"
                        # self.game_over("black")
                    else:
                        self.turn = "white"
                        # self.game_over("white")
            except ValueError as ve:
                print(f"Ошибка формата хода: {ve}")
        self.board.print_board()

    def game_over(self, color: str):
        if color == "white":
            i, j = self.white_king
        else:
            i, j = self.black_king
        if not self.board.board[i][j].show_possible_moves().empty():
            return False
        for k in range(8):
            for t in range(8):
                board_k_t = self.board.board[k][t]
                if board_k_t is not None:
                    if board_k_t.color == color and not board_k_t.show_possible_moves().empty():
                        return False

        if self.board.board[i][j].is_in_check():
            if color == "white":
                self.result = "black"
            else:
                self.result = "white"
        else:
            self.result = "draw"

a = ChessGame(1, 1)
a.start_game()
a.move("b2", "b3")
        
    

    



