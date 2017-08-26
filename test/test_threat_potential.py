import numpy as np
import unittest

from test.utils import Gomoku, parse_board

from threat_potential import ThreatPotential

class TestThreatPotential(unittest.TestCase):

    def test_notice_three_threat(self):
        """
        If the square will make a threat, record it and the threat made.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . X . X . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        (
            player_threats,
            opponent_threats,
            immediate_response,
        ) = ThreatPotential(15).calculate(board, (7, 7))

        self.assertEqual(player_threats, 1)
        self.assertEqual(opponent_threats, 0)
        self.assertEqual(immediate_response, False)

    @unittest.skip('TODO')
    def test_notice_opponent_three_threat(self):
        """
        If the square will make an opponent's threat, record it and the threat
        made.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . O . O . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        (
            player_threats,
            opponent_threats,
            immediate_response,
        ) = ThreatPotential(15).calculate(board, (7, 7))

        self.assertEqual(player_threats, 0)
        self.assertEqual(opponent_threats, 1)
        self.assertEqual(immediate_response, False)
