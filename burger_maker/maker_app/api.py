from fastapi import FastAPI
from pydantic import BaseModel

import logging

import maker_app.worker as worker

app = FastAPI()

log = logging.getLogger(__name__)


class Burger(BaseModel):
    name: str
    price: float


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
    return {"message": "I'm working!"}


@app.post("/make")
async def make(burger: Burger):
    cooking_producer = await worker.get_cooking_producer()
    await cooking_producer.send_and_wait(worker.KAFKA_COOKING_TOPIC,
                                         burger.json().encode('utf-8'))
    return burger
