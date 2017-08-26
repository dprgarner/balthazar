import random

import numpy as np

from client import GomokuBase
from heuristic import HEURISTICS
from threat_potential import ThreatPotential
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

        # Prioritise preventing an unblockable open four from being made.
        if threats[-1]['SPLIT_THREE']:
            return heuristic.choose(threats[-1]['SPLIT_THREE'])
        if threats[-1]['THREE']:
            return heuristic.choose(threats[-1]['THREE'])

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

        # Check the most likely squares for gain
        # best_options = [
        #     (x // self.SIZE, x % self.SIZE)
        #     for x in weights.argsort(axis=None)[-self.TRIALS:][::-1]
        # ]

        # threat_potential = ThreatPotential(self.SIZE)
        # threat_potentials = [
        #     threat_potential.calculate(state, move)
        #     for move in best_options
        # ]

        return heuristic.choose([
            (i, j)
            for i in range(self.SIZE)
            for j in range(self.SIZE)
        ])


if __name__ == '__main__':
    Gomoku()
