import asyncio
import logging

from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from starlette.responses import HTMLResponse
from pydantic import BaseModel

import customer_app.worker as worker

app = FastAPI()

log = logging.getLogger(__name__)

notifications = []
count = 0


class BurgerOrder(BaseModel):
    burger_name: str
    customer_name: str


@app.on_event("startup")
async def startup_event():
    log.info('Initializing API ...')
    await worker.initialize()


@app.on_event("shutdown")
async def shutdown_event():
    log.info('Shutting down API')
    await worker.stop()


@app.get("/")
async def root():
    return {"message": "I'm eating!"}


@app.post("/eat")
async def eat(burgerOrder: BurgerOrder):
    consumption_producer = await worker.get_consumption_producer()
    await consumption_producer.send_and_wait(worker.KAFKA_CONSUMPTION_TOPIC,
                                             burgerOrder.json().encode('utf-8'))
    return burgerOrder


async def notification_generator(request):
    global count
    while True:
        if await request.is_disconnected():
            log.warning("Client disconnected!")
            break
        if count < len(notifications):
            count += 1
            yield notifications[count-1]
        await asyncio.sleep(1)


@app.get('/stream-notifications')
async def stream(request: Request):
    event_generator = notification_generator(request)
    return EventSourceResponse(event_generator)


@app.get('/board', response_class=HTMLResponse)
async def board():
    html_content = """
        <html>
            <head>
                <title>Notification board</title>
            </head>
            <body>
                <h1>Notifications:</h1>
                <div id="notifications">
                </div>
                <script>
                    var source = new EventSource("/stream-notifications");
                    source.onmessage = function(event) {
                        document.getElementById("notifications").innerHTML += event.data + "<br>";
                    };
                </script>
            </body>
        </html>
        """
    return HTMLResponse(content=html_content, status_code=200)
