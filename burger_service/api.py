from fastapi import FastAPI

import logging

import burger_service.worker as worker
import burger_service.db as db

app = FastAPI()

log = logging.getLogger(__name__)


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


@app.get("/burgerlist")
async def burgerlist():
    return await db.get_burgers()


@app.get("/orderlist")
async def orderlist():
    return await db.get_orders()
