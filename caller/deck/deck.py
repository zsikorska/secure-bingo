import random
from logger.logger import Logger
from caller.deck.deck_generator import DeckGenerator
import config as config


class Deck(DeckGenerator):
    def __init__(self, logger: Logger):
        DeckGenerator.__init__(self, logger)
        self.logger = logger   
        self.data = self.generate()
         
    def shuffle(self):
        self.data = random.sample(range(1, config.DECK_SIZE + 1), config.DECK_SIZE )
        self.data = [i.to_bytes(2, 'little') for i in self.data]
        self.logger.info("Caller", f"Deck data has been shuffled.")
    
        