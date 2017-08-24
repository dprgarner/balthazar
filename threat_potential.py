import numpy as np


class ThreatPotential:
    def __init__(self, SIZE):
        self.SIZE = SIZE

    def calculate(self, state, move):
        if state[move] != 0:
            return
        return (1, 0, False)
