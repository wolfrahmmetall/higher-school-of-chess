import copy
import unittest
from typing import Optional

from backend.game.pieces.knight import Knight
from backend.game.pieces.pawn import Pawn
from backend.game.pieces.piece import Piece


class TestKnight(unittest.TestCase):
    def setUp(self):
        self.board: list[list[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def test_valid_move_to_empty_square(self):
        knight = Knight("white", (4, 4))
        self.board[4][4] = knight

        knight_moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

        for dr, dc in knight_moves:
            with self.subTest(move=(dr, dc)):
                board_copy = copy.deepcopy(self.board)
                new_position = (4 + dr, 4 + dc)
                self.assertTrue(board_copy[4][4].move(new_position, board_copy))
                self.assertIsNone(board_copy[4][4])
                self.assertIsInstance(board_copy[new_position[0]][new_position[1]], Knight)

    def test_move_to_square_with_enemy(self):
        knight = Knight("white", (4, 4))
        enemy_pawn = Pawn("black", (5, 6))
        self.board[4][4] = knight
        self.board[5][6] = enemy_pawn

        self.assertTrue(knight.move((5, 6), self.board))
        self.assertIsNone(self.board[4][4])
        self.assertIsInstance(self.board[5][6], Knight)

    def test_move_to_square_with_ally(self):
        knight = Knight("white", (4, 4))
        ally_pawn = Pawn("white", (5, 6))
        self.board[4][4] = knight
        self.board[5][6] = ally_pawn

        self.assertFalse(knight.move((5, 6), self.board))
        self.assertIsInstance(self.board[4][4], Knight)
        self.assertIsInstance(self.board[5][6], Pawn)

    def test_invalid_move(self):
        knight = Knight("white", (4, 4))
        self.board[4][4] = knight

        invalid_moves = [(4, 4), (4, 6), (4, 3), (5, 5), (7, 2), (0, 0)]
        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(knight.move(move, self.board))
                self.assertIsInstance(self.board[4][4], Knight)

    def test_move_out_of_board(self):
        knight = Knight("white", (1, 1))
        self.board[1][1] = knight

        invalid_moves = [(-1, 0), (0, -1), (-1, -1)]
        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(knight.move(move, self.board))
                self.assertIsInstance(self.board[1][1], Knight)