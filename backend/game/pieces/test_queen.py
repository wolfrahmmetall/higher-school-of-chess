import copy
import unittest
from typing import Optional

from backend.game.pieces.queen import Queen
from backend.game.pieces.pawn import Pawn
from backend.game.pieces.piece import Piece


class TestQueen(unittest.TestCase):
    def setUp(self):
        self.board: list[list[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def test_valid_move_to_empty_square(self):
        queen = Queen("white", (4, 4))
        self.board[4][4] = queen

        queen_moves = [
            (1, 0), (2, 0), (3, 0), (-1, 0), (-2, 0), (-3, 0),  # Vertical moves
            (0, 1), (0, 2), (0, 3), (0, -1), (0, -2), (0, -3),  # Horizontal moves
            (1, 1), (2, 2), (3, 3), (-1, -1), (-2, -2), (-3, -3),  # Diagonal moves
            (1, -1), (2, -2), (3, -3), (-1, 1), (-2, 2), (-3, 3)
        ]

        for dr, dc in queen_moves:
            with self.subTest(move=(dr, dc)):
                board_copy = copy.deepcopy(self.board)
                new_position = (4 + dr, 4 + dc)
                if 0 <= new_position[0] < 8 and 0 <= new_position[1] < 8:
                    self.assertTrue(board_copy[4][4].move(new_position, board_copy))
                    self.assertIsNone(board_copy[4][4])
                    self.assertIsInstance(board_copy[new_position[0]][new_position[1]], Queen)

    def test_move_to_square_with_enemy(self):
        queen = Queen("white", (4, 4))
        enemy_pawn = Pawn("black", (6, 6))
        self.board[4][4] = queen
        self.board[6][6] = enemy_pawn

        self.assertTrue(queen.move((6, 6), self.board))
        self.assertIsNone(self.board[4][4])
        self.assertIsInstance(self.board[6][6], Queen)

    def test_move_to_square_with_ally(self):
        queen = Queen("white", (4, 4))
        ally_pawn = Pawn("white", (6, 6))
        self.board[4][4] = queen
        self.board[6][6] = ally_pawn

        self.assertFalse(queen.move((6, 6), self.board))
        self.assertIsInstance(self.board[4][4], Queen)
        self.assertIsInstance(self.board[6][6], Pawn)

    def test_invalid_move(self):
        queen = Queen("white", (4, 4))
        self.board[4][4] = queen

        invalid_moves = [
            (4, 4), (2, 1), (1, 2), (7, 6), (5, 2)
        ]

        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(queen.move(move, self.board))
                self.assertIsInstance(self.board[4][4], Queen)

    def test_move_out_of_board(self):
        queen = Queen("white", (7, 7))
        self.board[7][7] = queen

        invalid_moves = [(8, 8), (9, 9), (7, 8), (8, 7), (0, 9), (-1, -1), (0, 8)]
        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(queen.move(move, self.board))
                self.assertIsInstance(self.board[7][7], Queen)
