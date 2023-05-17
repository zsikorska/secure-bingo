import config
from game.game_server.game_server import GameServer
from logger.logger import Logger
from player.nickname_generator.nickname_generator import NicknameGenerator
from player.player_factory import PlayerFactory


class ClientSimulator:
    def __init__(self) -> None:
        self.nickname_generator = NicknameGenerator()
        self.player_factory = PlayerFactory()
        self.players = self.create_players()

    def create_players(self):
        return [self.player_factory.create(nickname=self.nickname_generator.random_unique_nickname())
                for i in range(config.PLAYERS_AMOUNT)]

    def start_players(self):
        for player in self.players:
            player.start()

    def send_registration_data(self):
        for player in self.players:
            player.send_registration_message()

    def join_players(self):
        for player in reversed(self.players):
            player.join()


if __name__ == '__main__':
    game_server = GameServer(Logger())
    game_server.playing_area.start()

    client_simulator = ClientSimulator()
    client_simulator.start_players()

    client_simulator.send_registration_data()

    client_simulator.join_players()
