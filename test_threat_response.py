import numpy as np
import unittest

from test_utils import Gomoku, parse_board


class TestFindWin(unittest.TestCase):

    def test_respond_to_unblocked_threat(self):
        """
        If there's a four threat, the bot must play there and win.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . X X X X . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        turn = Gomoku().play_turn(board, 1)

        # It doesn't matter which one the bot picks: they both win.
        self.assertIn(turn, [(7, 0), (7, 5)])

    def test_ignore_threat_if_going_to_win(self):
        """
        If both players have a four threat, the bot should just ignore the
        opponent's threat and win.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . O O O O X . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . X X X X . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        turn = Gomoku().play_turn(board, 1)

        # It doesn't matter which one the bot picks: they both win.
        self.assertIn(turn, [(7, 0), (7, 5)])

    def test_respond_to_threat_if_going_to_lose(self):
        """
        If the opponent has a four threat and the bot does not, then the bot
        must respond.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . O O O O X . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . X X X . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        turn = Gomoku().play_turn(board, 1)
        self.assertEqual(turn, (2, 0))

    def test_convert_split_three_to_open_four(self):
        """
        If there are no four threats and a split three threat, then the bot
        should make an unblockable open four.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . O O O . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . X X . X . . . . . . . .
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

        self.assertEqual(turn, (5, 5))

    def test_convert_three_to_open_four(self):
        """
        If there are no four threats and a three threat, then the bot should
        make an unblockable open four.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . O O O . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . X X X . . . . . . . . .
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

        # Either turn works.
        self.assertIn(turn, [(5, 2), (5, 6)])

    def test_block_three_threat(self):
        """
        If there are no other threats and there is a three threat, then the
        bot should block it.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . O O O . . . . . . . . . .
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

        # Either turn works.
        self.assertIn(turn, [(2, 1), (2, 5)])

    def test_block_split_three_threat(self):
        """
        If there are no other threats and there is a three threat, then the
        bot should block it.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . O O . O . . . . . . . . .
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

        # Either turn works.
        self.assertIn(turn, [(2, 1), (2, 4), (2, 6)])

    def test_block_botched_three_threat(self):
        """
        If the opponent creates two three threats that can be simultaneously
        blocked, then choose the space that block them both.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . O O . O . . . . . . . . .
            . . . . O . . . . . . . . . .
            . . . . O . . . . . . . . . .
            . . . . O . . . . . . . . . .
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

        self.assertEqual(turn, (2, 4))