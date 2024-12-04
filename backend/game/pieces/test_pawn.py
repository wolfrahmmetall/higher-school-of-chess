import copy
import unittest
import pytest
from unittest import mock
from typing import Optional

from backend.game.pieces.bishop import Bishop
from backend.game.pieces.knight import Knight
from backend.game.pieces.pawn import Pawn
from backend.game.pieces.piece import Piece
from backend.game.pieces.queen import Queen
from backend.game.pieces.rook import Rook


class TestPawn(unittest.TestCase):
    def setUp(self):
        self.board: list[list[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def test_valid_start_move_black(self):
        pawn = Pawn("black", (1, 1))
        self.board[1][1] = pawn

        valid_moves = [(2, 1), (3, 1)]

        for move in valid_moves:
            with self.subTest(move=move):
                board_copy = copy.deepcopy(self.board)
                self.assertTrue(board_copy[1][1].move(move, board_copy))
                self.assertIsNone(board_copy[1][1])
                self.assertIsInstance(board_copy[move[0]][move[1]], Pawn)

    def test_valid_start_move_white(self):
        pawn = Pawn("white", (6, 6))
        self.board[6][6] = pawn

        valid_moves = [(5, 6), (4, 6)]

        for move in valid_moves:
            with self.subTest(move=move):
                board_copy = copy.deepcopy(self.board)
                self.assertTrue(board_copy[6][6].move(move, board_copy))
                self.assertIsNone(board_copy[6][6])
                self.assertIsInstance(board_copy[move[0]][move[1]], Pawn)


    def test_invalid_move_forward_two_squares_after_first_move(self):
        pawn = Pawn("white", (6, 6))
        self.board[6][6] = pawn
        pawn.move((5, 6), self.board)

        invalid_moves = [(3, 6)]

        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(pawn.move(move, self.board))
                self.assertIsInstance(self.board[5][6], Pawn)

    def test_capture_move(self):
        pawn = Pawn("white", (4, 4))
        enemy_pawn = Pawn("black", (3, 3))
        self.board[4][4] = pawn
        self.board[3][3] = enemy_pawn

        valid_capture_moves = [(3, 3)]

        for move in valid_capture_moves:
            with self.subTest(move=move):
                self.assertTrue(pawn.move(move, self.board))
                self.assertIsNone(self.board[4][4])
                self.assertIsInstance(self.board[3][3], Pawn)
                self.assertTrue(self.board[3][3].color.lower() == "white")

    def test_invalid_capture_move(self):
        pawn = Pawn("white", (3, 3))
        enemy_pawn = Pawn("black", (2, 3))
        self.board[3][3] = pawn
        self.board[2][3] = enemy_pawn

        invalid_moves = [(2, 2), (2, 4), (2, 3)]

        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(pawn.move(move, self.board))
                self.assertIsInstance(self.board[3][3], Pawn)

    def test_move_out_of_board(self):
        pawn = Pawn("white", (7, 7))
        self.board[7][7] = pawn

        invalid_moves = [(8, 7), (7, 8), (9, 9), (7, 6)]
        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(pawn.move(move, self.board))
                self.assertIsInstance(self.board[7][7], Pawn)

    def test_move_backwards(self):
        pawn = Pawn("white", (4, 4))
        self.board[4][4] = pawn

        invalid_moves = [(5, 4), (6, 4)]  # Moving backwards is not allowed

        for move in invalid_moves:
            with self.subTest(move=move):
                self.assertFalse(pawn.move(move, self.board))
                self.assertIsInstance(self.board[4][4], Pawn)

    def test_valid_move_en_passant(self):
        pawn = Pawn("white", (3, 3))
        enemy_pawn = Pawn("black", (1, 2))
        self.board[3][3] = pawn
        self.board[1][2] = enemy_pawn

        enemy_pawn.move((3, 2), self.board)

        self.assertTrue(pawn.move((2, 2), self.board))
        self.assertIsNone(self.board[3][3])
        self.assertIsNone(self.board[3][2])
        self.assertIsInstance(self.board[2][2], Pawn)

    def test_invalid_move_en_passant(self):
        pawn = Pawn("white", (3, 3))
        enemy_pawn = Pawn("black", (2, 2))
        self.board[3][3] = pawn
        self.board[2][2] = enemy_pawn

        enemy_pawn.move((3, 2), self.board)

        self.assertFalse(pawn.move((2, 2), self.board))
        self.assertIsInstance(self.board[3][2], Pawn)
        self.assertIsInstance(self.board[3][3], Pawn)

    @mock.patch('builtins.input', create=True)
    def test_promotion(self, mock_input):
        mock_input.side_effect = ['Q', 'R', 'B', 'N']  # Ввод для каждого из превращений
        result_classes = [Queen, Rook, Bishop, Knight]

        for i in range(4):
            pawn = Pawn("white", (1, i))
            pawn.move((0, i), self.board)
            # Проверяем, что новая фигура имеет правильный класс
            self.assertIsInstance(self.board[0][i], result_classes[i])
            # Проверяем, что новая фигура правильно инициализирована
            self.assertEqual(self.board[0][i].color, "white")
            self.assertEqual(self.board[0][i].current_square, (0, i))
