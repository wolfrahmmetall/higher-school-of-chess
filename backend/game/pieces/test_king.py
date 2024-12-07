import copy
import unittest
from typing import Optional

from backend.game.pieces.king import King
from backend.game.pieces.knight import Knight
from backend.game.pieces.pawn import Pawn
from backend.game.pieces.piece import Piece
from backend.game.pieces.rook import Rook


class TestKing(unittest.TestCase):
    def setUp(self):
        self.board: list[list[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def test_valid_move_to_empty_square(self):
        king = King("white", (4, 4))
        self.board[4][4] = king

        king_moves = [
            (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]

        for dr, dc in king_moves:
            with self.subTest(move=(dr, dc)):
                board_copy = copy.deepcopy(self.board)
                new_position = (4 + dr, 4 + dc)
                self.assertTrue(board_copy[4][4].move(new_position, board_copy))
                self.assertIsNone(board_copy[4][4])
                self.assertIsInstance(board_copy[new_position[0]][new_position[1]], King)

    def test_move_to_square_with_enemy(self):
        king = King("white", (4, 4))
        enemy_pawn = Pawn("black", (4, 5))
        self.board[4][4] = king
        self.board[4][5] = enemy_pawn

        self.assertTrue(king.move((4, 5), self.board))
        self.assertIsNone(self.board[4][4])
        self.assertIsInstance(self.board[4][5], King)

    def test_move_to_square_with_ally(self):
        king = King("white", (4, 4))
        ally_pawn = Pawn("white", (5, 5))
        self.board[4][4] = king
        self.board[5][5] = ally_pawn

        self.assertFalse(king.move((5, 5), self.board))
        self.assertIsInstance(self.board[4][4], King)
        self.assertIsInstance(self.board[5][5], Pawn)

    def test_invalid_move(self):
        king = King("white", (4, 4))
        self.board[4][4] = king

        invalid_moves = [
            (6, 6), (4, 4), (2, 2), (6, 4), (4, 6)
        ]

        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(king.move(move, self.board))
                self.assertIsInstance(self.board[4][4], King)

    def test_move_out_of_board(self):
        king = King("white", (0, 0))
        self.board[0][0] = king

        invalid_moves = [(-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]
        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(king.move(move, self.board))
                self.assertIsInstance(self.board[0][0], King)

    def test_short_castling(self):
        king = King("white", (7, 4))
        rook = Rook("white", (7, 7))
        self.board[7][4] = king
        self.board[7][7] = rook

        self.assertTrue(king.move((7, 6), self.board))
        self.assertIsInstance(self.board[7][6], King)
        self.assertIsInstance(self.board[7][5], Rook)

    def test_long_castling(self):
        king = King("white", (7, 4))
        rook = Rook("white", (7, 0))
        self.board[7][4] = king
        self.board[7][0] = rook

        self.assertTrue(king.move((7, 2), self.board))
        self.assertIsInstance(self.board[7][2], King)
        self.assertIsInstance(self.board[7][3], Rook)

    def test_invalid_castling_king_moved(self):
        king = King("white", (7, 4))
        rook_short = Rook("white", (7, 7))
        rook_long = Rook("white", (7, 0))
        self.board[7][4] = king
        self.board[7][7] = rook_short
        self.board[7][0] = rook_long

        king.move((7, 3), self.board)
        king.move((7, 4), self.board)

        self.assertFalse(king.move((7, 6), self.board))
        self.assertFalse(king.move((7, 2), self.board))
        self.assertIsInstance(self.board[7][4], King)
        self.assertIsInstance(self.board[7][7], Rook)
        self.assertIsInstance(self.board[7][0], Rook)
        self.assertIsNone(self.board[7][6])
        self.assertIsNone(self.board[7][2])

    def test_invalid_castling_rook_moved(self):
        king = King("white", (7, 4))
        rook = Rook("white", (7, 7))
        self.board[7][4] = king
        self.board[7][7] = rook
        rook.move((6, 7), self.board)
        rook.move((7, 7), self.board)

        self.assertFalse(king.move((7, 6), self.board))
        self.assertIsNone(self.board[7][6])

    def test_invalid_castling_piece_between_v1(self):
        king = King("white", (7, 4))
        rook = Rook("white", (7, 7))
        knight = Knight("white", (7, 6))
        self.board[7][4] = king
        self.board[7][7] = rook
        self.board[7][6] = knight

        self.assertFalse(king.move((7, 6), self.board))
        self.assertIsInstance(self.board[7][6], Knight)

    def test_invalid_castling_piece_between_v2(self):
        king = King("white", (7, 4))
        rook = Rook("white", (7, 0))
        knight = Knight("white", (7, 1))
        self.board[7][4] = king
        self.board[7][0] = rook
        self.board[7][1] = knight

        self.assertFalse(king.move((7, 2), self.board))
        self.assertIsInstance(self.board[7][1], Knight)
        self.assertIsNone(self.board[7][2])

    def test_invalid_castling_king_jumps_under_attacked_square(self):
        king = King("white", (7, 4))
        rook_ally = Rook("white", (7, 0))
        rook_enemy = Rook("black", (0, 3))
        self.board[7][4] = king
        self.board[7][0] = rook_ally
        self.board[0][3] = rook_enemy

        self.assertFalse(king.move((7, 2), self.board))

    def test_invalid_castling_king_will_be_in_check(self):
        king = King("white", (7, 4))
        rook_ally = Rook("white", (7, 0))
        rook_enemy = Rook("black", (0, 2))
        self.board[7][4] = king
        self.board[7][0] = rook_ally
        self.board[0][2] = rook_enemy

        self.assertFalse(king.move((7, 2), self.board))

    def test_invalid_castling_king_in_check(self):
        king = King("white", (7, 4))
        rook_ally = Rook("white", (7, 0))
        rook_enemy = Rook("black", (0, 4))
        self.board[7][4] = king
        self.board[7][0] = rook_ally
        self.board[0][4] = rook_enemy

        self.assertFalse(king.move((7, 2), self.board))