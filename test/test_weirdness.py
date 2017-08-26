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
