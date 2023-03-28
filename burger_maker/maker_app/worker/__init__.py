import logging
import os
import aiokafka

# env variables
KAFKA_COOKING_TOPIC = os.getenv('KAFKA_COOKING_TOPIC', "cooking")
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# global variables
cooking_producer = None

log = logging.getLogger(__name__)


async def get_cooking_producer():
    if cooking_producer is not None:
        return cooking_producer

    log.debug(f'Initializing KafkaProducer for topic {KAFKA_COOKING_TOPIC}'
              f' and using bootstrap servers {KAFKA_BOOTSTRAP_SERVERS}')
    _cooking_producer = aiokafka.AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await _cooking_producer.start()
    return _cooking_producer


async def initialize():
    global cooking_producer
    cooking_producer = await get_cooking_producer()


async def stop():
    await cooking_producer.stop()
