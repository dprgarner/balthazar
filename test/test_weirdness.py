import numpy as np
import unittest

from test.utils import Gomoku, parse_board


class TestWeirdness(unittest.TestCase):

    def test_does_not_make_pointless_move(self):
        """
        Block multiple three-threats over making strange moves. (Taken from
        an actual game).
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . O . . . . . . .
            . . . . ? O X X X . . . . . .
            . . . . O X O O O X . . . . .
            . . . X O X X X O . O . . . .
            . . . . . . X O O O . X . . .
            . . . . . . . X O X . . . . .
            . . . . . . . X X O . . . . .
            . . . . . . . O . O ! . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        turn = Gomoku().play_turn(board)
        self.assertEqual(turn, (12, 10))

    def test_does_not_try_and_move_in_occupied_space(self):
        """
        Sometimes, near the end of the game, there is a bug where the
        heuristic function chooses an occupied square.
        """
        board = parse_board("""
            X O O X O O X O O X O O X O O
            O X X O X X O X X O X X O X X
            X O O X O O X O O X O O X O O
            O X X O X X O X X O X X O X X
            X O O X O O X O O X O O X O O
            O X X O X X O X X O X X O X X
            X O O X O O X O O X O O X O O
            O X X O X X O X X O X X O X X
            X O O X O O X O O X O O X O O
            O X X O X X O X X O X X O X X
            X O O X O O X O O X O O X O O
            O X X O X X O X X O X X O X X
            X O O X O O X O O X O O X O O
            O X X O X X O X X O X X O X X
            . . . . . . . . . . . . . . .
        """)

        class RandomGomoku(Gomoku):
            RANDOMNESS = 20

        row, col = RandomGomoku().play_turn(board)
        self.assertEqual(row, 14)
        row, col = RandomGomoku().play_turn(board)
        self.assertEqual(row, 14)
        row, col = RandomGomoku().play_turn(board)
        self.assertEqual(row, 14)
        row, col = RandomGomoku().play_turn(board)
        self.assertEqual(row, 14)
        row, col = RandomGomoku().play_turn(board)
        self.assertEqual(row, 14)
        row, col = RandomGomoku().play_turn(board)
        self.assertEqual(row, 14)
