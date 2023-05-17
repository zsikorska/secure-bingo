import config
from caller.caller import Caller
from crypto.asymmetric.asymmetric_key_generator import AsymmetricKeyGenerator
from crypto.asymmetric.asymmetric_manager import AsymmetricManager
from crypto.asymmetric.signature_manager import SignatureManager
from crypto.symmetric.symmetric_key_generator import SymmetricKeyGenerator
from logger.logger import Logger
from playing_area.playing_area import PlayingArea


class PlayingAreaFactory():
    def __init__(self) -> None:
        self.logger = Logger()
        self.asymmetric_manager = AsymmetricManager()
        self.asymmetric_key_generator = AsymmetricKeyGenerator(self.logger)
        self.symmetric_key_generator = SymmetricKeyGenerator()
        self.signature_manager = SignatureManager()

    def create(self, caller: Caller):
        return PlayingArea(caller=caller,
                           asymmetric_manager=self.asymmetric_manager, signature_manager=self.signature_manager,
                           asymmetric_keys=self.asymmetric_key_generator.generate_keys(),
                           client_id=config.PLAYING_AREA,
                           logger=self.logger)
