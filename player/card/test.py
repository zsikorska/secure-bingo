from player.card.card import Card

card = Card()

card.data = [
    1,   2,  3,  4,  5,
    12, 14, 16, 18, 19,
    21, 22, 23, 24, 25,
    31, 42, 43, 44, 45,
    51, 62, 63, 74, 85
]

numbers = [
    # 1,   2,  3,  4,  5,
    # 1, 14, 23, 44, 85
    1, 12, 21, 31, 51
]
#
for i in numbers:
    card.update(i)

# print(card.check_bingo())

print(card.numbers_checked)

import json

v = json.dumps(card.dict())

print(v)

c2 = Card.from_dict(json.loads(v))

print(c2.data)
print(c2.numbers_checked)