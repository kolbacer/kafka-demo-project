import asyncio
import logging
import os
import aiokafka

import service_app.worker.tasks.get_new_burgers as cooking_task
import service_app.worker.tasks.get_burger_orders as consumption_task

# env variables
KAFKA_COOKING_TOPIC = os.getenv('KAFKA_COOKING_TOPIC', "cooking")
KAFKA_CONSUMPTION_TOPIC = os.getenv('KAFKA_CONSUMPTION_TOPIC', "consumption")
KAFKA_NOTIFICATION_TOPIC = os.getenv('KAFKA_NOTIFICATION_TOPIC', "notification")
KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP_PREFIX', 'service_group')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# global variables
cooking_consumer = None
consumption_consumer = None
notification_producer = None
cooking_consumer_task = None
consumption_consumer_task = None

log = logging.getLogger(__name__)


async def get_cooking_consumer():
    if cooking_consumer is not None:
        return cooking_consumer

    group_id = f'{KAFKA_CONSUMER_GROUP}'
    log.debug(f'Initializing KafkaConsumer for topic {KAFKA_COOKING_TOPIC}, group_id {group_id}'
              f' and using bootstrap servers {KAFKA_BOOTSTRAP_SERVERS}')
    _cooking_consumer = aiokafka.AIOKafkaConsumer(KAFKA_COOKING_TOPIC,
                                                  bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                                  group_id=group_id)
    await _cooking_consumer.start()
    return _cooking_consumer


async def get_consumption_consumer():
    if consumption_consumer is not None:
        return consumption_consumer

    group_id = f'{KAFKA_CONSUMER_GROUP}'
    log.debug(f'Initializing KafkaConsumer for topic {KAFKA_CONSUMPTION_TOPIC}, group_id {group_id}'
              f' and using bootstrap servers {KAFKA_BOOTSTRAP_SERVERS}')
    _consumption_consumer = aiokafka.AIOKafkaConsumer(KAFKA_CONSUMPTION_TOPIC,
                                                      bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                                      group_id=group_id)
    await _consumption_consumer.start()
    return _consumption_consumer


async def get_notification_producer():
    if notification_producer is not None:
        return notification_producer

    log.debug(f'Initializing KafkaProducer for topic {KAFKA_NOTIFICATION_TOPIC}'
              f' and using bootstrap servers {KAFKA_BOOTSTRAP_SERVERS}')
    _notification_producer = aiokafka.AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await _notification_producer.start()
    return _notification_producer


async def get_cooking_consumer_task(consumer):
    if cooking_consumer_task is not None:
        return cooking_consumer_task
    else:
        return asyncio.create_task(cooking_task.on_burger_make(consumer))


async def get_consumption_consumer_task(consumer):
    if consumption_consumer_task is not None:
        return consumption_consumer_task
    else:
        return asyncio.create_task(consumption_task.on_burger_eat(consumer))


async def initialize():
    global cooking_consumer, consumption_consumer, notification_producer, \
        cooking_consumer_task, consumption_consumer_task
    cooking_consumer = await get_cooking_consumer()
    consumption_consumer = await get_consumption_consumer()
    notification_producer = await get_notification_producer()
    cooking_consumer_task = await get_cooking_consumer_task(cooking_consumer)
    consumption_consumer_task = await get_consumption_consumer_task(consumption_consumer)


async def stop():
    cooking_consumer_task.cancel()
    consumption_consumer_task.cancel()
    await cooking_consumer.stop()
    await consumption_consumer.stop()
    await notification_producer.stop()
