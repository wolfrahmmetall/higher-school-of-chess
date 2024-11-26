from typing import List
from .pieces.bishop import Bishop
from .pieces.king import King
from .pieces.knight import Knight
from .pieces.pawn import Pawn
from .pieces.piece import Piece
from .pieces.queen import Queen
from .pieces.rook import Rook


class Board:
    def __init__(self) -> None:
        self.board: list[list[Piece | None]] = [[None for _ in range(8)] for _ in range(8)]

    def __getitem__(self, item: List[int]) -> Piece | None:
        return self.board[item[0]][item[1]]

    def __setitem__(self, key: List[int], value: Piece | None) -> None:
        self.board[key[0]][key[1]] = value

    def print_board(self):
        for i in range(8):
            print(8 - i, end='|')
            for j in range(8):
                if j != 7:
                    if self.board[i][j] is None:
                        print('\uA900', end=' ')
                    else:
                        print(self.board[i][j].name(), end=' ')
                else:
                    if self.board[i][j] is None:
                        print('\uA900')
                    else:
                        print(self.board[i][j].name())
            if i == 7:
                letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
                print(' ', end=' ')
                for k in range(8):
                    print(letters[k], end=' ')
                print("\n")

    def start_board(self):
        for i in range(8):
            for j in range(8):
                if i == 1:
                    self.board[i][j] = Pawn('black', (i, j))
                elif i == 6:
                    self.board[i][j] = Pawn('white', (i, j))
                elif i == 7:
                    if j == 0 or j == 7:
                        self.board[i][j] = Rook('white', (i, j))
                    if j == 1 or j == 6:
                        self.board[i][j] = Knight('white', (i, j))
                    if j == 2 or j == 5:
                        self.board[i][j] = Bishop('white', (i, j))
                    if j == 3:
                        self.board[i][j] = Queen('white', (i, j))
                    if j == 4:
                        self.board[i][j] = King('white', (i, j))
                elif i == 0:
                    if j == 0 or j == 7:
                        self.board[i][j] = Rook('black', (i, j))
                    if j == 1 or j == 6:
                        self.board[i][j] = Knight('black', (i, j))
                    if j == 2 or j == 5:
                        self.board[i][j] = Bishop('black', (i, j))
                    if j == 3:
                        self.board[i][j] = Queen('black', (i, j))
                    if j == 4:
                        self.board[i][j] = King('black', (i, j))
