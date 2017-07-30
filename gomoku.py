import numpy as np
from client import GomokuBase


# Each tuple is of the form (type, cost_squares, gain_squares), where
# cost_squares are the squares that a defender should play in to stop the
# threat being fulfilled, and gain_squares the squares which fulfill the
# threat.
SIXES = {
    (0, 1, 1, 1, 0, 0): ('THREE', [0, 4], [4]),
    (0, 0, 1, 1, 1, 0): ('THREE', [1, 5], [1]),
    (0, 1, 0, 1, 1, 0): ('SPLIT_THREE', [0, 2, 5], [2]),
    (0, 1, 1, 0, 1, 0): ('SPLIT_THREE', [0, 3, 5], [3]),

    # Technically there are no defensive responses to an open four, but the bot
    # would look a little defeatist if it didn't play in one of them.
    (0, 1, 1, 1, 1, 0): ('OPEN_FOUR', [0, 5], [0, 5]),
}

FIVES = {
    (0, 1, 1, 1, 1): ('FOUR', [0], [0]),
    (1, 0, 1, 1, 1): ('FOUR', [1], [1]),
    (1, 1, 0, 1, 1): ('FOUR', [2], [2]),
    (1, 1, 1, 0, 1): ('FOUR', [3], [3]),
    (1, 1, 1, 1, 0): ('FOUR', [4], [4]),

    # Probably won't be used?
    (1, 1, 1, 1, 1): ('FIVE', [], []),
}


class Gomoku(GomokuBase):

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
        This method mutates line.
        """
        offset = -1
        while len(line) >= 5:
            offset += 1
            if len(line) >= 6:
                six_threat = self.match_six_threat(line)
                if six_threat:
                    yield six_threat, offset
                    del line[0]
                    continue

            five_threat = self.match_five_threat(line)
            if five_threat:
                yield five_threat, offset

            del line[0]

    def find_threats_in_grid(self, state):
        threats = []

        # Check along rows for a threat.
        for row in range(self.SIZE):
            for threat in self.find_threats_in_line(list(state[row])):
                (player, type_, cost_squares, gain_squares), offset = threat
                threats.append((
                    player, type_, [
                        (row, offset + cost_square)
                        for cost_square in cost_squares
                    ], [
                        (row, offset + gain_square)
                        for gain_square in gain_squares
                    ]
                ))

        # Check along columns...
        for col in range(self.SIZE):
            for threat in self.find_threats_in_line(list(state[:, col])):
                (player, type_, cost_squares, gain_squares), offset = threat
                threats.append((
                    player, type_, [
                        (offset + cost_square, col)
                        for cost_square in cost_squares
                    ], [
                        (offset + gain_square, col)
                        for gain_square in gain_squares
                    ]
                ))

        # Check along down-right diagonals...
        for diag_offset in range(-self.SIZE + 5, self.SIZE - 4):
            diag_line = list(np.diagonal(state, offset=diag_offset))
            for threat in self.find_threats_in_line(diag_line):
                (player, type_, cost_squares, gain_squares), offset = threat
                row = max(0, -diag_offset) + offset
                col = max(0, diag_offset) + offset
                threats.append((
                    player, type_, [
                        (row + cost_square, col + cost_square)
                        for cost_square in cost_squares
                    ], [
                        (row + gain_square, col + gain_square)
                        for gain_square in gain_squares
                    ]
                ))

        # Check along down-left diagonals...
        for diag_offset in range(-self.SIZE + 5, self.SIZE - 4):
            diag_line = list(np.diagonal(state[::-1], offset=diag_offset))
            for threat in self.find_threats_in_line(diag_line):
                (player, type_, cost_squares, gain_squares), offset = threat
                row = self.SIZE - 1 - max(0, -diag_offset) - offset
                col = max(0, diag_offset) + offset
                threats.append((
                    player, type_, [
                        (row - cost_square, col + cost_square)
                        for cost_square in cost_squares
                    ], [
                        (row - gain_square, col + gain_square)
                        for gain_square in gain_squares
                    ]
                ))

        return threats

    def play_turn(self, state, player):
        """
        Given the state (represented as a single list of 15*15 integers, -1 for
        the first player, 1 for the second player, 0 for empty) and the player
        number (-1 if this bot is the first player, 1 if the bot is the second
        player), return the index of the place to play (from 0 to 15*15-1).
        """
        next_place = sum(sum(abs(i) for i in state))
        return next_place // self.SIZE, next_place % self.SIZE


if __name__ == '__main__':
    Gomoku()
