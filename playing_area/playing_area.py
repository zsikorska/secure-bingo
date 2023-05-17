import config
from caller.caller import Caller
from citizen_card.fake_smart_card import SmartCard
from crypto.asymmetric.asymmetric_manager import AsymmetricManager
from crypto.asymmetric.signature_manager import SignatureManager
from game.logger_messages.logger_messages import LoggerMessages
from logger.logger import Logger
from mqtt.message.header import Header
from mqtt.message.message import Message
from mqtt.message.registration_message import RegistrationMessage
from mqtt.mqtt_client import MqttClient


class PlayingArea(MqttClient):
    def __init__(self, asymmetric_keys, asymmetric_manager: AsymmetricManager,
                 signature_manager: SignatureManager,
                 caller: Caller,
                 client_id: str,
                 logger: Logger) -> None:
        MqttClient.__init__(self, topic=config.PLAYING_AREA_QUEUE, client_id=client_id, on_message=self.on_message,
                            logger=logger)
        self.caller = caller
        self.logger = logger
        self.asymmetric_manager = asymmetric_manager
        self.signature_manager = signature_manager
        self.private_key = asymmetric_keys['private_key']
        self.public_key = asymmetric_keys['public_key']
        self.serialized_public_key = asymmetric_keys['serialized_public_key']
        self.is_registration_finished = False
        self.players_data = {}
        self.current_player_id = None
        self.current_player_index = 0
        self.current_deck_data = self.caller.deck.data

    def on_message(self, client, userdata, json_message) -> None:
        msg = Message(logger=self.logger)
        msg.deserialize(serialized_message=json_message.payload.decode('utf-8'))  # string --> object

        if msg.header == Header.REGISTRATION_DATA and not self.is_registration_finished:
            msg = RegistrationMessage(logger=self.logger)
            msg.deserialize(serialized_message=json_message.payload.decode('utf-8'))  # string --> object
            self.logger.info(owner=self.client_id, msg=LoggerMessages.received_registration_data(msg.addressee))
            if SmartCard.verify_signature(msg.signature, msg.data_as_bytes,
                                          msg.data['citizen_card_certificate'].public_key()):
                self.players_data[msg.addressee] = {}
                self.players_data[msg.addressee]['serialized_public_key'] = msg.data['serialized_public_key']
                self.players_data[msg.addressee]['citizen_card_certificate'] = msg.data['citizen_card_certificate']
                self.logger.info(owner=self.client_id, msg=LoggerMessages.signature_verified_citizen_card(msg.addressee))
                self.send_registration_data_response(recipient=msg.addressee)
            else:
                LoggerMessages.unverified_signature_info(cheater=msg.addressee)
                self.send_game_finished_requests(reason=f'unverified signature for {msg.addressee}.')
                self.running = False

            if len(self.players_data) == config.PLAYERS_AMOUNT:
                self.logger.info(owner=self.client_id, msg=LoggerMessages.all_players_registered_info())
                self.is_registration_finished = True
                self.current_player_id = list(self.players_data)[self.current_player_index]
                self.request_next_shuffle()

        if msg.header == Header.SHUFFLE_DONE:
            self.verify_signature(msg)
            self.current_deck_data = msg.data['deck_data']
            self.current_player_index += 1
            if self.current_player_index == config.PLAYERS_AMOUNT:
                self.logger.info(owner=self.client_id, msg=LoggerMessages.all_players_shuffled_info())
                self.current_player_index = 0
                self.current_player_id = list(self.players_data)[self.current_player_index]
                self.request_next_symmetric_keys()
            else:
                self.current_player_id = list(self.players_data)[self.current_player_index]
                self.request_next_shuffle()

        if msg.header == Header.SYMMETRIC_KEYS_SENT:
            self.verify_signature(msg)
            self.players_data[msg.addressee]['symmetric_key'] = msg.data['symmetric_key']
            self.players_data[msg.addressee]['symmetric_iv'] = msg.data['symmetric_iv']
            self.current_player_index += 1
            if self.current_player_index == config.PLAYERS_AMOUNT:
                self.logger.info(owner=self.client_id, msg=LoggerMessages.all_symmetric_keys_saved())
                self.current_player_index = 0
                self.current_player_id = list(self.players_data)[self.current_player_index]
                self.request_next_onion_decryption()
            else:
                self.current_player_id = list(self.players_data)[self.current_player_index]
                self.request_next_symmetric_keys()

        if msg.header == Header.DECRYPT_ONION_DONE:
            self.verify_signature(msg)
            if msg.data['is_legit']:
                self.logger.info(owner=msg.addressee, msg=LoggerMessages.decrypt_onion_legit_info(msg.addressee))
            else:
                self.logger.info(owner=self.client, msg=LoggerMessages.decrypt_onion_non_legit_info(msg.addressee))
                self.send_game_finished_requests(reason=f'unverified shuffle. Player who disagreed: {msg.addressee}.')
                self.running = False
            self.current_player_index += 1
            if self.current_player_index == config.PLAYERS_AMOUNT:
                self.logger.info(owner=self.client_id, msg=LoggerMessages.all_players_accept_shuffles_info())
                self.current_player_index = 0
                self.current_player_id = list(self.players_data)[self.current_player_index]
                self.call_current_number()
            else:
                self.current_player_id = list(self.players_data)[self.current_player_index]
                self.request_next_onion_decryption()

        if msg.header == Header.NEXT_NUMBER_UPDATED:
            self.verify_signature(msg)
            self.current_player_index += 1
            if self.current_player_index == config.PLAYERS_AMOUNT:
                self.current_player_index = 0
                self.current_player_id = list(self.players_data)[self.current_player_index]
                self.caller.update_next_number()
            else:
                self.current_player_id = list(self.players_data)[self.current_player_index]
            self.call_current_number()

        if msg.header == Header.BINGO:
            self.verify_signature(msg)
            self.logger.info(owner=self.client_id, msg=LoggerMessages.bingo_declared_info(msg.addressee))
            if msg.data['card'].check_bingo():
                self.logger.info(owner=self.client_id,
                                 msg=LoggerMessages.legit_bingo_info(winner=msg.addressee, card=msg.data['card']))
                self.send_game_finished_requests(reason=f'{msg.addressee} has BINGO and is the legit winner.')
            else:
                self.logger.info(owner=self.client_id,
                                 msg=LoggerMessages.non_legit_bingo_info(cheater=msg.addressee, card=msg.data['card']))
                self.send_game_finished_requests(reason=f'{msg.addressee} is a cheater!')
            self.running = False

    def send_message(self, msg: Message):
        serialized_and_signed_msg = msg.serialize_and_sign(private_key=self.private_key)  # object --> string
        self.client.publish(msg.topic, serialized_and_signed_msg)

    def verify_signature(self, msg: Message):
        if msg.verify_signature(message=msg.data_as_bytes,
                                serialized_public_key=self.players_data[msg.addressee]['serialized_public_key'],
                                signature=msg.signature):
            self.logger.info(owner=self.client_id, msg=LoggerMessages.signature_verified(msg.addressee))
        else:
            self.logger.error(owner=self.client_id, msg=LoggerMessages.signature_wrong(msg.addressee))
            self.send_game_finished_requests(reason=f'unverified signature for {msg.addressee}.')
            self.running = False

    def build_deck_data(self):
        return {'deck_data': self.current_deck_data}

    def build_registration_data(self):
        return {'serialized_public_key': self.serialized_public_key}

    def build_decrypt_onion_data(self):
        players_data = list()
        i = 0
        for player_id in reversed(self.players_data):  # reverse order allows to decrypt stacked encryptions
            players_data.append({})
            players_data[i]['symmetric_key'] = self.players_data[player_id]['symmetric_key']
            players_data[i]['symmetric_iv'] = self.players_data[player_id]['symmetric_iv']
            i += 1
        return {
            'deck_data': self.caller.deck.data,
            'onion_deck': self.current_deck_data,
            'players_data': players_data
        }

    def build_current_number_data(self):
        return {'next_number': self.caller.get_current_number()}

    def send_registration_data_response(self, recipient: str):
        self.logger.info(owner=self.client_id, msg=LoggerMessages.send_registration_data_response_info(recipient))
        self.send_message(msg=Message(
            topic=config.PLAYING_AREA_QUEUE,
            header=Header.REGISTRATION_DATA_RESPONSE,
            addressee=self.client_id,
            recipient=recipient,
            data=self.build_registration_data(),
            logger=self.logger
        ))

    def request_next_shuffle(self):
        self.logger.info(owner=self.client_id, msg=LoggerMessages.send_shuffle_request_info(
                             player_id=self.current_player_id,
                             player_index=self.current_player_index))
        self.send_message(msg=Message(
            topic=config.PLAYING_AREA_QUEUE,
            header=Header.SHUFFLE_REQUEST,
            addressee=self.client_id,
            recipient=self.current_player_id,
            data=self.build_deck_data(),
            logger=self.logger
        ))

    def request_next_symmetric_keys(self):
        self.logger.info(owner=self.client_id, msg=LoggerMessages.request_next_symmetric_keys_info(
                            player_id=self.current_player_id,
                            player_index=self.current_player_index))
        self.send_message(msg=Message(
            topic=config.PLAYING_AREA_QUEUE,
            header=Header.SYMMETRIC_KEYS_REQUEST,
            addressee=self.client_id,
            recipient=self.current_player_id,
            data={'key': 'sym'},
            logger=self.logger
        ))

    def request_next_onion_decryption(self):
        self.logger.info(owner=self.client_id, msg=LoggerMessages.request_next_onion_decryption_info(
                             player_id=self.current_player_id,
                             player_index=self.current_player_index))
        self.send_message(msg=Message(
            topic=config.PLAYING_AREA_QUEUE,
            header=Header.DECRYPT_ONION_REQUEST,
            addressee=self.client_id,
            recipient=self.current_player_id,
            data=self.build_decrypt_onion_data(),
            logger=self.logger
        ))

    def call_current_number(self):
        self.logger.info(owner=self.client_id,
                         msg=LoggerMessages.call_current_number_info(
                             player_id=self.current_player_id,
                             current_number=int.from_bytes(self.caller.get_current_number(), "little"),
                             current_number_index=self.caller.current_number_index
                         ))
        self.send_message(msg=Message(
            topic=config.PLAYING_AREA_QUEUE,
            header=Header.NEXT_NUMBER_CALLED,
            addressee=self.client_id,
            recipient=self.current_player_id,
            data=self.build_current_number_data(),
            logger=self.logger
        ))

    def send_game_finished_requests(self, reason: str):
        self.logger.info(owner=self.client_id, msg=LoggerMessages.send_game_finished_info())
        for player_id in self.players_data:
            self.send_message(msg=Message(
                topic=config.PLAYING_AREA_QUEUE,
                header=Header.GAME_FINISHED_REQUEST,
                addressee=self.client_id,
                recipient=player_id,
                data={'reason': reason},
                logger=self.logger
            ))
