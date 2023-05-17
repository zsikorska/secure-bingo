import math

import config
from player.card.card_generator import CardGenerator


class Card(CardGenerator):
    def __init__(self):
        CardGenerator.__init__(self)
        self.data = self.generate()
        self.numbers_checked = [False for i in self.data]

    def update(self, new_number: int):
        for i in range(len(self.data)):
            if new_number == self.data[i]:
                self.numbers_checked[i] = True

    def check_bingo(self):
        dimension = int(math.sqrt(config.CARD_SIZE))
        d_range = range(dimension)
        # diagonal
        solutions = [[(x, x) for x in d_range], [(x, dimension - x - 1) for x in d_range]]
        # horizontal
        solutions += [[(x, y) for x in d_range] for y in d_range]
        # vertical
        solutions += [[(y, x) for x in d_range] for y in d_range]

        for line in solutions:
            done = True
            for x, y in line:
                if not self.numbers_checked[y * dimension + x]:
                    done = False
                    break
            if done:
                return True
        return False

    def dict(self):
        return {
            'data': ' '.join(str(e) for e in self.data),
            'checked': ' '.join(str(e) for e in self.numbers_checked)
        }

    @staticmethod
    def from_dict(card_as_dict):
        card = Card()
        card.data = [int(x) for x in card_as_dict["data"].split()]
        card.numbers_checked = [x == "True" for x in card_as_dict["checked"].split()]
        return card

    def pretty(self):
        dimension = int(math.sqrt(config.CARD_SIZE))
        pretty = "======== CARD ========\n"
        for i in range(0, config.CARD_SIZE, dimension):
            pretty += "|"
            for j in range(dimension):
                pretty += ("({0:2d})" if self.numbers_checked[i + j] else " {0:2d} ").format(self.data[i + j])
            pretty += "|\n"
        pretty += "======================\n"
        return pretty
