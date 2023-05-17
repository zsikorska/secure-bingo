import time
import uuid
from mqtt.dto.message import Message

TEST_NAME = '----TEST_MQTT----'


def spam_messages(client1, topic: str):
    cnt = 0
    while cnt < 10:
        client1.send_message(Message(topic=topic, data=f'Message {str(cnt)}: {str(uuid.uuid4())}'))
        time.sleep(.2)
        cnt += 1


def run(logger, client1, client2):
    logger.info("Test mqtt", f"\n\n\n{TEST_NAME}")
    client1.start()
    client2.start()

    spam_messages(client1=client1, topic='test')

    client2.running = False
    client1.running = False
    client2.join()
    client1.join()
