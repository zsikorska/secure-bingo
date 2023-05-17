from enum import Enum


class Header(str, Enum):
    REGISTRATION_DATA = 'registration_data'
    REGISTRATION_DATA_RESPONSE = 'registration_data_response'
    SHUFFLE_REQUEST = 'shuffle_request'
    SHUFFLE_DONE = 'shuffle_done'
    SYMMETRIC_KEYS_REQUEST = 'symmetric_keys_request'
    SYMMETRIC_KEYS_SENT = 'symmetric_keys_sent'
    DECRYPT_ONION_REQUEST = 'decrypt_onion_request'
    DECRYPT_ONION_DONE = 'decrypt_onion_done'
    NEXT_NUMBER_CALLED = 'next_number_called'
    NEXT_NUMBER_UPDATED = 'next_number_updated'
    BINGO = 'bingo'
    GAME_FINISHED_REQUEST = 'game_finished_request'

