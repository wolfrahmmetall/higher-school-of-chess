import unittest
from typing import Optional

# Import necessary classes from your project
from backend.game.pieces.king import King
from backend.game.pieces.queen import Queen
from backend.game.pieces.rook import Rook
from backend.game.pieces.bishop import Bishop
from backend.game.pieces.knight import Knight
from backend.game.pieces.pawn import Pawn
from backend.game.pieces.piece import Piece
from backend.game.board import Board
from backend.game.chess_game import ChessGame


class TestEvergreenGame(unittest.TestCase):
    def setUp(self):
        # Initialize the game and set up the board
        self.game = ChessGame(60, 0)
        self.game.start_game()
        self.board = self.game.board

    def test_evergreen_game(self):
        # List of moves in the Evergreen Game in algebraic notation
        moves = [
            ('e2', 'e4'),  # 1. e4
            ('e7', 'e5'),  # 1... e5
            ('g1', 'f3'),  # 2. Nf3
            ('b8', 'c6'),  # 2... Nc6
            ('f1', 'c4'),  # 3. Bc4
            ('f8', 'c5'),  # 3... Bc5
            ('b2', 'b4'),  # 4. b4
            ('c5', 'b4'),  # 4... Bxb4
            ('c3', 'c3'),  # 5. c3
            ('b4', 'a5'),  # 5... Ba5
            ('d2', 'd4'),  # 6. d4
            ('e5', 'd4'),  # 6... exd4
            ('e1', 'g1'),  # 7. O-O (castling)
            ('d4', 'c3'),  # 7... dxc3
            ('b1', 'c3'),  # 8. Nxc3
            ('d7', 'd6'),  # 8... d6
            ('c1', 'g5'),  # 9. Bg5
            ('c8', 'g4'),  # 9... Bg4
            ('h2', 'h3'),  # 10. h3
            ('g4', 'h5'),  # 10... Bh5
            ('g2', 'g4'),  # 11. g4
            ('h5', 'g6'),  # 11... Bg6
            ('f3', 'h4'),  # 12. Nh4
            ('g6', 'e4'),  # 12... Be4
            ('d1', 'e2'),  # 13. Qe2
            ('d8', 'g5'),  # 13... Qg5
            ('c4', 'e6'),  # 14. Bxe6
            ('f7', 'e6'),  # 14... fxe6
            ('h4', 'g2'),  # 15. Ng2
            ('e4', 'g2'),  # 15... Bxg2
            ('e2', 'e6+'), # 16. Qe6+
            ('g8', 'e7'),  # 16... Ne7
            ('c3', 'd5'),  # 17. Nd5
            ('a5', 'c3'),  # 17... Ba5
            ('b2', 'c3'),  # 18. Bxc3
            ('c6', 'e5'),  # 18... Nxd5
            ('e6', 'd5'),  # 19. Qxd5
            ('h7', 'h5'),  # 19... h5
            ('f2', 'f4'),  # 20. f4
            ('g5', 'g6'),  # 20... Qg6
            ('d5', 'b7'),  # 21. Qxb7
            ('e8', 'd8'),  # 21... Rd8
            ('f4', 'e5'),  # 22. exd6
            ('d8', 'd6'),  # 22... Rxd6
            ('d5', 'd6'),  # 23. Qxd6
            ('c7', 'd6'),  # 23... cxd6
            ('c1', 'f8'),  # 24. Rf8# (checkmate)
        ]

        # Function to convert chess notation to board indices
        def notation_to_index(notation):
            files = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                     'e': 4, 'f': 5, 'g': 6, 'h': 7}
            ranks = {'1': 7, '2': 6, '3': 5, '4': 4,
                     '5': 3, '6': 2, '7': 1, '8': 0}
            file = notation[0]
            rank = notation[1]
            return ranks[rank], files[file]

        white_to_move = True
        move_number = 1
        for move in moves:
            from_notation, to_notation = move

            # Handle special cases like castling
            if from_notation == 'e1' and to_notation == 'g1':
                # White kingside castling
                self.game.move('e1', 'g1')
                white_to_move = not white_to_move
                move_number += 1
                continue

            # Get the piece at the from position
            from_pos = notation_to_index(from_notation)
            piece = self.board[from_pos]
            self.assertIsNotNone(
                piece, f"No piece at position {from_notation}")

            # Check if it's the correct player's turn
            expected_color = 'white' if white_to_move else 'black'
            self.assertEqual(piece.color, expected_color,
                             f"Expected {expected_color}'s turn, but got {piece.color} at {from_notation}")

            # Perform the move
            move_result = self.game.move(from_notation, to_notation)
            self.assertTrue(
                move_result, f"Move from {from_notation} to {to_notation} failed at move {move_number}")

            # Optionally print the board after each move
            # self.game.board.print_board()

            white_to_move = not white_to_move
            move_number += 1

        # After the moves, check if black is checkmated
        self.assertTrue(self.game.result == "white won",
                        "Black is not checkmated when expected")

        # Check the final positions of key pieces
        expected_positions = {
            'f8': ('Rook', 'white'),
            'e8': ('King', 'black'),
            # Add more expected positions if needed
        }

        for notation, (expected_piece_name, expected_color) in expected_positions.items():
            pos = notation_to_index(notation)
            piece = self.board[pos]
            self.assertIsNotNone(
                piece, f"No piece at position {notation}")
            self.assertEqual(piece.__class__.__name__, expected_piece_name,
                             f"Expected {expected_piece_name} at {notation}, but got {piece.__class__.__name__}")
            self.assertEqual(piece.color, expected_color,
                             f"Expected {expected_color} piece at {notation}, but got {piece.color}")