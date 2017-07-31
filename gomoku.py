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
    # Also, is this necessary?
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


class Gomoku(GomokuBase):
    # Tuneable parameters
    centre_weight = 1
    centre_gradient = 1
    cross_weight = 1

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

    def get_heuristic_board(self, state, player):
        heuristic = np.zeros((self.SIZE, self.SIZE), dtype=float)
        heuristic += self.centre_bias()
        heuristic += self.cross_bias()
        heuristic[state != 0] = 0
        return heuristic

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
        while len(line) >= 5:
            offset += 1
            if len(line) >= 6:
                six_threat = self.match_six_threat(line)
                if six_threat:
                    yield six_threat, offset

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

    def response_to_threat(self, state, player):
        # First, find and collate the threats.
        threats = {}
        for threat_player, type_, costs, gains in self.find_threats_in_grid(state):
            if threat_player not in threats:
                threats[threat_player] = {}
            if type_ not in threats[threat_player]:
                threats[threat_player][type_] = []
            threats[threat_player][type_].extend(
                gains if threat_player == player else costs
            )

        # Prioritise an immediate win.
        if threats.get(player, {}).get('FOUR'):
            return threats[player]['FOUR'][0]

        # Prioritise blocking an immediate loss.
        if threats.get(-player, {}).get('FOUR'):
            return threats[-player]['FOUR'][0]

        # Prioritise making an unblockable open four.
        if threats.get(player, {}).get('SPLIT_THREE'):
            return threats[player]['SPLIT_THREE'][0]
        if threats.get(player, {}).get('THREE'):
            return threats[player]['THREE'][0]

        # Prioritise preventing an unblockable open four from being made.
        # The bot must choose the square that appears in the most simultaneous
        # threats.
        three_threats = {}
        for threat in (
            threats.get(-player, {}).get('SPLIT_THREE', []) +
            threats.get(-player, {}).get('THREE', [])
        ):
            three_threats[threat] = three_threats.get(threat, 0) + 1
        if three_threats:
            max_square = None
            max_concurrent_threats = 0
            for square, concurrent_threats in three_threats.items():
                if concurrent_threats > max_concurrent_threats:
                    max_concurrent_threats = concurrent_threats
                    max_square = square
            return max_square

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
        heuristic = self.get_heuristic_board(state, player)
        return np.unravel_index(np.argmax(heuristic), (self.SIZE, self.SIZE))


if __name__ == '__main__':
    Gomoku()
