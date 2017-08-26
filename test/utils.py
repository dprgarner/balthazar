import numpy as np

import gomoku


class Gomoku(gomoku.Gomoku):
    heuristic = 'deterministic'

    # Do not connect or set args.
    def set_args(self):
        pass

    def connect(self):
        pass


def clear_falsy(dict_):
    """
    Helper tool to cut down on test boilerplate.
    """
    if type(dict_) != dict:
        return
    keys = list(dict_.keys())
    for k in keys:
        clear_falsy(dict_[k])
        if not dict_[k]:
            del dict_[k]
    return dict_


def parse_board(string):
    """
    Parses a string-representation of the board into a numpy array.
    """
    lookup = {
        'X': 1,
        'O': -1,
        '.': 0,
        '?': 0,
        '!': 0,
    }
    relevant_chars = lookup.keys()
    return np.array(
        [lookup[c] for c in string if c in relevant_chars]
    ).reshape(Gomoku.SIZE, Gomoku.SIZE)

class Heuristic:
    def __init__(self, SIZE):
        self.SIZE = SIZE

    # Null heuristic board.
    def calculate(self, state):
        return np.zeros((self.SIZE, self.SIZE))
