import os
import aiokafka
import asyncio
import logging

import burger_customer.worker.tasks.get_notifications as notification_task

# env variables
KAFKA_CONSUMPTION_TOPIC = os.getenv('KAFKA_CONSUMPTION_TOPIC', "consumption")
KAFKA_NOTIFICATION_TOPIC = os.getenv('KAFKA_NOTIFICATION_TOPIC', "notification")
KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP', 'customer_group')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# global variables
notification_consumer = None
consumption_producer = None
notification_consumer_task = None

log = logging.getLogger(__name__)


async def get_notification_consumer():
    if notification_consumer is not None:
        return notification_consumer

    group_id = f'{KAFKA_CONSUMER_GROUP}'
    log.debug(f'Initializing KafkaConsumer for topic {KAFKA_NOTIFICATION_TOPIC}, group_id {group_id}'
              f' and using bootstrap servers {KAFKA_BOOTSTRAP_SERVERS}')
    _notification_consumer = aiokafka.AIOKafkaConsumer(KAFKA_NOTIFICATION_TOPIC,
                                                       bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                                       group_id=group_id)
    await _notification_consumer.start()
    return _notification_consumer


async def get_consumption_producer():
    if consumption_producer is not None:
        return consumption_producer

    log.debug(f'Initializing KafkaProducer for topic {KAFKA_CONSUMPTION_TOPIC}'
              f' and using bootstrap servers {KAFKA_BOOTSTRAP_SERVERS}')
    _consumption_producer = aiokafka.AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await _consumption_producer.start()
    return _consumption_producer


async def get_notification_consumer_task(consumer):
    if notification_consumer_task is not None:
        return notification_consumer_task
    else:
        return asyncio.create_task(notification_task.on_notification(consumer))


async def initialize():
    global notification_consumer, consumption_producer, notification_consumer_task
    notification_consumer = await get_notification_consumer()
    consumption_producer = await get_consumption_producer()
    notification_consumer_task = await get_notification_consumer_task(notification_consumer)


async def stop():
    notification_consumer_task.cancel()
    await notification_consumer.stop()
    await consumption_producer.stop()
