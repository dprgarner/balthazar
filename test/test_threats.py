import numpy as np
import unittest

from test.utils import Heuristic, parse_board
from threat_response import ThreatResponse


threat_responder = ThreatResponse(15, Heuristic(15))


class TestMatchSixThreatDetecting(unittest.TestCase):

    def test_three_threat(self):
        threat = threat_responder.match_six_threat([0, +1, +1, +1, 0, 0])
        self.assertEqual(threat, (1, 'THREE', [0, 4], [4]))

        threat = threat_responder.match_six_threat([0, -1, -1, -1, 0, 0])
        self.assertEqual(threat, (-1, 'THREE', [0, 4], [4]))

        threat = threat_responder.match_six_threat([0, 0, +1, +1, +1, 0])
        self.assertEqual(threat, (1, 'THREE', [1, 5], [1]))

        threat = threat_responder.match_six_threat([0, 0, -1, -1, -1, 0])
        self.assertEqual(threat, (-1, 'THREE', [1, 5], [1]))

    def test_split_three_threat(self):
        threat = threat_responder.match_six_threat([0, +1, +1, 0, +1, 0])
        self.assertEqual(threat, (1, 'SPLIT_THREE', [0, 3, 5], [3]))

        threat = threat_responder.match_six_threat([0, -1, -1, 0, -1, 0])
        self.assertEqual(threat, (-1, 'SPLIT_THREE', [0, 3, 5], [3]))

        threat = threat_responder.match_six_threat([0, +1, 0, +1, +1, 0])
        self.assertEqual(threat, (1, 'SPLIT_THREE', [0, 2, 5], [2]))

        threat = threat_responder.match_six_threat([0, -1, 0, -1, -1, 0])
        self.assertEqual(threat, (-1, 'SPLIT_THREE', [0, 2, 5], [2]))

    def test_null_threat(self):
        threat = threat_responder.match_six_threat([+1, +1, +1, +1, 0, 0])
        self.assertIsNone(threat)

        threat = threat_responder.match_six_threat([0, 0, +1, +1, +1, +1])
        self.assertIsNone(threat)

        threat = threat_responder.match_six_threat([+1, +1, 0, 0, +1, +1])
        self.assertIsNone(threat)


class TestMatchFiveThreatDetecting(unittest.TestCase):

    def test_four_threat(self):
        threat = threat_responder.match_five_threat([0, 1, 1, 1, 1])
        self.assertEqual(threat, (1, 'FOUR', [0], [0]))

        threat = threat_responder.match_five_threat([1, 0, 1, 1, 1])
        self.assertEqual(threat, (1, 'FOUR', [1], [1]))

        threat = threat_responder.match_five_threat([1, 1, 0, 1, 1])
        self.assertEqual(threat, (1, 'FOUR', [2], [2]))

        threat = threat_responder.match_five_threat([1, 1, 1, 0, 1])
        self.assertEqual(threat, (1, 'FOUR', [3], [3]))

        threat = threat_responder.match_five_threat([1, 1, 1, 1, 0])
        self.assertEqual(threat, (1, 'FOUR', [4], [4]))

        threat = threat_responder.match_five_threat([0, -1, -1, -1, -1])
        self.assertEqual(threat, (-1, 'FOUR', [0], [0]))

    def test_null_threat(self):
        threat = threat_responder.match_five_threat([+1, +1, +1, 0, 0])
        self.assertIsNone(threat)

        threat = threat_responder.match_five_threat([0, 0, +1, +1, +1])
        self.assertIsNone(threat)

        threat = threat_responder.match_five_threat([+1, +1, 0, 0, +1])
        self.assertIsNone(threat)


def clear_falsy(dict_):
    """
    Helper tool to cut down on test boilerplate.
    """
    if type(dict_) != dict:
        return
    keys = list(dict_.keys())
    for k in keys:
        clear_falsy(dict_[k])
        if not dict_[k]:
            del dict_[k]
    return dict_


class TestFindThreat(unittest.TestCase):

    def test_no_threats(self):
        """
        No immediate threats here.
        """
        board = parse_board("""
            . . . . . . . . . . . . . O .
            X . . . . . . . . . . . . O .
            X . . . . . . . . . . . . O .
            X . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            O . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . O X X X O . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . O
            X . . . . . . . . . . . . X .
            . X . . . . . . . . . . X . .
            . . X . . . . . . . . X . . .
            . . . X . . . . . . X . . . .
        """)
        threats = threat_responder.find_threats_in_grid(board)
        self.assertEqual(clear_falsy(threats), {})

    def test_find_open_four(self):
        """
        Should find an open four, i.e. two four threats.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . X X X X . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        threats = threat_responder.find_threats_in_grid(board)
        self.assertEqual(clear_falsy(threats), {
            1: {
                'FOUR': [(7, 4), (7, 9)],
            },
        })

    def test_find_closed_four(self):
        """
        Should find a closed four.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            O O O . O . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        threats = threat_responder.find_threats_in_grid(board)
        self.assertEqual(clear_falsy(threats), {
            -1: {
                'FOUR': [(7, 3)],
            },
        })

    def test_find_closed_four_with_piece_boundaries(self):
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            X O O . O O X . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        threats = threat_responder.find_threats_in_grid(board)
        self.assertEqual(clear_falsy(threats), {
            -1: {
                'FOUR': [(7, 3)],
            },
        })

    def test_split_three(self):
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            X . O . O O . X . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        threats = threat_responder.find_threats_in_grid(board)
        self.assertEqual(clear_falsy(threats), {
            -1: {
                'SPLIT_THREE': [(7, 1), (7, 3), (7, 6)],
            },
        })

    def test_column_threats(self):
        board = parse_board("""
            X . . . . . . . . . . . . . .
            X . . . . . . . . . . . . . .
            X . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            X . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        threats = threat_responder.find_threats_in_grid(board)
        self.assertEqual(clear_falsy(threats), {
            1: {
                'FOUR': [(3, 0)],
            },
        })

    def test_open_three_yielded_once(self):
        """
        Only one threat should be registered when there is an open three.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . O . . . . . . . . . . . .
            . . O . . . . . . . . . . . .
            . . O . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        threats = threat_responder.find_threats_in_grid(board)
        self.assertEqual(clear_falsy(threats), {
            -1: {
                'THREE': [(9, 2), (13, 2)],
            },
        })

    def test_down_right_diagonal_threats(self):
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . X . . . .
            . . . . . . . . . . . X . . .
            . . . . . . . . . . . . X . .
            . . . . . . . . . . . . . X .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            O . . . . . . . . . . . . . .
            . O . . . . . . . . . . . . .
            . . O . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . O . . . . . . . . . .
        """)
        threats = threat_responder.find_threats_in_grid(board)
        self.assertEqual(clear_falsy(threats), {
            1: {
                'FOUR': [(0, 9), (5, 14)],
            },
            -1: {
                'FOUR': [(13, 3)],
            },
        })

    def test_down_left_diagonal_threats(self):
        board = parse_board("""
            . . . . O . . . . . . . . . .
            . . . O . . . . . . . . . O .
            . . O . . . . . . . . . O . .
            . . . . . . . . . . . O . . .
            O . . . . . . . . . O . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . X . . . . . . . . X .
            . . . . . . . . . . . . X . .
            . . X . . . . . . . . . . . .
            . X . . . . . . . . X . . . .
            X . . . . . . . . . . . . . .
        """)
        threats = threat_responder.find_threats_in_grid(board)
        self.assertEqual(clear_falsy(threats), {
            1: {
                'FOUR': [(11, 3)],
                'SPLIT_THREE': [(12, 11)],
            },
            -1: {
                'FOUR': [(3, 1), (5, 9), (0, 14)],
            },
        })

