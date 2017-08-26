import numpy as np
import unittest

from test.utils import Gomoku, parse_board, clear_falsy
from threats import Threats


threats_instance = Threats(15)


class TestThreatsPotential(unittest.TestCase):

    def test_three_threat(self):
        """
        If the square will make a threat, record it and the number of moves
        that it would take to win.
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
        threats = clear_falsy(
            threats_instance.find_threats_from_move(board, (7, 7))
        )
        self.assertEqual(threats, {
            1: {'TWO_MOVES': 1}
        })

    def test_four_threat(self):
        """
        If the square will make a threat, record it and the number of moves
        that it would take to win.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . O X X . X . O . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        threats = clear_falsy(
            threats_instance.find_threats_from_move(board, (7, 7))
        )
        self.assertEqual(threats, {
            1: {'ONE_MOVE': 1}
        })

    def test_row_threat_edge(self):
        """
        Detect row threats at the edges.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . O ! X X X . O . . . . . . .
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
            . . . . . . . . X . . O O ! .
        """)
        threats = clear_falsy(
            threats_instance.find_threats_from_move(board, (1, 2))
        )
        self.assertEqual(threats, {
            1: {'ONE_MOVE': 1}
        })
        threats = clear_falsy(
            threats_instance.find_threats_from_move(board, (14, 13))
        )
        self.assertEqual(threats, {
            -1: {'TWO_MOVES': 1}
        })

    def test_col_threat_edge(self):
        """
        Detect column threats at the edges.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . X . . . . . . .
            . . . . . . . X . . . . . . .
            . . . . . . . X . . . . . . .
            . . . . . . . O . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . O . . . . . . .
            . . . . . . . O . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . X . . . . . . .
        """)
        threats = clear_falsy(
            threats_instance.find_threats_from_move(board, (0, 7))
        )
        self.assertEqual(threats, {
            1: {'ONE_MOVE': 1}
        })
        threats = clear_falsy(
            threats_instance.find_threats_from_move(board, (12, 7))
        )
        self.assertEqual(threats, {
            -1: {'TWO_MOVES': 1}
        })

    def test_diag_down_threat_edge(self):
        """
        Detect diagonal down-right threats at the edges.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . ! . . . .
            . . . . . . . . . . . O . . .
            . . . . . . . . . . . . O . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            ! . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . X . . . . . . . . . . . .
            . . . X . . . . . . . . . . .
            . . . . X . . . . . . . . . .
        """)
        threats = clear_falsy(
            threats_instance.find_threats_from_move(board, (10, 0))
        )
        self.assertEqual(threats, {
            1: {'ONE_MOVE': 1}
        })
        threats = clear_falsy(
            threats_instance.find_threats_from_move(board, (1, 10))
        )
        self.assertEqual(threats, {
            -1: {'TWO_MOVES': 1}
        })

    def test_diag_up_threat_edge(self):
        """
        Detect diagonal up-right threats at the edges.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . . 
            . . . . O . . . . . . . . . . 
            . . . O . . . . . . . . . . . 
            . . ! . . . . . . . . . . . . 
            . . . . . . . . . . . . . . . 
            . . . . . . . . . . . . . . . 
            . . . . . . . . . . . . . . . 
            . . . . . . . . . . . . . . . 
            . . . . . . . . . . . . . . . 
            . . . . . . . . . . . . . . . 
            . . . . . . . . . . . . . . . 
            . . . . . . . . ! . . . . . . 
            . . . . . . . . . X . . . . . 
            . . . . . . . . . . X . . . . 
            . . . . . . . . . . . X . . . 
        """)
        threats = clear_falsy(
            threats_instance.find_threats_from_move(board, (3, 2))
        )
        self.assertEqual(threats, {
            -1: {'TWO_MOVES': 1}
        })

        threats = clear_falsy(
            threats_instance.find_threats_from_move(board, (11, 8))
        )
        self.assertEqual(threats, {
            1: {'ONE_MOVE': 1}
        })

    def test_simultaneous_threats(self):
        """
        Record when multiple threats are registered in different rows.
        """
        board = parse_board("""
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . ! X X X O
            . . . . . . . . . X . . . . .
            . . . . . . . . X . . . . . .
            . . . . . X X ! . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . .
        """)
        threats = clear_falsy(
            threats_instance.find_threats_from_move(board, (7, 7))
        )
        self.assertEqual(threats, {
            1: {'TWO_MOVES': 2}
        })

        threats = clear_falsy(
            threats_instance.find_threats_from_move(board, (4, 10))
        )
        self.assertEqual(threats, {
            1: {
                'ONE_MOVE': 1,
                'TWO_MOVES': 1,
            }
        })
