import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key


class SignatureManager:
    def __init__(self) -> None:
        pass

    def create_signature(self, message, private_key: RSAPrivateKey):
        if type(message) == str:
            message = bytes(message, 'ascii')

        signature = private_key.sign(message,
                                     padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                                     hashes.SHA256())
        return signature

    def verify_signature(self, message, signature: bytes, serialized_public_key: bytes):
        public_key = self._convert_bytes_key_to_object(serialized_public_key)
        try:
            public_key.verify(signature, message,
                              padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                              hashes.SHA256())
            return True
        except Exception:
            return False

    def sign_list(self, data, private_key: RSAPrivateKey):
        return self.create_signature(bytes(data), private_key)

    def verify_list(self, data, signature: bytes, serialized_public_key: bytes):
        return self.verify_signature(bytes(data), signature, serialized_public_key)

    def _convert_bytes_key_to_object(self, public_key_bytes: bytes) -> RSAPublicKey:
        """ deserialize the bytes key and recreate a public key object """
        return load_pem_public_key(public_key_bytes, backend=default_backend())
