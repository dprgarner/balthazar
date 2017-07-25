from client import GomokuBase


class Gomoku(GomokuBase):
    """
    Write your bot here!
    """
    def get_victor(self, state):
        # Check along rows.
        for row in range(self.SIZE):
            offset = row * self.SIZE
            in_a_row = 0
            for col in range(1, self.SIZE):
                if state[offset + col] == state[offset + col - 1] != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return state[offset + col]

        # Check along columns.
        for col in range(self.SIZE):
            in_a_row = 0
            for offset in range(self.SIZE, self.SIZE * self.SIZE, self.SIZE):
                if state[offset + col] == state[offset + col - self.SIZE] != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return state[offset + col]

        # The top-right diagonals, going down-right.
        for start_col in range(self.SIZE - 4):
            last = None
            in_a_row = 0
            for row in range(0, self.SIZE - start_col):
                if state[(self.SIZE + 1) * row + start_col] == last != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return last
                last = state[(self.SIZE + 1) * row + start_col]

        # The bottom-left diagonals, going down-right.
        for start_row in range(1, self.SIZE - 4):
            last = None
            in_a_row = 0
            for col in range(0, self.SIZE - start_row):
                if state[(start_row + col) * self.SIZE + col] == last != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return last
                last = state[(start_row + col) * self.SIZE + col]

        # The top-left diagonals, going down-left.
        for start_col in range(4, self.SIZE):
            last = None
            in_a_row = 0
            for row in range(0, start_col + 1):
                if state[(self.SIZE - 1) * row + start_col] == last != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return last
                last = state[(self.SIZE - 1) * row + start_col]

        # The bottom-right diagonals, going up-right.
        """
        for start_col in range(0, self.SIZE - 4):
            last = None
            in_a_row = 0
            for row in range(0, start_col + 1):
                if state[(self.SIZE - 1) * row + start_col] == last != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return last
                last = state[(self.SIZE - 1) * row + start_col]
        """


        return 0

    def play_turn(self, state, player):
        """
        Given the state (represented as a single list of 15*15 integers, -1 for
        the first player, 1 for the second player, 0 for empty) and the player
        number (-1 if this bot is the first player, 1 if the bot is the second
        player), return the index of the place to play (from 0 to 15*15-1).
        """
        return sum(abs(i) for i in state)


if __name__ == '__main__':
    Gomoku()
