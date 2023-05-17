from player.player_factory import PlayerFactory
from logger.logger import Logger

TEST_NAME = "-----TEST_ONION-----"


def run(player_factory: PlayerFactory, deck_data: list, logger: Logger):
    logger.info("", f"\n\n\n{TEST_NAME} 0000")
    PLAYERS_AMOUNT = 4

    # create players
    players = []
    for i in range(PLAYERS_AMOUNT):
        players.append(player_factory.create(f'player_{i}'))

    # encrypt onion
    onion_deck = deck_data
    for player in players:
        onion_deck = player.encrypt_deck(deck_data=onion_deck)

    # get players keys
    players_keys = []
    for player in players:
        players_keys.insert(0, {'symmetric_key': player.symmetric_key, 'symmetric_iv': player.symmetric_iv})

    # decrypt onion
    for player in players:
        if player.verify_onion_deck(deck_data=deck_data, onion_deck=onion_deck, players_data=players_keys):
            logger.info("Test onion", f"{player.nickname} confirms shuffling!")
        else:
            logger.info("Test onion", f"{player.nickname} rejects shuffling!")
