import random

import numpy as np

from client import GomokuBase
from heuristic import HEURISTICS
from threat_potential import ThreatPotential
from threat_response import ThreatResponse


float_formatter = lambda x: "%.1f" % x
np.set_printoptions(formatter={'float_kind': float_formatter})


class Gomoku(GomokuBase):

    TRIALS = 12

    @property
    def threat_potential(self):
        if not hasattr(self, '_threat_potential'):
            self._threat_potential = ThreatPotential(self.SIZE)
        return self._threat_potential

    @property
    def cached_heuristic(self):
        if not hasattr(self, '_heuristic'):
            self._heuristic = (
                HEURISTICS.get(self.heuristic)(self.SIZE)
            )
            print('Using heuristic:', self.heuristic)
        return self._heuristic

    def get_heuristic_board(self):
        return Heuristics(self.SIZE).get_heuristic_board(state)

    def play_turn(self, state):
        """
        Given the state (represented as a single list of 15*15 integers, 1 for
        the current player, -1 for the opponent), return the index pair (i, j)
        of the place to play, where i, j are integers from 0 to 14.
        """
        player = 1

        heuristic = HEURISTICS[self.heuristic](self.SIZE)

        # If there is a threat to respond to, either by the current bot or the
        # opponent, then respond immediately.
        threat_responder = ThreatResponse(self.SIZE, heuristic)
        threat_response = threat_responder.response_to_threat(state)
        if threat_response:
            return threat_response

        # Check the most likely squares for gain
        weights = heuristic.get_heuristic_board(state)
        best_options = [
            (x // self.SIZE, x % self.SIZE)
            for x in weights.argsort(axis=None)[-self.TRIALS:][::-1]
        ]

        threat_potentials = [
            self.threat_potential.get_potential(state, move)
            for move in best_options
        ]

        max_weight = np.amax(weights)
        max_indices = [
            (i, j)
            for i in range(self.SIZE)
            for j in range(self.SIZE)
            if weights[i, j] == max_weight
        ]
        return random.choice(max_indices)


if __name__ == '__main__':
    Gomoku()
