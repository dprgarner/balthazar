from client import GomokuBase


SIXES = {
    (0, 1, 1, 1, 0, 0): ('THREE', [0, 4], [4]),
    (0, 0, 1, 1, 1, 0): ('THREE', [1, 5], [1]),
    (0, 1, 0, 1, 1, 0): ('SPLIT_THREE', [0, 2, 5], [2]),
    (0, 1, 1, 0, 1, 0): ('SPLIT_THREE', [0, 3, 5], [3]),
    (0, 1, 1, 1, 1, 0): ('OPEN_FOUR', [0, 5], [0, 5]),
}

FIVES = {
    (0, 1, 1, 1, 1): ('FOUR', [0], [0]),
    (1, 0, 1, 1, 1): ('FOUR', [1], [1]),
    (1, 1, 0, 1, 1): ('FOUR', [2], [2]),
    (1, 1, 1, 0, 1): ('FOUR', [3], [3]),
    (1, 1, 1, 1, 0): ('FOUR', [4], [4]),
    (1, 1, 1, 1, 1): ('FIVE', [], []),
}


class Gomoku(GomokuBase):

    def get_victor(self, state):
        """
        TODO use np.diag
        """

        # Check along rows.
        for row in range(self.SIZE):
            in_a_row = 0
            for col in range(1, self.SIZE):
                if state[row, col] == state[row, col - 1] != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return state[row, col]

        # Check along columns.
        for col in range(self.SIZE):
            in_a_row = 0
            for row in range(self.SIZE):
                if state[row, col] == state[row - 1, col] != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return state[row, col]

        # The down-right diagonals.
        for i in range(-self.SIZE + 5, self.SIZE - 4):
            start_row = max(0, -i)
            start_col = max(0, i)

            last = None
            in_a_row = 0

            for k in range(min(self.SIZE - start_row, self.SIZE - start_col)):
                next_square = state[start_row + k, start_col + k]
                if next_square == last != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return last
                last = next_square

        # The up-right diagonals.
        for i in range(4, self.SIZE * 2 - 5):
            start_row = min(i, self.SIZE - 1)
            start_col = max(0, i - self.SIZE + 1)

            last = None
            in_a_row = 0

            for k in range(min(start_row + 1, self.SIZE - start_col)):
                next_square = state[start_row - k, start_col + k]
                if next_square == last != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return last
                last = next_square

        return 0

    def match_six_threat(self, counters):
        # Return (player, type, defence_squares, offense_squares).

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
        # Return (player, type, defence_squares, offense_squares).

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

    def find_threats(self, state):
        """
        In progress...
        """
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
