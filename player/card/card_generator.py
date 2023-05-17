import random

import config as config


class CardGenerator():
    def __init__(self) -> None:
        pass

    def generate(self):
        return random.sample(range(1, config.DECK_SIZE), config.CARD_SIZE)
