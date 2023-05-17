import os


class SymmetricKeyGenerator():
    def __init__(self) -> None:
        self.symmetric_key_len = 32
        self.iv_len = 16
        

    def _generate_symmetric_key(self):
        return os.urandom(self.symmetric_key_len) 

    def _generate_initialization_vector(self):
        return os.urandom(self.iv_len)    

    def generate_key_pair(self):
        key_pair = {}
        key_pair['symmetric_key'] = self._generate_symmetric_key()
        key_pair['iv'] =   self._generate_initialization_vector()
        return key_pair
        