import uvicorn

from burger_service.api import app
import burger_service

uvicorn.run(app, host=burger_service.API_HOST, port=burger_service.API_PORT)
