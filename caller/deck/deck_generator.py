import config as config
from logger.logger import Logger


class DeckGenerator:
    def __init__(self, logger: Logger) -> None:
        pass

    def generate(self):
        return [i.to_bytes(2, 'little') for i in range(1, config.DECK_SIZE + 1)]
