from caller.caller import Caller
from logger.logger import Logger
from playing_area.playing_area_factory import PlayingAreaFactory


class GameServer():
    def __init__(self, logger: Logger, ) -> None:
        self.running = True
        self.logger = logger
        self.playing_area_factory = PlayingAreaFactory()
        self.caller = Caller(logger=self.logger)
        self.playing_area = self.playing_area_factory.create(caller=self.caller)


if __name__ == '__main__':
    game_server = GameServer(Logger())
    game_server.playing_area.start()
