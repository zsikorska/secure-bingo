from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class AsymmetricManager():
    def __init__(self) -> None:
        pass

    def encrypt(self,message,public_key):
        return public_key.encrypt(message,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

    def decrypt(self,ciphertext,private_key):
        return private_key.decrypt(ciphertext,padding.OAEP (mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
