import copy
import unittest
from typing import Optional

from backend.game.pieces.rook import Rook
from backend.game.pieces.pawn import Pawn
from backend.game.pieces.piece import Piece


class TestRook(unittest.TestCase):
    def setUp(self):
        self.board: list[list[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def test_valid_move_to_empty_square(self):
        rook = Rook("white", (4, 4))
        self.board[4][4] = rook

        rook_moves = [
            (1, 0), (2, 0), (3, 0), (-1, 0), (-2, 0), (-3, 0), (-4, 0),  # Vertical moves
            (0, 1), (0, 2), (0, 3), (0, -1), (0, -2), (0, -3), (0, -4)  # Horizontal moves
        ]

        for dr, dc in rook_moves:
            with self.subTest(move=(dr, dc)):
                board_copy = copy.deepcopy(self.board)
                new_position = (4 + dr, 4 + dc)
                self.assertTrue(board_copy[4][4].move(new_position, board_copy))
                self.assertIsNone(board_copy[4][4])
                self.assertIsInstance(board_copy[new_position[0]][new_position[1]], Rook)

    def test_move_to_square_with_enemy(self):
        rook = Rook("white", (4, 4))
        enemy_pawn = Pawn("black", (6, 4))
        self.board[4][4] = rook
        self.board[6][4] = enemy_pawn

        self.assertTrue(rook.move((6, 4), self.board))
        self.assertIsNone(self.board[4][4])
        self.assertIsInstance(self.board[6][4], Rook)

    def test_move_to_square_with_ally(self):
        rook = Rook("white", (4, 4))
        ally_pawn = Pawn("white", (6, 4))
        self.board[4][4] = rook
        self.board[6][4] = ally_pawn

        self.assertFalse(rook.move((6, 4), self.board))
        self.assertIsInstance(self.board[4][4], Rook)
        self.assertIsInstance(self.board[6][4], Pawn)

    def test_invalid_move(self):
        rook = Rook("white", (4, 4))
        self.board[4][4] = rook

        invalid_moves = [
            (5, 5), (3, 3), (6, 6), (4, 4), (2, 3)
        ]

        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(rook.move(move, self.board))
                self.assertIsInstance(self.board[4][4], Rook)

    def test_move_out_of_board(self):
        rook = Rook("white", (0, 0))
        self.board[0][0] = rook

        invalid_moves = [(-1, 0), (0, -1), (-1, -1), (8, 0), (0, 8)]
        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(rook.move(move, self.board))
                self.assertIsInstance(self.board[0][0], Rook)
