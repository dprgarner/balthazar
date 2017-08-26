import random

import numpy as np

from client import GomokuBase
from heuristic import HEURISTICS
from threats import Threats


float_formatter = lambda x: "%.1f" % x
np.set_printoptions(formatter={'float_kind': float_formatter})


class Gomoku(GomokuBase):

    TRIALS = 12

    def response_to_threat(self, state, heuristic):
        # First, find and collate the threats.
        threats = self.threats.find_all_threats(state)

        # Prioritise an immediate win.
        if threats[1]['FOUR']:
            return heuristic.choose(threats[1]['FOUR'])

        # Prioritise blocking an immediate loss.
        if threats[-1]['FOUR']:
            return heuristic.choose(threats[-1]['FOUR'])

        # Prioritise making an unblockable open four.
        if threats[1]['SPLIT_THREE']:
            return heuristic.choose(threats[1]['SPLIT_THREE'])
        if threats[1]['THREE']:
            return heuristic.choose(threats[1]['THREE'])

        # Check in the best option squares whether there are any unblockable
        # simultaneous threats that can be made, by either player.
        best_moves = heuristic.get_best_options(self.TRIALS)

        new_threats = {}
        for move in best_moves:
            new_threats[move] = self.threats.find_threats_from_move(state, move)
            # Make an unblockable instant-response threat if it exists.
            if (
                new_threats[move][1]['ONE_MOVE'] > 1 or
                new_threats[move][1]['ONE_MOVE'] == 1 and
                new_threats[move][1]['TWO_MOVES'] > 0
            ):
                return move
            # Prevent an unblockable instant-response threat if it exists.
            if (
                new_threats[move][-1]['ONE_MOVE'] > 1 or
                new_threats[move][-1]['ONE_MOVE'] == 1 and
                new_threats[move][-1]['TWO_MOVES'] > 0
            ):
                return move

        # Prioritise preventing an unblockable open four from being made.
        if threats[-1]['SPLIT_THREE']:
            return heuristic.choose(threats[-1]['SPLIT_THREE'])
        if threats[-1]['THREE']:
            return heuristic.choose(threats[-1]['THREE'])

        # Find an unblockable sequence of three-threats, if any.
        for move in best_moves:
            # Prioritise player's move.
            if new_threats[move][1]['TWO_MOVES'] > 1:
                return move
            # Respond to opponent's possible sequence.
            if new_threats[move][-1]['TWO_MOVES'] > 1:
                return move

    def play_turn(self, state):
        """
        Given the state (represented as a single list of 15*15 integers, 1 for
        the current player, -1 for the opponent), return the index pair (i, j)
        of the place to play, where i, j are integers from 0 to 14.
        """
        self.Heuristic = HEURISTICS[self.heuristic]
        self.threats = Threats(self.SIZE)
        heuristic = self.Heuristic(state)

        # If there is a threat to respond to, either by the current bot or the
        # opponent, then respond immediately.
        threat_response = self.response_to_threat(state, heuristic)
        if threat_response:
            return threat_response

        # Just choose the best-looking move.
        return heuristic.choose([
            (i, j)
            for i in range(self.SIZE)
            for j in range(self.SIZE)
        ], randomness=self.randomness)


if __name__ == '__main__':
    Gomoku()
