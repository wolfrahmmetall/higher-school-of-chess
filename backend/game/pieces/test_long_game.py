import unittest
from typing import Tuple

# Import necessary classes from your project
from backend.game.pieces.king import King
from backend.game.pieces.queen import Queen
from backend.game.pieces.rook import Rook
from backend.game.pieces.bishop import Bishop
from backend.game.pieces.knight import Knight
from backend.game.pieces.pawn import Pawn
from backend.game.chess_game import ChessGame


class TestEvergreenGame(unittest.TestCase):
    def setUp(self):
        # Initialize the game and set up the board
        self.game = ChessGame(60, 0)
        self.game.start_game()
        self.board = self.game.board

    def test_evergreen_game(self):
        # List of moves in the Evergreen Game in coordinate notation
        moves = [
            ('e2', 'e4'),  # 1. e4
            ('e7', 'e5'),  # 1... e5
            ('g1', 'f3'),  # 2. Nf3
            ('b8', 'c6'),  # 2... Nc6
            ('f1', 'c4'),  # 3. Bc4
            ('f8', 'c5'),  # 3... Bc5
            ('b2', 'b4'),  # 4. b4
            ('c5', 'b4'),  # 4... Bxb4
            ('c2', 'c3'),  # 5. c3
            ('b4', 'a5'),  # 5... Ba5
            ('d2', 'd4'),  # 6. d4
            ('e5', 'd4'),  # 6... exd4
            ('e1', 'g1'),  # 7. O-O (castling)
            ('d4', 'd3'),  # 7... d3
            ('d1', 'b3'),  # 8. Qb3
            ('d8', 'f6'),  # 8... Qf6
            ('e4', 'e5'),  # 9. e5
            ('f6', 'g6'),  # 9... Qg6
            ('f1', 'e1'),  # 10. Re1
            ('g8', 'e7'),  # 10... Nge7
            ('c1', 'a3'),  # 11. Ba3
            ('b7', 'b5'),  # 11... b5
            ('b3', 'b5'),  # 12. Qxb5
            ('a8', 'b8'),  # 12... Rb8
            ('b5', 'a4'),  # 13. Qa4
            ('a5', 'b6'),  # 13... Bb6
            ('b1', 'd2'),  # 14. Nbd2
            ('c8', 'b7'),  # 14... Bb7
            ('d2', 'e4'),  # 15. Ne4
            ('g6', 'f5'),  # 15... Qf5
            ('c4', 'd3'),  # 16. Bxd3
            ('f5', 'h5'),  # 16... Qh5
            ('e4', 'f6'),  # 17. Nf6+
            ('g7', 'f6'),  # 17... gxf6
            ('e5', 'f6'),  # 18. exf6
            ('h8', 'g8'),  # 18... Rg8
            ('a1', 'd1'),  # 19. Rad1
            ('h5', 'f3'),  # 19... Qxf3
            ('e1', 'e7'),  # 20. Rxe7+
            ('c6', 'e7'),  # 20... Nxe7
            ('a4', 'd7'),  # 21. Qxd7+
            ('e8', 'd7'),  # 21... Kxd7
            ('d3', 'f5'),  # 22. Bf5+
            ('d7', 'e8'),  # 22... Ke8
            ('f5', 'd7'),  # 23. Bd7+
            ('e8', 'f8'),  # 23... Kf8
            ('a3', 'e7'),  # 24. Bxe7# (checkmate)
        ]

        # Perform the moves
        for move_number, (from_notation, to_notation) in enumerate(moves, 1):
            # Perform the move
            move_result = self.game.move(from_notation, to_notation)
            self.assertTrue(
                move_result, f"Move from {from_notation} to {to_notation} failed at move {move_number}"
            )

        # Expected final positions of pieces
        expected_positions = {
            # White pieces
            'd1': ('Rook', 'white'),
            'g1': ('King', 'white'),
            'd7': ('Bishop', 'white'),
            'e7': ('Bishop', 'white'),
            'a2': ('Pawn', 'white'),
            'c3': ('Pawn', 'white'),
            'f2': ('Pawn', 'white'),
            'f6': ('Pawn', 'white'),
            'g2': ('Pawn', 'white'),
            'h2': ('Pawn', 'white'),
            # Black pieces
            'f8': ('King', 'black'),
            'f3': ('Queen', 'black'),
            'g8': ('Rook', 'black'),
            'b8': ('Rook', 'black'),
            'b6': ('Bishop', 'black'),
            'b7': ('Bishop', 'black'),
            'a7': ('Pawn', 'black'),
            'c7': ('Pawn', 'black'),
            'f7': ('Pawn', 'black'),
            'h7': ('Pawn', 'black'),
        }

        # Now compare the actual final positions with the expected positions
        board = self.game.board
        for row in range(8):
            for col in range(8):
                position_notation = self.index_to_notation(row, col)
                piece = board[row, col]
                if position_notation in expected_positions:
                    expected_piece_name, expected_color = expected_positions[position_notation]
                    self.assertIsNotNone(piece, f"Expected {expected_piece_name} at {position_notation}, but found None")
                    self.assertEqual(
                        piece.__class__.__name__, expected_piece_name,
                        f"Expected {expected_piece_name} at {position_notation}, but found {piece.__class__.__name__}"
                    )
                    self.assertEqual(
                        piece.color, expected_color,
                        f"Expected {expected_color} piece at {position_notation}, but found {piece.color}"
                    )
                else:
                    # We expect no piece at this position
                    self.assertIsNone(piece, f"Expected empty square at {position_notation}, but found {piece}")

        # Indicate that tests passed
        print("All tests passed.")

    @staticmethod
    def index_to_notation(row: int, col: int) -> str:
        files = 'abcdefgh'
        ranks = '87654321'
        return files[col] + ranks[row]


if __name__ == '__main__':
    unittest.main()