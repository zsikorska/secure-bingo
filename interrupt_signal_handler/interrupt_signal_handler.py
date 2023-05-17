import signal

from logger.logger import Logger


class InterruptSignalHandler:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.SIGINT = False
        self.HARD_RESET = False
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        if self.SIGINT:
            self.logger.info("InterruptSignalHandler", 'signal_handler: COMBO!!! COMTROL + C         x2!\n')
            exit()
        self.logger.info("InterruptSignalHandler", 'SIGINT signal catched. You pressed CONTROL + C ! Exiting.')
        self.SIGINT = True
