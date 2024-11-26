import copy
import unittest
from typing import Optional

from backend.game.pieces.bishop import Bishop
from backend.game.pieces.pawn import Pawn
from backend.game.pieces.piece import Piece


class TestBishop(unittest.TestCase):
    def setUp(self):
        self.board: list[list[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def test_valid_move_to_empty_square(self):
        bishop = Bishop("white", (4, 4))
        self.board[4][4] = bishop

        bishop_moves = [
            (1, 1), (2, 2), (3, 3), (-1, -1), (-2, -2), (-3, -3),
            (1, -1), (2, -2), (3, -3), (-1, 1), (-2, 2), (-3, 3)
        ]

        for dr, dc in bishop_moves:
            with self.subTest(move=(dr, dc)):
                board_copy = copy.deepcopy(self.board)
                new_position = (4 + dr, 4 + dc)
                if 0 <= new_position[0] < 8 and 0 <= new_position[1] < 8:
                    self.assertTrue(board_copy[4][4].move(new_position, board_copy))
                    self.assertIsNone(board_copy[4][4])
                    self.assertIsInstance(board_copy[new_position[0]][new_position[1]], Bishop)

    def test_move_to_square_with_enemy(self):
        bishop = Bishop("white", (4, 4))
        enemy_pawn = Pawn("black", (6, 6))
        self.board[4][4] = bishop
        self.board[6][6] = enemy_pawn

        self.assertTrue(bishop.move((6, 6), self.board))
        self.assertIsNone(self.board[4][4])
        self.assertIsInstance(self.board[6][6], Bishop)

    def test_move_to_square_with_ally(self):
        bishop = Bishop("white", (4, 4))
        ally_pawn = Pawn("white", (6, 6))
        self.board[4][4] = bishop
        self.board[6][6] = ally_pawn

        self.assertFalse(bishop.move((6, 6), self.board))
        self.assertIsInstance(self.board[4][4], Bishop)
        self.assertIsInstance(self.board[6][6], Pawn)

    def test_invalid_move(self):
        bishop = Bishop("white", (4, 4))
        self.board[4][4] = bishop

        invalid_moves = [
            (4, 4), (4, 5), (5, 4), (1, 2), (2, 5), (7, 2), (0, 7)
        ]

        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(bishop.move(move, self.board))
                self.assertIsInstance(self.board[4][4], Bishop)

    def test_move_out_of_board(self):
        bishop = Bishop("white", (7, 7))
        self.board[7][7] = bishop

        invalid_moves = [(8, 8), (9, 9), (7, 8), (8, 7), (0, 9), (-1, -1)]
        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(bishop.move(move, self.board))
                self.assertIsInstance(self.board[7][7], Bishop)