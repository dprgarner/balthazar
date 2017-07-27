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
