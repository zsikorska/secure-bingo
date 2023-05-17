import test_card_signature, test_onion
from caller.caller import Caller
from crypto.asymmetric.asymmetric_key_generator import AsymmetricKeyGenerator
from crypto.asymmetric.asymmetric_manager import AsymmetricManager
from crypto.asymmetric.signature_manager import SignatureManager
from crypto.symmetric.symmetric_key_generator import SymmetricKeyGenerator
from crypto.symmetric.symmetric_manager import SymmetricManager
from logger.logger import Logger
from player.player import Player
from player.player_factory import PlayerFactory

logger                      = Logger()
symmetric_manager           = SymmetricManager(logger = logger)
asymmetric_manager          = AsymmetricManager()
asymmetric_key_generator    = AsymmetricKeyGenerator()
symmetric_key_generator     = SymmetricKeyGenerator()
signature_manager           = SignatureManager()
caller                      = Caller(logger=logger)
player_factory = PlayerFactory()
playerA  = player_factory.create('Hans')
playerB = player_factory.create('user_testowy')


def main():
    # test_mqtt.run(logger=logger, client1=MqttClient(topic='test', client_type=MqttClientType.PLAYING_AREA, logger=logger), client2=MqttClient(topic='test', client_type=MqttClientType.PLAYER, logger=logger))
    # test_asymmetric_encryption.run(player=playerA, asymmetric_manager=asymmetric_manager, logger=logger)
    # test_card_signature.run(player_a=playerA, player_b=playerB, logger=logger)
    # test_deck_encryption.run(player=playerA, deck_data=caller.deck.data, logger=logger)
    test_onion.run(player_factory, deck_data=caller.deck.data, logger=logger)
    

if __name__ == '__main__':
    main()
