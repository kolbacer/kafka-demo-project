import json
import logging

import service_app.worker as worker
import service_app.db as db

log = logging.getLogger(__name__)


async def on_burger_eat(consumer):
    try:
        async for msg in consumer:
            log.info(f"Message consumed: {msg}")
            burger_order = json.loads(msg.value)
            await db.add_order(burger_name=burger_order["burger_name"],
                               customer_name=burger_order["customer_name"])
            toEat = await db.get_burger_by_name(burger_order["burger_name"])
            message = ""
            if toEat is None:
                message = f'Sorry, burger "{burger_order["burger_name"]}" not found'
            elif toEat.owner is not None:
                message = f'Sorry, burger "{burger_order["burger_name"]}" was already eaten by {toEat.owner}'
            else:
                await db.set_burger_owner(burger_name=burger_order["burger_name"],
                                          customer_name=burger_order["customer_name"])
                message = "Your burger, sir. Bon Appetit!"
            notification_producer = await worker.get_notification_producer()
            await notification_producer.send_and_wait(worker.KAFKA_NOTIFICATION_TOPIC,
                                                      json.dumps({"message": message}).encode('utf-8'))
    finally:
        log.warning('Stopping consumer')
        await consumer.stop()
