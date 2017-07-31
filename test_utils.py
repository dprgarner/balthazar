import numpy as np

import gomoku


class Gomoku(gomoku.Gomoku):
    def __init__(self):
        # Do not connect or set args.
        pass


def parse_board(string):
    """
    Parses a string-representation of the board into a numpy array.
    """
    lookup = {
        'X': 1,
        'O': -1,
        '.': 0,
    }
    relevant_chars = lookup.keys()
    return np.array(
        [lookup[c] for c in string if c in relevant_chars]
    ).reshape(Gomoku.SIZE, Gomoku.SIZE)
