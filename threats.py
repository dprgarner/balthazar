import numpy as np


# Each tuple is of the form (type, cost_squares, gain_squares), where
# cost_squares are the squares that a defender should play in to stop the
# threat being fulfilled, and gain_squares the squares which fulfill the
# threat.
THREAT_TYPES = ['THREE', 'SPLIT_THREE', 'FOUR']

SIXES = {
    (0, 1, 1, 1, 0, 0): ('THREE', [0, 4], [4]),
    (0, 0, 1, 1, 1, 0): ('THREE', [1, 5], [1]),
    (0, 1, 0, 1, 1, 0): ('SPLIT_THREE', [0, 2, 5], [2]),
    (0, 1, 1, 0, 1, 0): ('SPLIT_THREE', [0, 3, 5], [3]),

    # Is this necessary?
    # (0, 1, 1, 1, 1, 0): ('OPEN_FOUR', [0, 5], [0, 5]),
}


FIVES = {
    (0, 1, 1, 1, 1): ('FOUR', [0], [0]),
    (1, 0, 1, 1, 1): ('FOUR', [1], [1]),
    (1, 1, 0, 1, 1): ('FOUR', [2], [2]),
    (1, 1, 1, 0, 1): ('FOUR', [3], [3]),
    (1, 1, 1, 1, 0): ('FOUR', [4], [4]),

    # Probably won't be used?
    # (1, 1, 1, 1, 1): ('FIVE', [], []),
}


class Threats:
    """
    A class that handles whether a player needs to immediately respond to a
    given state on the board.
    """
    def __init__(self, SIZE):
        self.SIZE = SIZE

    def match_six_threat(self, counters):
        # Return (player, type, cost_squares, gain_squares).

        counts = [0, 0, 0]
        for s in range(6):
            counts[counters[s] + 1] += 1

        if counts[0] != 0 and counts[2] != 0:
            return
        if counts[0] < 3 and counts[2] < 3:
            return
        player = 1 if counts[2] else -1

        abs_six = tuple(abs(counters[s]) for s in range(6))
        threat = SIXES.get(abs_six)

        if threat:
            return (player,) + threat

    def match_five_threat(self, counters):
        # Return (player, type, cost_squares, gain_squares).

        counts = [0, 0, 0]
        for s in range(5):
            counts[counters[s] + 1] += 1

        if counts[0] != 0 and counts[2] != 0:
            return
        if counts[0] < 4 and counts[2] < 4:
            return
        player = 1 if counts[2] else -1

        abs_five = tuple(abs(counters[s]) for s in range(5))
        threat = FIVES.get(abs_five)

        if threat:
            return (player,) + threat

    def find_threats_in_line(self, line):
        """
        This generator mutates the input list 'line'.
        """
        offset = -1
        last_six_threat = None
        while len(line) >= 5:
            offset += 1
            if len(line) >= 6:
                six_threat = self.match_six_threat(line)
                # Special case: don't yield an open three threat made by the
                # other player twice in a row, as it's the same threat.
                if six_threat and not (
                    six_threat[0] == -1 and
                    six_threat[1] == 'THREE' and
                    last_six_threat and
                    last_six_threat[1] == 'THREE'
                ):
                    yield six_threat, offset
                last_six_threat = six_threat

            five_threat = self.match_five_threat(line)
            if five_threat:
                yield five_threat, offset

            del line[0]

    def find_all_threats(self, state):
        threats = {
            1: {
                threat_type: []
                for threat_type in THREAT_TYPES
            },
            -1: {
                threat_type: []
                for threat_type in THREAT_TYPES
            },
        }

        # Check along rows for a threat.
        for row in range(self.SIZE):
            for threat in self.find_threats_in_line(list(state[row])):
                (player, type_, cost_squares, gain_squares), offset = threat
                costs = [
                    (row, offset + cost_square)
                    for cost_square in cost_squares
                ]
                gains = [
                    (row, offset + gain_square)
                    for gain_square in gain_squares
                ]
                threats[player][type_].extend(
                    gains if player == 1 else costs
                )

        # Check along columns...
        for col in range(self.SIZE):
            for threat in self.find_threats_in_line(list(state[:, col])):
                (player, type_, cost_squares, gain_squares), offset = threat
                costs = [
                    (offset + cost_square, col)
                    for cost_square in cost_squares
                ]
                gains = [
                    (offset + gain_square, col)
                    for gain_square in gain_squares
                ]
                threats[player][type_].extend(
                    gains if player == 1 else costs
                )

        # Check along down-right diagonals...
        for diag_offset in range(-self.SIZE + 5, self.SIZE - 4):
            diag_line = list(np.diagonal(state, offset=diag_offset))
            for threat in self.find_threats_in_line(diag_line):
                (player, type_, cost_squares, gain_squares), offset = threat
                row = max(0, -diag_offset) + offset
                col = max(0, diag_offset) + offset
                costs = [
                    (row + cost_square, col + cost_square)
                    for cost_square in cost_squares
                ]
                gains = [
                    (row + gain_square, col + gain_square)
                    for gain_square in gain_squares
                ]
                threats[player][type_].extend(
                    gains if player == 1 else costs
                )

        # Check along down-left diagonals...
        for diag_offset in range(-self.SIZE + 5, self.SIZE - 4):
            diag_line = list(np.diagonal(state[::-1], offset=diag_offset))
            for threat in self.find_threats_in_line(diag_line):
                (player, type_, cost_squares, gain_squares), offset = threat
                row = self.SIZE - 1 - max(0, -diag_offset) - offset
                col = max(0, diag_offset) + offset
                costs = [
                    (row - cost_square, col + cost_square)
                    for cost_square in cost_squares
                ]
                gains = [
                    (row - gain_square, col + gain_square)
                    for gain_square in gain_squares
                ]
                threats[player][type_].extend(
                    gains if player == 1 else costs
                )

        return threats
