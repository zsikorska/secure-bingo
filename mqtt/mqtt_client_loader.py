from threading import Thread
import paho.mqtt.client as mqtt
from interrupt_signal_handler.interrupt_signal_handler import InterruptSignalHandler

from logger.logger import Logger


class MqttClientLoader(Thread):
    def __init__(self, mqtt_address: str, mqtt_port: int, client_id: str, logger: Logger) -> None:
        Thread.__init__(self)
        self.mqtt_address   = mqtt_address
        self.mqtt_port      = mqtt_port
        self.client_id      = client_id
        self.logger         = logger
        self.connected      = False
        self.interrupt_signal_handler    = InterruptSignalHandler(self.logger)
    
    def load_client(self, on_message=None):
        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.on_connect
        if on_message is not None:
            self.client.on_message = on_message
        self.client.connect(host=self.mqtt_address, port=self.mqtt_port)
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            self.logger.info(f'{self.client_id}', f'Mqtt Client connection successfull. RC = {rc}')
        else:
            self.logger.info(f'{self.client_id}', f'Mqtt Client connection failed. RC = {rc}')
    
    