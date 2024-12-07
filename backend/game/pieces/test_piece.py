import unittest

from backend.game.pieces.bishop import Bishop
from backend.game.pieces.king import King
from backend.game.pieces.knight import Knight
from backend.game.pieces.pawn import Pawn
from backend.game.pieces.queen import Queen
from backend.game.pieces.rook import Rook


class TestPiece(unittest.TestCase):
    def setUp(self):
        self.valid_cases = [
            (King, "white", (1, 1)),
            (King, "black", (7, 2)),
            (Queen, "white", (3, 1)),
            (Queen, "black", (4, 6)),
            (Rook, "white", (1, 3)),
            (Rook, "black", (0, 0)),
            (Bishop, "white", (0, 1)),
            (Bishop, "black", (2, 7)),
            (Knight, "white", (3, 4)),
            (Knight, "black", (4, 5)),
            (Pawn, "white", (6, 1)),
            (Pawn, "black", (6, 7)),
        ]

        self.invalid_colors = [
            (King, "abacaba"),
            (Queen, "superQueen"),
            (Rook, "xdxdxd"),
            (Bishop, "megaSlon"),
            (Knight, "ded dvinul koney"),
            (Pawn, "just a slave"),
        ]

        self.invalid_positions = [
            (King, (-1, 1)),
            (Queen, (8, 1)),
            (Rook, (100, -1)),
            (Bishop, (2, -2)),
            (Knight, (100, 10)),
            (Pawn, (1, 9)),
        ]

    def test_valid_color_and_position(self):
        for cls, color, position in self.valid_cases:
            with self.subTest(cls=cls, color=color, position=position):
                piece = cls(color.lower(), position)
                self.assertEqual(piece.color, color.lower())
                self.assertEqual(piece.current_square, position)

    def test_invalid_color(self):
        for cls, color in self.invalid_colors:
            with self.subTest(cls=cls, color=color):
                with self.assertRaises(ValueError):
                    cls(color, (1, 1))

    def test_invalid_position(self):
        for cls, position in self.invalid_positions:
            with self.subTest(cls=cls, position=position):
                with self.assertRaises(ValueError):
                    cls("white", position)

