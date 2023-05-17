from player.nickname_generator.nickname_generator import NicknameGenerator
from player.player_factory import PlayerFactory


class Client:
    def __init__(self) -> None:
        self.nickname_generator = NicknameGenerator()
        self.player_factory = PlayerFactory()
        self.player = self.player_factory.create(nickname=self.nickname_generator.random_unique_nickname())


if __name__ == '__main__':
    client = Client()
    client.player.start()
    client.player.send_registration_message()
    client.player.join()
