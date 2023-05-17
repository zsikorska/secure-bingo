from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import padding
from logger.logger import Logger
import config as config

class SymmetricManager:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def encrypt(self, message, key, iv):
        cipher      = Cipher(algorithms.AES(key), modes.CBC(iv))
        padder      = padding.PKCS7(config.PKCS7_BLOCK_SIZE).padder()
        padded_data = padder.update(message)
        padded_data += padder.finalize()
        return cipher.encryptor().update(padded_data) + cipher.encryptor().finalize()

    def decrypt(self, ciphertext, key, iv):
        cipher      = Cipher(algorithms.AES(key), modes.CBC(iv))
        padded_data = cipher.decryptor().update(ciphertext)
        padded_data += cipher.decryptor().finalize()
        unpadder    = padding.PKCS7(config.PKCS7_BLOCK_SIZE).unpadder()
        unpadded_data = unpadder.update(padded_data)
        unpadded_data += unpadder.finalize()
        return unpadded_data

    def encrypt_list(self, deck_data: list, symmetric_key, symmetric_iv) -> list:
        encrypted_list = []
        if type(deck_data[0]) is bytes:
            for byte in deck_data:
                encrypted_list.append(self.encrypt(byte, symmetric_key, symmetric_iv))
        else:
            for num in deck_data:
                encrypted_list.append(self.encrypt(num.to_bytes(2, 'little'), symmetric_key, symmetric_iv))
        return encrypted_list

    def decrypt_list(self, encrypted_deck, symmetric_key, symmetric_iv):
        decrypted_list = []
        for number in encrypted_deck:
            decrypted_list.append(self.decrypt(number, symmetric_key, symmetric_iv))
        return decrypted_list

    def decrypt_onion_deck(self, onion_deck: list, players_data: list):
        for i in range(len(players_data)):
            onion_deck = self.decrypt_list(onion_deck, players_data[i]['symmetric_key'], players_data[i]['symmetric_iv'])
        return onion_deck

