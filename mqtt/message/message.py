import json

from citizen_card.fake_smart_card import SmartCard
from crypto.asymmetric.signature_manager import SignatureManager
from logger.logger import Logger
from mqtt.message.header import Header
from player.card.card import Card


class Message(SignatureManager):
    def __init__(self,
                 logger: Logger,
                 topic: str = None, data=None,
                 addressee: str = None, recipient: str = None, header: Header = None,
                 signature=None, ) -> None:
        self.topic = topic
        self.header = header
        self.addressee = addressee  # from
        self.recipient = recipient  # to
        self.data = data
        self.signature = signature
        self.logger = logger
        self.data_as_bytes = None

    def serialize_and_sign(self, private_key=None, smart_card: SmartCard = None) -> str:
        self.data = self.serialize_data()
        self.signature = self.create_signature(self.data, private_key).hex()  # bytes -> str
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)  # dict  -> str (this object)

    def deserialize(self, serialized_message: str) -> None:
        self.__dict__ = json.loads(serialized_message)  # str -> dict (this object)
        self.data_as_bytes = bytes(self.data, 'ascii')
        self.signature = bytes.fromhex(self.signature)  # str -> bytes
        self.data = self.deserialize_data()

    def serialize_data(self):
        serialized_data = self.data
        if 'serialized_public_key' in serialized_data:
            serialized_data['serialized_public_key'] = serialized_data['serialized_public_key'].hex()  # bytes -> str
        if 'deck_data' in serialized_data and type(serialized_data['deck_data'][0]) == bytes:
            serialized_data['deck_data'] = ' '.join(byte.hex() for byte in serialized_data['deck_data'])  # list[bytes] -> str
        if 'onion_deck' in serialized_data and type(serialized_data['onion_deck'][0]) == bytes:
            serialized_data['onion_deck'] = ' '.join(byte.hex() for byte in serialized_data['onion_deck'])  # list[bytes] -> str
        if 'symmetric_key' in serialized_data and 'symmetric_iv' in serialized_data:
            serialized_data['symmetric_key'] = serialized_data['symmetric_key'].hex()
            serialized_data['symmetric_iv'] = serialized_data['symmetric_iv'].hex()
        if 'players_data' in serialized_data and type(serialized_data['players_data'] == list):
            for i in range(len(serialized_data['players_data'])):
                serialized_data['players_data'][i]['symmetric_key'] = serialized_data['players_data'][i]['symmetric_key'].hex()
                serialized_data['players_data'][i]['symmetric_iv'] = serialized_data['players_data'][i]['symmetric_iv'].hex()
        if 'next_number' in serialized_data:
            serialized_data['next_number'] = serialized_data['next_number'].hex()
        if 'card' in serialized_data:
            serialized_data['card'] = json.dumps(serialized_data["card"].dict())
        return json.dumps(serialized_data)  # dict  -> str

    def deserialize_data(self):
        deserialized_data = json.loads(self.data)  # str -> dict
        if 'serialized_public_key' in deserialized_data:
            deserialized_data['serialized_public_key'] = bytes.fromhex(deserialized_data['serialized_public_key'])  # str -> bytes
        if 'deck_data' in deserialized_data:
            deserialized_data['deck_data'] = [bytes.fromhex(num_str) for num_str in deserialized_data['deck_data'].split(' ')]  # str -> list[bytes]
        if 'onion_deck' in deserialized_data:
            deserialized_data['onion_deck'] = [bytes.fromhex(num_str) for num_str in deserialized_data['onion_deck'].split(' ')]  # str -> list[bytes]
        if 'symmetric_key' in deserialized_data and 'symmetric_iv' in deserialized_data:
            deserialized_data['symmetric_key'] = bytes.fromhex(deserialized_data['symmetric_key'])  # str -> bytes
            deserialized_data['symmetric_iv'] = bytes.fromhex(deserialized_data['symmetric_iv'])  # str -> bytes
        if 'players_data' in deserialized_data and type(deserialized_data['players_data'] == list):
            for i in range(len(deserialized_data['players_data'])):  #
                deserialized_data['players_data'][i]['symmetric_key'] = bytes.fromhex(deserialized_data['players_data'][i]['symmetric_key'])
                deserialized_data['players_data'][i]['symmetric_iv'] = bytes.fromhex(deserialized_data['players_data'][i]['symmetric_iv'])
        if 'next_number' in deserialized_data:
            deserialized_data['next_number'] = int.from_bytes(bytes.fromhex(deserialized_data['next_number']), 'little')
        if 'card' in deserialized_data:
            deserialized_data['card'] = Card.from_dict(json.loads(deserialized_data["card"]))
        return deserialized_data

    def pretty(self):
        return f'''
            topic: {self.topic},
            header: {self.header},
            addressee: {self.addressee}, 
            recipient: {self.recipient},
            data[type: {type(self.data)}]: {self.data},
            signature[type: {type(self.signature)}]: {self.signature}
            '''
