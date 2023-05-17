

from player.player import Player
TEST_NAME = "-----TEST_DECK_ENCRYPTION-----"


def run(player : Player, deck_data, logger):
    logger.info("Test deck encrypt", f"\n\n\n{TEST_NAME}")
    encrypted_deck = player.encrypt_deck(deck_data=deck_data)
    logger.info("Encrypted deck", f'{encrypted_deck}')
    # todo decrypt onion 

    