import json
import logging

import burger_service.worker as worker
import burger_service.db as db

log = logging.getLogger(__name__)


async def on_burger_make(consumer):
    try:
        async for msg in consumer:
            log.info(f"Message consumed: {msg}")
            burger = json.loads(msg.value)
            added = await db.add_burger(burger_name=burger["name"], burger_price=burger["price"])
            if added:
                message = f'New burger "{burger["name"]}" for only {burger["price"]}$ is available now!'
                notification_producer = await worker.get_notification_producer()
                await notification_producer.send_and_wait(worker.KAFKA_NOTIFICATION_TOPIC,
                                                          json.dumps({"message": message}).encode('utf-8'))
    finally:
        log.warning('Stopping consumer')
        await consumer.stop()
