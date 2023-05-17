import config
from citizen_card.fake_smart_card import SmartCard
from crypto.asymmetric.asymmetric_manager import AsymmetricManager
from crypto.asymmetric.signature_manager import SignatureManager
from crypto.symmetric.symmetric_manager import SymmetricManager
from game.logger_messages.logger_messages import LoggerMessages
from logger.logger import Logger
from mqtt.message.header import Header
from mqtt.message.message import Message
from mqtt.message.registration_message import RegistrationMessage
from mqtt.mqtt_client import MqttClient
from player.card.card import Card
from player.cheat_module.cheat_module import CheatModule


class Player(MqttClient):
    def __init__(self, nickname,
                 asymmetric_keys, asymmetric_manager: AsymmetricManager,
                 symmetric_key_pair, symmetric_manager: SymmetricManager,
                 signature_manager: SignatureManager, smart_card: SmartCard,
                 cheat_module: CheatModule,
                 logger: Logger):
        MqttClient.__init__(self, topic=config.PLAYING_AREA_QUEUE, client_id=f'player_{nickname}',
                            on_message=self.on_message, logger=logger)
        self.cheat_module = cheat_module
        self.symmetric_manager = symmetric_manager
        self.asymmetric_manager = asymmetric_manager
        self.signature_manager = signature_manager
        self.nickname = nickname
        self.private_key = asymmetric_keys['private_key']
        self.public_key = asymmetric_keys['public_key']
        self.serialized_public_key = asymmetric_keys['serialized_public_key']
        self.symmetric_key = symmetric_key_pair['symmetric_key']
        self.symmetric_iv = symmetric_key_pair['iv']
        self.card = Card()
        self.smart_card = smart_card
        self.playing_area_data = {}

    def send_message(self, msg: Message):
        serialized_and_signed_msg = msg.serialize_and_sign(private_key=self.private_key)  # object --> string
        self.client.publish(msg.topic, serialized_and_signed_msg)

    def send_registration_message(self):
        self.smart_card.load_session()
        msg = RegistrationMessage(
            addressee=self.client_id,
            recipient=config.PLAYING_AREA,
            data=self.build_registration_data(),
            logger=self.logger
        )
        serialized_msg = msg.serialize_and_sign(smart_card=self.smart_card)  # object --> string
        self.smart_card.logout()
        self.client.publish(msg.topic, serialized_msg)

    def on_message(self, client, userdata, json_message) -> None:
        msg = Message(logger=self.logger)
        msg.deserialize(serialized_message=json_message.payload.decode('utf-8'))  # string --> object
        if msg.recipient == self.client_id and msg.addressee == config.PLAYING_AREA:  # filter this player, listen only to playing area
            if msg.header == Header.REGISTRATION_DATA_RESPONSE:
                self.logger.info(owner=self.client_id, msg=LoggerMessages.received_registration_response())
                self.playing_area_data['serialized_public_key'] = msg.data['serialized_public_key']

            if msg.header == Header.SHUFFLE_REQUEST:
                self.verify_signature(msg)
                self.logger.info(owner=self.client_id, msg=LoggerMessages.received_shuffle_request())
                onion_layer = self.build_encrypted_deck_data(deck_data=msg.data['deck_data'])
                self.send_shuffle_done_message(onion_layer=onion_layer)

            if msg.header == Header.SYMMETRIC_KEYS_REQUEST:
                self.verify_signature(msg)
                self.logger.info(owner=self.client_id, msg=LoggerMessages.received_symmetric_keys_request())
                self.send_symmetric_keys()

            if msg.header == Header.DECRYPT_ONION_REQUEST:
                self.verify_signature(msg)
                is_legit = self.verify_onion_deck(deck_data=msg.data['deck_data'],
                                                  onion_deck=msg.data['onion_deck'],
                                                  players_data=msg.data['players_data'])
                self.logger.info(owner=self.client_id, msg=LoggerMessages.received_decrypt_onion_request())
                self.send_decrypt_onion_done_message(is_legit=is_legit)

            if msg.header == Header.NEXT_NUMBER_CALLED:
                self.verify_signature(msg)
                self.logger.info(owner=self.client_id, msg=LoggerMessages.received_next_number_called(msg.data["next_number"]))
                self.card.update(msg.data['next_number'])
                if self.check_bingo():
                    self.logger.info(owner=self.client_id, msg=LoggerMessages.call_bingo_info())
                    self.call_bingo()
                else:
                    self.send_next_number_updated()

            if msg.header == Header.GAME_FINISHED_REQUEST:
                self.verify_signature(msg)
                self.logger.info(owner=self.client_id, msg=LoggerMessages.received_game_finished_request(msg.data['reason']))
                self.running = False

    def check_bingo(self):
        if self.card.check_bingo():  # is there a bingo?
            return True
        if self.cheat_module.is_cheat_decision(chance=config.PLAYER_CHEAT_CHANCE):  # is the player unsportsmanlike?
            return True
        return False

    def verify_onion_deck(self, deck_data, onion_deck, players_data):
        decrypted_deck_bytes = self.symmetric_manager.decrypt_onion_deck(onion_deck, players_data)
        if decrypted_deck_bytes == deck_data:
            return True
        return False

    def call_bingo(self):
        self.send_message(msg=Message(
            topic=config.PLAYING_AREA_QUEUE,
            header=Header.BINGO,
            addressee=self.client_id,
            recipient=config.PLAYING_AREA,
            data=self.build_bingo_data(),
            logger=self.logger
        ))

    def send_next_number_updated(self):
        self.send_message(msg=Message(
            topic=config.PLAYING_AREA_QUEUE,
            header=Header.NEXT_NUMBER_UPDATED,
            addressee=self.client_id,
            recipient=config.PLAYING_AREA,
            data={'updated': 'true'},
            logger=self.logger
        ))

    def send_decrypt_onion_done_message(self, is_legit: bool):
        self.send_message(msg=Message(
            topic=config.PLAYING_AREA_QUEUE,
            header=Header.DECRYPT_ONION_DONE,
            addressee=self.client_id,
            recipient=config.PLAYING_AREA,
            data={'is_legit': is_legit},
            logger=self.logger
        ))

    def send_symmetric_keys(self):
        self.send_message(msg=Message(
            topic=config.PLAYING_AREA_QUEUE,
            header=Header.SYMMETRIC_KEYS_SENT,
            addressee=self.client_id,
            recipient=config.PLAYING_AREA,
            data=self.build_symmetric_keys_data(),
            logger=self.logger
        ))

    def send_shuffle_done_message(self, onion_layer):
        self.send_message(msg=Message(
            topic=config.PLAYING_AREA_QUEUE,
            header=Header.SHUFFLE_DONE,
            addressee=self.client_id,
            recipient=config.PLAYING_AREA,
            data=onion_layer,
            logger=self.logger
        ))

    def encrypt_deck(self, deck_data: list) -> list:
        return self.symmetric_manager.encrypt_list(deck_data, self.symmetric_key, self.symmetric_iv)

    def build_bingo_data(self):
        return {'card': self.card}

    def build_registration_data(self):
        return {
            'serialized_public_key': self.serialized_public_key,
            'citizen_card_certificate': self.smart_card.get_certificate_serialized()
        }

    def build_encrypted_deck_data(self, deck_data):
        return {'deck_data': self.encrypt_deck(deck_data=deck_data)}

    def build_symmetric_keys_data(self):
        return {
            'symmetric_key': self.symmetric_key,
            'symmetric_iv': self.symmetric_iv
        }

    def verify_signature(self, msg: Message):
        if msg.verify_signature(message=msg.data_as_bytes,
                                serialized_public_key=self.playing_area_data['serialized_public_key'],
                                signature=msg.signature):
            self.logger.info(owner=self.client_id, msg=LoggerMessages.signature_verified(msg.addressee))
        else:
            self.logger.error(owner=self.client_id, msg=LoggerMessages.signature_wrong(msg.addressee))
