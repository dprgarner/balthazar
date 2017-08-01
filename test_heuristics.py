import numpy as np
import unittest

from test_utils import Gomoku, parse_board


class TestHeuristics(unittest.TestCase):

    def test_centre_bias(self):
        """
        The bot should play in the centre on the first turn.
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
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        turn = Gomoku().play_turn(board, 1)
        self.assertEqual(turn, (7, 7))

    def test_cross_bias(self):
        """
        The bot should play diagonally away from the centre on the second turn.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . X . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        turn = Gomoku().play_turn(board, -1)
        self.assertIn(turn, [(6, 6), (8, 8), (8, 6), (6, 8)])


class TestPossibleFivesHeuristics(unittest.TestCase):

    def test_possible_fives(self):
        """
        Check that the same rows, columns, and diagonals of an existing square
        are preferred.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . X . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)

        class GomokuWithBias(Gomoku):
            potential_one_player = 1
            potential_one_opponent = 0

        biases = GomokuWithBias().add_possible_fives_bias(board, 1)
        # The centre is a nonsense result, so ignore.
        biases[7, 7] = 0
        expected = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 3, 4, 0, 4, 3, 2, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ], dtype=float)
        self.assertTrue(np.all(biases == expected))

    def test_possible_fives(self):
        """
        Check that the same rows, columns, and diagonals of an opponent's square
        are preferred.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . X . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)

        class GomokuWithBias(Gomoku):
            potential_one_player = 0
            potential_one_opponent = 1

        biases = GomokuWithBias().add_possible_fives_bias(board, -1)
        # The centre is a nonsense result, so ignore.
        biases[7, 7] = 0
        expected = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 3, 4, 0, 4, 3, 2, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ], dtype=float)
        self.assertTrue(np.all(biases == expected))