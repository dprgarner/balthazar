import numpy as np
import unittest

from heuristic import Heuristic
from test.utils import Gomoku, parse_board


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
            . . . . . . . ! . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        turn = Gomoku().play_turn(board)
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
            . . . . . . ! . ! . . . . . .
            . . . . . . . O . . . . . . .
            . . . . . . ! . ! . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        turn = Gomoku().play_turn(board)
        self.assertIn(turn, [(6, 6), (8, 8), (8, 6), (6, 8)])


class TestPossibleFivesHeuristics(unittest.TestCase):

    def test_possible_fives_when_following_up(self):
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

        class HeuristicWithBias(Heuristic):
            potential_one_player = 1
            potential_one_opponent = 0
            potential_empty = 0

        biases = HeuristicWithBias(board).add_possible_fives_bias(board)
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
        print(biases)
        self.assertTrue(np.all(biases == expected))

    def test_possible_fives_when_responding_to_opponent(self):
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
            . . . . . . . O . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)

        class HeuristicWithBias(Heuristic):
            potential_one_player = 0
            potential_one_opponent = 1
            potential_empty = 0

        biases = HeuristicWithBias(board).add_possible_fives_bias(board)
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
