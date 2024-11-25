import copy

import pytest
import unittest

from backend.game.pieces.king import King
from backend.game.pieces.piece import Piece
from backend.game.pieces.queen import Queen
from backend.game.pieces.rook import Rook
from backend.game.pieces.bishop import Bishop
from backend.game.pieces.knight import Knight
from backend.game.pieces.pawn import Pawn


class TestPiece(unittest.TestCase):
    def test_valid_color_and_position(self):
        piece_kw = King("white", (1, 1))
        piece_kb = King("bLACK", (7, 2))
        piece_qw = Queen("white", (3, 1))
        piece_qb = Queen("black", (4, 6))
        piece_rw = Rook("WHIte", (1, 3))
        piece_rb = Rook("black", (0, 0))
        piece_bw = Bishop("whITe", (0, 1))
        piece_bb = Bishop("black", (2, 7))
        piece_nw = Knight("white", (3, 4))
        piece_nb = Knight("BLACK", (4, 5))
        piece_pw = Pawn("White", (6, 1))
        piece_pb = Pawn("black", (6, 7))
        assert piece_kw.color == "white" and piece_kw.current_square == (1, 1)
        assert piece_kb.color == "black" and piece_kb.current_square == (7, 2)
        assert piece_qw.color == "white" and piece_qw.current_square == (3, 1)
        assert piece_qb.color == "black" and piece_qb.current_square == (4, 6)
        assert piece_rw.color == "white" and piece_rw.current_square == (1, 3)
        assert piece_rb.color == "black" and piece_rb.current_square == (0, 0)
        assert piece_bw.color == "white" and piece_bw.current_square == (0, 1)
        assert piece_bb.color == "black" and piece_bb.current_square == (2, 7)
        assert piece_nw.color == "white" and piece_nw.current_square == (3, 4)
        assert piece_nb.color == "black" and piece_nb.current_square == (4, 5)
        assert piece_pw.color == "white" and piece_pw.current_square == (6, 1)
        assert piece_pb.color == "black" and piece_pb.current_square == (6, 7)

    def test_invalid_color(self):
        with pytest.raises(ValueError):
            piece_k = King("abacaba", (1, 1))
        with pytest.raises(ValueError):
            piece_q = Queen("superQueen", (1, 1))
        with pytest.raises(ValueError):
            piece_r = Rook("xdxdxd", (1, 1))
        with pytest.raises(ValueError):
            piece_b = Bishop("megaSlon", (1, 1))
        with pytest.raises(ValueError):
            piece_n = Knight("ded dvinul koney", (1, 1))
        with pytest.raises(ValueError):
            piece_p = Pawn("just a slave", (1, 1))

    def test_invalid_position(self):
        with pytest.raises(ValueError):
            piece_k = King("white", (-1, 1))
        with pytest.raises(ValueError):
            piece_q = Queen("black", (8, 1))
        with pytest.raises(ValueError):
            piece_r = Rook("white", (100, -1))
        with pytest.raises(ValueError):
            piece_b = Bishop("black", (2, -2))
        with pytest.raises(ValueError):
            piece_n = Knight("white", (100, 10))
        with pytest.raises(ValueError):
            piece_p = Pawn("black", (1, 9))


class TestKnight(unittest.TestCase):
    board: list[list[Piece | None]] = [
        [None for _ in range(8)] for _ in range(8)
    ]

    def test_valid_move_to_empty_square(self):
        knight_moves = [
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1)
        ]
        board = copy.deepcopy(self.board)
        board[4][4] = Knight("white", (4, 4))
        for dr, dc in knight_moves:
            board_1 = copy.deepcopy(board)
            assert board_1[4][4].move((4 + dr, 4 + dc), board_1)
            assert board_1[4][4] is None
            assert type(board_1[4+dr][4+dc]) == Knight

    def test_move_to_square_with_enemy(self):
        board = copy.deepcopy(self.board)
        board[4][4] = Knight("white", (4, 4))
        board[5][6] = Pawn("black", (5, 6))
        assert board[4][4].move((5, 6), board)
        assert board[4][4] is None
        assert type(board[5][6]) == Knight

    def test_move_to_square_with_ally(self):
        board = copy.deepcopy(self.board)
        board[4][4] = Knight("white", (4, 4))
        board[5][6] = Pawn("white", (5, 6))
        assert not board[4][4].move((5, 6), board)
        assert type(board[4][4]) == Knight
        assert type(board[5][6]) == Pawn

    def test_invalid_move(self):
        board = copy.deepcopy(self.board)
        board[4][4] = Knight("white", (4, 4))
        assert not board[4][4].move((4, 4), board)
        assert type(board[4][4]) == Knight
        assert not board[4][4].move((4, 6), board)
        assert type(board[4][4]) == Knight
        assert not board[4][4].move((4, 3), board)
        assert type(board[4][4]) == Knight
        assert not board[4][4].move((5, 5), board)
        assert type(board[4][4]) == Knight
        assert not board[4][4].move((7, 2), board)
        assert type(board[4][4]) == Knight
        assert not board[4][4].move((0, 0), board)
        assert type(board[4][4]) == Knight

    def test_move_out_of_board(self):
        board = copy.deepcopy(self.board)
        board[1][1] = Knight("white", (1, 1))
        assert not board[1][1].move((-1, 0), board)
        assert type(board[1][1]) == Knight
        assert not board[1][1].move((0, -1), board)
        assert not board[1][1].move((-1, -1), board)


