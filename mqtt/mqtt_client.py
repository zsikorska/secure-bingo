
import time

import config
from logger.logger import Logger
from mqtt.mqtt_client_loader import MqttClientLoader


class MqttClient(MqttClientLoader):
    def __init__(self, topic : str, client_id, on_message, logger : Logger) -> None:
        MqttClientLoader.__init__(self, config.MQTT_ADDRESS, config.MQTT_PORT, client_id, logger)
        self.load_client(on_message=on_message)
        self.topic = topic
        self.client.subscribe(self.topic)
        self.running = True
      
    def run(self):
        self.client.loop_start()
        self.logger.info(f'{self.client_id}', f'Started successfully, topic: {self.topic}')
        while self.running:
            if self.interrupt_signal_handler.SIGINT:
                self.running = False
                break
            time.sleep(.1)
        self.client.loop_stop()
        self.logger.info(owner=self.client_id, msg=f"Exited successfully.")

    