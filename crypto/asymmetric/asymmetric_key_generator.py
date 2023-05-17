from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from game.logger_messages.logger_messages import LoggerMessages
from logger.logger import Logger


class AsymmetricKeyGenerator:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def _generate_private_key(self):
        return rsa.generate_private_key(public_exponent=65537, key_size=2048)

    def _generate_public_key(self, private_key):
        return private_key.public_key()

    def _generate_serialized_public_key(self, public_key):
        return public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)

    def generate_keys(self):
        self.logger.info(owner=self.__class__.__name__, msg=LoggerMessages.generate_keys_start_info())
        private_key = self._generate_private_key()
        public_key = self._generate_public_key(private_key)
        serialized_public_key = self._generate_serialized_public_key(public_key)
        self.logger.info(owner=self.__class__.__name__, msg=LoggerMessages.generate_keys_end_info())
        return {
            'private_key': private_key,
            'public_key': public_key,
            'serialized_public_key': serialized_public_key
        }
