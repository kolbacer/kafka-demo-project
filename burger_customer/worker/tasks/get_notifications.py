import json
import logging

import burger_customer.api as api

log = logging.getLogger(__name__)


async def on_notification(consumer):
    try:
        async for msg in consumer:
            notification = json.loads(msg.value)["message"]
            log.info(f'Notification: {notification}')
            api.notifications.append(notification)
    finally:
        log.warning('Stopping consumer')
        await consumer.stop()
