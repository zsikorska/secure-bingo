import json

import config
from citizen_card.fake_smart_card import SmartCard
from logger.logger import Logger
from mqtt.message.header import Header
from mqtt.message.message import Message


class RegistrationMessage(Message):
    def __init__(self, logger: Logger, data=None, addressee: str = None, recipient: str = None) -> None:
        super().__init__(topic=config.PLAYING_AREA_QUEUE,
                         header=Header.REGISTRATION_DATA,
                         addressee=addressee,
                         recipient=recipient,
                         data=data,
                         logger=logger)

    def serialize_and_sign(self, private_key=None, smart_card: SmartCard = None) -> str:
        self.data['serialized_public_key'] = self.data['serialized_public_key'].hex()           # bytes -> str
        self.data['citizen_card_certificate'] = self.data['citizen_card_certificate'].hex()   # bytes -> str
        self.data = json.dumps(self.data)                                                       # dict  -> str
        data_as_bytes = bytes(self.data, 'ascii')                                               # str -> bytes
        self.signature = smart_card.sign_message(data_as_bytes).hex()                           # bytes -> str
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)         # dict  -> str (this object)

    def deserialize(self, serialized_message: str) -> None:
        self.__dict__ = json.loads(serialized_message)                                          # str -> dict (this object)
        self.data_as_bytes = bytes(self.data, 'ascii')                                          # str -> bytes
        self.data = json.loads(self.data)                                                       # str -> dict
        self.signature = bytes.fromhex(self.signature)  # str -> bytes
        self.data['serialized_public_key'] = bytes.fromhex(self.data['serialized_public_key'])  # str -> bytes
        self.data['citizen_card_certificate'] = SmartCard.deserialize_certificate(
            bytes.fromhex(self.data['citizen_card_certificate']))  # str -> bytes
