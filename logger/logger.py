import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(message)s')


class Logger:
    def __init__(self) -> None:
        self.info("Logger", "__________________________________")
        self.info("Logger", "Started new Logger session. Hello!")

    def info(self, owner, msg) -> None:
        logging.info(f'{owner}: {msg}')

    def error(self, owner, msg) -> None:
        logging.error(f'{owner}: {msg}')
