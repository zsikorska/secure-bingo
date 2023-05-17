import config
from citizen_card.fake_smart_card import SmartCard
from crypto.asymmetric.asymmetric_key_generator import AsymmetricKeyGenerator
from crypto.asymmetric.asymmetric_manager import AsymmetricManager
from crypto.asymmetric.signature_manager import SignatureManager
from crypto.symmetric.symmetric_key_generator import SymmetricKeyGenerator
from crypto.symmetric.symmetric_manager import SymmetricManager
from logger.logger import Logger
from player.cheat_module.cheat_module import CheatModule
from player.player import Player


class PlayerFactory():
    def __init__(self) -> None:
        self.logger = Logger()
        self.symmetric_manager = SymmetricManager(logger=self.logger)
        self.asymmetric_manager = AsymmetricManager()
        self.asymmetric_key_generator = AsymmetricKeyGenerator(logger=self.logger)
        self.symmetric_key_generator = SymmetricKeyGenerator()
        self.signature_manager = SignatureManager()
        self.cheat_module = CheatModule()

    def create(self, nickname):
        return Player(nickname=nickname,
                      symmetric_manager=self.symmetric_manager,
                      symmetric_key_pair=self.symmetric_key_generator.generate_key_pair(),
                      asymmetric_manager=self.asymmetric_manager,
                      asymmetric_keys=self.asymmetric_key_generator.generate_keys(),
                      signature_manager=self.signature_manager,
                      smart_card=SmartCard(pin=config.DEFAULT_CITIZEN_CARD_PIN,
                                           keys=self.asymmetric_key_generator.generate_keys(),
                                           signature_manager=self.signature_manager,
                                           logger=self.logger),
                      cheat_module=self.cheat_module,
                      logger=self.logger)
