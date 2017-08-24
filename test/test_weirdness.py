import numpy as np
import unittest

from test.utils import Gomoku, parse_board

from threat_potential import ThreatPotential


class TestWeirdness(unittest.TestCase):

    @unittest.skip('TODO')
    def test_does_not_make_pointless_move(self):
        """
        What is going on here? The bot moves in (6, 4), when it should move
        in (12, 10)...
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
