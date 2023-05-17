TEST_NAME = "-----TEST_ASYMMETRIC_ENCRYPTION-----"


def run(player, asymmetric_manager, logger, message="This is a test for asymmetric encryption!"):
    logger.info("Test asymmetric encrypt", f"\n\n\n{TEST_NAME}")

    ciphertext = asymmetric_manager.encrypt(bytes(message, "UTF-8"), player.public_key)
    logger.info("Ciphertext", f"{ciphertext}")
    plaintext = asymmetric_manager.decrypt(ciphertext, player.private_key)
    logger.info("Plaintext", f"{plaintext}")
    logger.info("Original message", f"{message}")
