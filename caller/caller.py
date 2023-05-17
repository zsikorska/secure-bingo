from caller.deck.deck import Deck
from logger.logger import Logger


class Caller():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.deck = Deck(logger)
        self.deck.shuffle()
        self.current_number_index = 0

    def update_next_number(self):
        self.current_number_index += 1

    def is_deck_over(self):
        return self.current_number_index >= len(self.deck.data)

    def get_current_number(self):
        return self.deck.data[self.current_number_index]
