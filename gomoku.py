from client import GomokuBase


class Gomoku(GomokuBase):

    def get_victor(self, state):
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
        # Return (type_, gain_squares)

        counts = [0, 0, 0]
        for s in range(6):
            counts[counters[s] + 1] += 1

        if counts[0] != 0 and counts[2] != 0:
            return
        if counts[0] < 3 and counts[2] < 3:
            return

        player = 1 if counts[2] else -1
        abs_six = tuple(abs(counters[s]) for s in range(6))

        if abs_six == (0, 1, 1, 1, 0, 0):
            return ('THREE', player, [0, 4])
        if abs_six == (0, 0, 1, 1, 1, 0):
            return ('THREE', player, [1, 5])

        if abs_six == (0, 1, 0, 1, 1, 0):
            return ('SPLIT_THREE', player, [0, 2, 5])
        if abs_six == (0, 1, 1, 0, 1, 0):
            return ('SPLIT_THREE', player, [0, 3, 5])

        if abs_six == (0, 1, 1, 1, 1, 0):
            return ('OPEN_FOUR', player, [0, 5])

    def match_five_threat(self, counters):
        # Return (type_, gain_squares)

        counts = [0, 0, 0]
        for s in range(5):
            counts[counters[s] + 1] += 1

        if counts[0] != 0 and counts[2] != 0:
            return
        if counts[0] < 4 and counts[2] < 4:
            return

        player = 1 if counts[2] else -1
        abs_five = tuple(abs(counters[s]) for s in range(5))

        if abs_five == (0, 1, 1, 1, 1):
            return ('FOUR', player, [0])

        if abs_five == (1, 0, 1, 1, 1):
            return ('FOUR', player, [1])

        if abs_five == (1, 1, 0, 1, 1):
            return ('FOUR', player, [2])

        if abs_five == (1, 1, 1, 0, 1):
            return ('FOUR', player, [3])

        if abs_five == (1, 1, 1, 1, 0):
            return ('FOUR', player, [4])

        if abs_five == (1, 1, 1, 1, 1):
            return ('FIVE', player, [])

    def find_threat(self, state):
        """
        In progress...
        """
        threats = []
        return
        # Check along rows for a threat.
        for row in range(self.SIZE):
            counters = list(state[row])

            while counters:
                if len(group) > 6:
                    six_threat = self.match_six_threat(counters)
                    if six_threat:
                        type_, player, gain_squares = six_threat
                        threats.append(
                            type_, [
                                (row, col + gain_square)
                                for gain_square in gain_squares
                            ]
                        )
                        continue
                    group.pop()

                if len(group) == 5:
                    five_threat = self.match_five_threat(group)
                    if five_threat:
                        type_, player, gain_squares, depleted = five_threat
                        threats.append(
                            type_, [
                                (row, col + gain_square)
                                for gain_square in gain_squares
                            ]
                        )
                    del counters[0]
                else:
                    break

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
