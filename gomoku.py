import random

import numpy as np

from client import GomokuBase
from threat_response import ThreatResponse
from heuristic import Heuristic, BaseTwentyHeuristic


class Gomoku(ThreatResponse, GomokuBase):

    @property
    def heuristic(self):
        if not hasattr(self, '_heuristic'):
            self._heuristic = (
                Heuristic(self.SIZE)
                if getattr(self, 'basetwenty', False)
                else BaseTwentyHeuristic(self.SIZE)
            )
        return self._heuristic

    def play_turn(self, state, player):
        """
        Given the state (represented as a single list of 15*15 integers, -1 for
        the first player, 1 for the second player, 0 for empty) and the player
        number (-1 if this bot is the first player, 1 if the bot is the second
        player), return the index of the place to play (from 0 to 15*15-1).
        """

        # If there is a threat to respond to, either by the current bot or the
        # opponent, then respond immediately.
        threat_response = self.response_to_threat(state, player)
        if threat_response:
            return threat_response

        heuristic = self.heuristic.get_heuristic_board(state, player)

        max_weight = np.amax(heuristic)
        max_indices = [
            (i, j)
            for i in range(self.SIZE)
            for j in range(self.SIZE)
            if heuristic[i, j] == max_weight
        ]
        return random.choice(max_indices)


if __name__ == '__main__':
    Gomoku()
