
from logger.logger import Logger
from player.player import Player
TEST_NAME = "-----TEST_CARD_SIGNATURE-----"


def run(player_a: Player, player_b: Player, logger: Logger):
    logger.info("Test card signature", f"\n\n\n{TEST_NAME}")

    signature = player_a.signature_manager.create_signature('message', player_a.private_key)
    is_signature_legit = player_a.signature_manager.verify_signature('message', signature, player_a.serialized_public_key)
    
    logger.info("card_A_signature", f"{signature}")
    if is_signature_legit:
        logger.info("Test card signature", "This card has not been altered :D")
    else:
        logger.info("Test card signature", "This card has been altered! Attention !!! :(")
