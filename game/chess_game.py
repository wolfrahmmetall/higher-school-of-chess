from board import Board
from index_notation import notation_to_index

class ChessGame:
    def __init__(self, game_time, increment) -> None:
        self.white_timer = game_time
        self.black_timer = game_time
        self.increment = increment
        self.turn = "white"
        self.board = Board()

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
                from_square.move(to_position_index, self.board.board)
                if self.turn == "white":
                    self.turn = "black"
                else:
                    self.turn = "white"
            except ValueError as ve:
                print(f"Ошибка формата хода: {ve}")
        self.board.print_board()



        
    

    



