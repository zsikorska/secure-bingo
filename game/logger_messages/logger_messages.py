import config
from player.card.card import Card


class LoggerMessages:
    def __init__(self):
        pass

    @staticmethod
    def unverified_signature_info(cheater: str):
        return f'Could not verify signature for: {cheater}. Player is not trusted.'

    @staticmethod
    def unverified_shuffle_info():
        return f'Does not trust the shuffling - onion decryption did not match.'

    @staticmethod
    def non_legit_bingo_info(cheater: str, card: Card):
        return f'{cheater} announced himself a winner, it turns out this player is a cheater! His card was:\n\n{card.pretty()}.'

    @staticmethod
    def legit_bingo_info(winner: str, card: Card):
        return f'{winner} is the legit WINNER! His card was:\n\n{card.pretty()}.'

    @staticmethod
    def received_registration_response():
        return 'Received registration confirmation.'

    @staticmethod
    def received_shuffle_request():
        return f"Received shuffling request. Shuffling the deck."

    @staticmethod
    def signature_verified(addressee: str):
        return f'Signature confirmed for {addressee}.'

    @staticmethod
    def signature_wrong(addressee: str):
        return f'Signature wrong for {addressee}.'

    @staticmethod
    def received_next_number_called(next_number: int):
        return f'I am checking number {next_number}.'

    @staticmethod
    def received_game_finished_request(reason: str):
        return f'Received game finished request, reason: {reason}. Exiting.'

    @staticmethod
    def call_bingo_info():
        return f'I have bingo...'

    @staticmethod
    def received_decrypt_onion_request():
        return 'Received decrypt onion request. Decrypting and sending the result back.'

    @staticmethod
    def received_symmetric_keys_request():
        return 'Received symmetric keys request.'

    @staticmethod
    def received_registration_data(addressee: str):
        return f'Registration data received from: {addressee}.'

    @staticmethod
    def signature_verified_citizen_card(addressee: str):
        return f'Signature confirmed for {addressee} | Player registered.'

    @staticmethod
    def all_players_registered_info():
        return f'All players({config.PLAYERS_AMOUNT}) registered successfully.'

    @staticmethod
    def all_players_shuffled_info():
        return f'All players shuffled the deck: {config.PLAYERS_AMOUNT}.'

    @staticmethod
    def all_symmetric_keys_saved():
        return f'All players\' symmetric keys have been saved: {config.PLAYERS_AMOUNT}.'

    @staticmethod
    def all_players_accept_shuffles_info():
        return f'All players\'({config.PLAYERS_AMOUNT}) accepted shuffled deck.'

    @staticmethod
    def decrypt_onion_legit_info(addressee: str):
        return f'Accepted shuffled deck, player source: {addressee}.'

    @staticmethod
    def decrypt_onion_non_legit_info(addressee: str):
        return f'Did not accept shuffled deck, player source: {addressee}'

    @staticmethod
    def bingo_declared_info(addressee: str):
        return f'{addressee} claims (s)he has BINGO. Checking his card.'

    @staticmethod
    def send_registration_data_response_info(recipient: str):
        return f'Sending registration data response to: {recipient}.'

    @staticmethod
    def send_shuffle_request_info(player_id: str, player_index: int):
        return f'Sending shuffle request to: {player_id}[{player_index}]'

    @staticmethod
    def send_game_finished_info():
        return f'Sending game finished requests to all players.'

    @staticmethod
    def call_current_number_info(player_id: str, current_number_index: int, current_number: int):
        return f'Messaging player {player_id} about call nr[{current_number_index}]: {current_number}!'

    @staticmethod
    def request_next_onion_decryption_info(player_id: str, player_index: int):
        return f'Sending verify decrypt onion request to: {player_id}[{player_index}].'

    @staticmethod
    def request_next_symmetric_keys_info(player_id: str, player_index: int):
        return f'Requesting symmetric keys from: {player_id}[{player_index}].'

    @staticmethod
    def generate_keys_start_info():
        return 'Generating keys...'

    @staticmethod
    def generate_keys_end_info():
        return 'Keys generated successfully.'
