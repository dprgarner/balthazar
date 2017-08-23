import numpy as np


class Heuristic:
    """
    A class for getting a rough, non-depth-searching value for each counter on
    the board.
    """

    # Tuneable parameters.
    centre_weight = 1
    centre_gradient = 0.1
    cross_weight = 1

    potential_three_player = 20
    potential_three_opponent = 15

    potential_two_player = 20
    potential_two_opponent = 15

    potential_one_player = 3
    potential_one_opponent = 1
    potential_empty = 0

    def __init__(self, size):
        self.SIZE = size

    @property
    def potential_weights(self):
        if not hasattr(self, '_potential_weights'):
            self._potential_weights = {
            # Could certainly form a threat next turn.
            (3, 2, 0): self.potential_three_opponent,
            (0, 2, 3): self.potential_three_player,

            # Could potentially form a threat next turn.
            (2, 3, 0): self.potential_two_opponent,
            (0, 3, 2): self.potential_two_player,

            # Perhaps better to play in places that could eventually form a
            # five.
            (1, 4, 0): self.potential_one_opponent,
            (0, 4, 1): self.potential_one_player,

            (0, 5, 0): self.potential_empty,
        }
        return self._potential_weights

    def centre_bias(self):
        # A numpy array reflecting bias towards the centre.
        centre = np.zeros((self.SIZE, self.SIZE), dtype=float)
        max_ = 0
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                centre[i, j] = (self.SIZE // 2 - i)**2 + (self.SIZE // 2 - j)**2
                max_ = max(max_, centre[i, j])
        centre = (max_ - centre) / max_

        return self.centre_weight * centre ** self.centre_gradient

    def cross_bias(self):
        # There should be a preference for the spaces diagonally adjacent to the
        # centre.
        cross = np.zeros((self.SIZE, self.SIZE), dtype=float)
        cross[self.SIZE // 2, self.SIZE // 2] = 1
        cross[self.SIZE // 2 - 1, self.SIZE // 2 - 1] = 1
        cross[self.SIZE // 2 + 1, self.SIZE // 2 - 1] = 1
        cross[self.SIZE // 2 - 1, self.SIZE // 2 + 1] = 1
        cross[self.SIZE // 2 + 1, self.SIZE // 2 + 1] = 1
        return self.cross_weight * cross

    def find_potentials_in_line(self, line):
        counts = [0, 0, 0]
        for i in range(len(line)):
            counts[line[i] + 1] += 1
            if i > 4:
                counts[line[i - 5] + 1] -= 1

            if i > 3:
                weight = self.potential_weights.get(tuple(counts), None)
                if weight:
                    yield i - 4, weight

    def add_possible_fives_bias(self, state):
        biases = np.zeros((self.SIZE, self.SIZE), dtype=float)

        # Check along rows for potential fives.
        for row in range(self.SIZE):
            for offset, weight in self.find_potentials_in_line(state[row]):
                for i in range(5):
                    biases[row, offset + i] += weight

        # Check along columns...
        for col in range(self.SIZE):
            for offset, weight in self.find_potentials_in_line(state[:, col]):
                for i in range(5):
                    biases[offset + i, col] += weight

        # Check along down-right diagonals...
        for diag_offset in range(-self.SIZE + 5, self.SIZE - 4):
            diag_line = list(np.diagonal(state, offset=diag_offset))
            for offset, weight in self.find_potentials_in_line(diag_line):
                row = max(0, -diag_offset) + offset
                col = max(0, diag_offset) + offset
                for i in range(5):
                    biases[row + i, col + i] += weight

        # Check along down-right diagonals...
        for diag_offset in range(-self.SIZE + 5, self.SIZE - 4):
            diag_line = list(np.diagonal(state[::-1], offset=diag_offset))
            for offset, weight in self.find_potentials_in_line(diag_line):
                row = self.SIZE - 1 - max(0, -diag_offset) - offset
                col = max(0, diag_offset) + offset
                for i in range(5):
                    biases[row - i, col + i] += weight

        return biases

    def get_heuristic_board(self, state):
        heuristic = np.zeros((self.SIZE, self.SIZE), dtype=float)
        heuristic += self.centre_bias()
        heuristic += self.cross_bias()
        heuristic += self.add_possible_fives_bias(state)
        heuristic[state != 0] = -1
        return heuristic


class HighThreesHeuristic(Heuristic):
    """
    Weights the values of threes more highly.
    """
    potential_three_player = 100
    potential_three_opponent = 50


class BaseTwentyHeuristic(Heuristic):
    """
    As above, but (maybe) using Adrian's bot's values.
    """
    potential_three_player = int('1111111', 20)
    potential_three_opponent = int('111111', 20)

    potential_two_player = int('11111', 20)
    potential_two_opponent = int('1111', 20)

    potential_one_player = int('111', 20)
    potential_one_opponent = int('11', 20)

    potential_empty = int('1', 20)


HEURISTICS = {
    'default': Heuristic,
    'basetwenty': BaseTwentyHeuristic,
    'highthrees': HighThreesHeuristic,
}
