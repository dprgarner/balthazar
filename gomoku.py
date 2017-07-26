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

        # The top-right diagonals, going down-right.
        for start_col in range(self.SIZE - 4):
            last = None
            in_a_row = 0
            for row in range(0, self.SIZE - start_col):
                if state[row, start_col + row] == last != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return last
                last = state[row, start_col + row]

        # The bottom-left diagonals, going down-right.
        for start_row in range(1, self.SIZE - 4):
            last = None
            in_a_row = 0
            for col in range(0, self.SIZE - start_row):
                if state[start_row + col, col] == last != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return last
                last = state[start_row + col, col]

        # The top-left diagonals, going down-left.
        for start_col in range(4, self.SIZE):
            last = None
            in_a_row = 0
            for row in range(0, start_col + 1):
                if state[row, start_col - row] == last != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return last
                last = state[row, start_col - row]

        # The bottom-right diagonals, going up-right.
        for start_col in range(0, self.SIZE - 4):
            last = None
            in_a_row = 0
            for row in range(0, self.SIZE - start_col):
                if state[self.SIZE - row - 1, start_col + row] == last != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == 4:
                    return last
                last = state[self.SIZE - row - 1, start_col + row]

        return 0

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
