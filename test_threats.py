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
        self.assertEqual(threat, ('THREE', 1, [0, 4]))

        threat = Gomoku().match_six_threat([0, -1, -1, -1, 0, 0])
        self.assertEqual(threat, ('THREE', -1, [0, 4]))

        threat = Gomoku().match_six_threat([0, 0, +1, +1, +1, 0])
        self.assertEqual(threat, ('THREE', +1, [1, 5]))

        threat = Gomoku().match_six_threat([0, 0, -1, -1, -1, 0])
        self.assertEqual(threat, ('THREE', -1, [1, 5]))

    def test_split_three_threat(self):
        threat = Gomoku().match_six_threat([0, +1, +1, 0, +1, 0])
        self.assertEqual(threat, ('SPLIT_THREE', 1, [0, 3, 5]))

        threat = Gomoku().match_six_threat([0, -1, -1, 0, -1, 0])
        self.assertEqual(threat, ('SPLIT_THREE', -1, [0, 3, 5]))

        threat = Gomoku().match_six_threat([0, +1, 0, +1, +1, 0])
        self.assertEqual(threat, ('SPLIT_THREE', +1, [0, 2, 5]))

        threat = Gomoku().match_six_threat([0, -1, 0, -1, -1, 0])
        self.assertEqual(threat, ('SPLIT_THREE', -1, [0, 2, 5]))

    def test_open_four_threat(self):
        threat = Gomoku().match_six_threat([0, +1, +1, +1, +1, 0])
        self.assertEqual(threat, ('OPEN_FOUR', 1, [0, 5]))

        threat = Gomoku().match_six_threat([0, -1, -1, -1, -1, 0])
        self.assertEqual(threat, ('OPEN_FOUR', -1, [0, 5]))

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
        self.assertEqual(threat, ('FOUR', 1, [0]))

        threat = Gomoku().match_five_threat([1, 0, 1, 1, 1])
        self.assertEqual(threat, ('FOUR', 1, [1]))

        threat = Gomoku().match_five_threat([1, 1, 0, 1, 1])
        self.assertEqual(threat, ('FOUR', 1, [2]))

        threat = Gomoku().match_five_threat([1, 1, 1, 0, 1])
        self.assertEqual(threat, ('FOUR', 1, [3]))

        threat = Gomoku().match_five_threat([1, 1, 1, 1, 0])
        self.assertEqual(threat, ('FOUR', 1, [4]))

        threat = Gomoku().match_five_threat([0, -1, -1, -1, -1])
        self.assertEqual(threat, ('FOUR', -1, [0]))

    def test_five_threat(self):
        threat = Gomoku().match_five_threat([1, 1, 1, 1, 1])
        self.assertEqual(threat, ('FIVE', 1, []))

        threat = Gomoku().match_five_threat([-1, -1, -1, -1, -1])
        self.assertEqual(threat, ('FIVE', -1, []))

    def test_null_threat(self):
        threat = Gomoku().match_five_threat([+1, +1, +1, 0, 0])
        self.assertIsNone(threat)

        threat = Gomoku().match_five_threat([0, 0, +1, +1, +1])
        self.assertIsNone(threat)

        threat = Gomoku().match_five_threat([+1, +1, 0, 0, +1])
        self.assertIsNone(threat)
