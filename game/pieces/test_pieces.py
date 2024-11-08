import pytest
import unittest

from game.pieces.king import King
from game.pieces.queen import Queen
from game.pieces.rook import Rook
from game.pieces.bishop import Bishop
from game.pieces.knight import Knight
from game.pieces.pawn import Pawn


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


