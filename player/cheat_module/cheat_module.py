import random


class CheatModule:

    def __init__(self):
        pass

    @staticmethod
    def is_cheat_decision(chance):
        if 0 <= chance <= 1:
            return random.random() < chance
