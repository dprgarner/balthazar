import numpy as np
import unittest

import gomoku


class Gomoku(gomoku.Gomoku):
    def __init__(self):
        # Do not connect or set args.
        pass


def parse_board(string):
    """
    Parses a string-representation of the board into a numpy array.
    """
    lookup = {
        'X': 1,
        'O': -1,
        '.': 0,
    }
    relevant_chars = lookup.keys()
    return np.array(
        [lookup[c] for c in string if c in relevant_chars]
    ).reshape(Gomoku.SIZE, Gomoku.SIZE)


class TestMatchSixThreatDetecting(unittest.TestCase):

    def test_three_threat(self):
        threat = Gomoku().match_six_threat([0, +1, +1, +1, 0, 0])
        self.assertEqual(threat, (1, 'THREE', [0, 4], [4]))

        threat = Gomoku().match_six_threat([0, -1, -1, -1, 0, 0])
        self.assertEqual(threat, (-1, 'THREE', [0, 4], [4]))

        threat = Gomoku().match_six_threat([0, 0, +1, +1, +1, 0])
        self.assertEqual(threat, (1, 'THREE', [1, 5], [1]))

        threat = Gomoku().match_six_threat([0, 0, -1, -1, -1, 0])
        self.assertEqual(threat, (-1, 'THREE', [1, 5], [1]))

    def test_split_three_threat(self):
        threat = Gomoku().match_six_threat([0, +1, +1, 0, +1, 0])
        self.assertEqual(threat, (1, 'SPLIT_THREE', [0, 3, 5], [3]))

        threat = Gomoku().match_six_threat([0, -1, -1, 0, -1, 0])
        self.assertEqual(threat, (-1, 'SPLIT_THREE', [0, 3, 5], [3]))

        threat = Gomoku().match_six_threat([0, +1, 0, +1, +1, 0])
        self.assertEqual(threat, (1, 'SPLIT_THREE', [0, 2, 5], [2]))

        threat = Gomoku().match_six_threat([0, -1, 0, -1, -1, 0])
        self.assertEqual(threat, (-1, 'SPLIT_THREE', [0, 2, 5], [2]))

    def test_null_threat(self):
        threat = Gomoku().match_six_threat([+1, +1, +1, +1, 0, 0])
        self.assertIsNone(threat)

        threat = Gomoku().match_six_threat([0, 0, +1, +1, +1, +1])
        self.assertIsNone(threat)

        threat = Gomoku().match_six_threat([+1, +1, 0, 0, +1, +1])
        self.assertIsNone(threat)


class TestMatchFiveThreatDetecting(unittest.TestCase):

    def test_four_threat(self):
        threat = Gomoku().match_five_threat([0, 1, 1, 1, 1])
        self.assertEqual(threat, (1, 'FOUR', [0], [0]))

        threat = Gomoku().match_five_threat([1, 0, 1, 1, 1])
        self.assertEqual(threat, (1, 'FOUR', [1], [1]))

        threat = Gomoku().match_five_threat([1, 1, 0, 1, 1])
        self.assertEqual(threat, (1, 'FOUR', [2], [2]))

        threat = Gomoku().match_five_threat([1, 1, 1, 0, 1])
        self.assertEqual(threat, (1, 'FOUR', [3], [3]))

        threat = Gomoku().match_five_threat([1, 1, 1, 1, 0])
        self.assertEqual(threat, (1, 'FOUR', [4], [4]))

        threat = Gomoku().match_five_threat([0, -1, -1, -1, -1])
        self.assertEqual(threat, (-1, 'FOUR', [0], [0]))

    def test_null_threat(self):
        threat = Gomoku().match_five_threat([+1, +1, +1, 0, 0])
        self.assertIsNone(threat)

        threat = Gomoku().match_five_threat([0, 0, +1, +1, +1])
        self.assertIsNone(threat)

        threat = Gomoku().match_five_threat([+1, +1, 0, 0, +1])
        self.assertIsNone(threat)



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
        threats = Gomoku().find_threats_in_grid(board)
        self.assertEqual(threats, [])

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
        threats = Gomoku().find_threats_in_grid(board)
        self.assertIn((1, 'FOUR', [(7, 4)], [(7, 4)]), threats)
        self.assertIn((1, 'FOUR', [(7, 9)], [(7, 9)]), threats)

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
        threats = Gomoku().find_threats_in_grid(board)
        self.assertIn((-1, 'FOUR', [(7, 3)], [(7, 3)]), threats)

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
        threats = Gomoku().find_threats_in_grid(board)
        self.assertEqual(threats, [(-1, 'FOUR', [(7, 3)], [(7, 3)])])

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
        threats = Gomoku().find_threats_in_grid(board)
        self.assertEqual(threats, [
            (-1, 'SPLIT_THREE', [(7, 1), (7, 3), (7, 6)], [(7, 3)])
        ])

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
        threats = Gomoku().find_threats_in_grid(board)
        self.assertEqual(threats, [(1, 'FOUR', [(3, 0)], [(3, 0)])])

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
        threats = Gomoku().find_threats_in_grid(board)
        self.assertIn((-1, 'THREE', [(9, 2), (13, 2)], [(9, 2)]), threats)
        self.assertIn((-1, 'THREE', [(9, 2), (13, 2)], [(13, 2)]), threats)

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
        threats = Gomoku().find_threats_in_grid(board)
        self.assertIn((1, 'FOUR', [(5, 14)], [(5, 14)]), threats)
        self.assertIn((1, 'FOUR', [(0, 9)], [(0, 9)]), threats)
        self.assertIn((-1, 'FOUR', [(13, 3)], [(13, 3)]), threats)

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
        threats = Gomoku().find_threats_in_grid(board)
        self.assertIn((-1, 'FOUR', [(3, 1)], [(3, 1)]), threats)
        self.assertIn(
            (1, 'SPLIT_THREE', [(14, 9), (12, 11), (9, 14)], [(12, 11)]),
            threats,
        )
        self.assertIn((1, 'FOUR', [(11, 3)], [(11, 3)]), threats)
        self.assertIn((-1, 'FOUR', [(0, 14)], [(0, 14)]), threats)
