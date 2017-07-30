import numpy as np
import unittest

import gomoku


class Gomoku(gomoku.Gomoku):
    def __init__(self):
        # Do not connect or set args.
        pass


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

    def test_open_four_threat(self):
        threat = Gomoku().match_six_threat([0, +1, +1, +1, +1, 0])
        self.assertEqual(threat, (1, 'OPEN_FOUR', [0, 5], [0, 5]))

        threat = Gomoku().match_six_threat([0, -1, -1, -1, -1, 0])
        self.assertEqual(threat, (-1, 'OPEN_FOUR', [0, 5], [0, 5]))

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

    def test_five_threat(self):
        threat = Gomoku().match_five_threat([1, 1, 1, 1, 1])
        self.assertEqual(threat, (1, 'FIVE', [], []))

        threat = Gomoku().match_five_threat([-1, -1, -1, -1, -1])
        self.assertEqual(threat, (-1, 'FIVE', [], []))

    def test_null_threat(self):
        threat = Gomoku().match_five_threat([+1, +1, +1, 0, 0])
        self.assertIsNone(threat)

        threat = Gomoku().match_five_threat([0, 0, +1, +1, +1])
        self.assertIsNone(threat)

        threat = Gomoku().match_five_threat([+1, +1, 0, 0, +1])
        self.assertIsNone(threat)
