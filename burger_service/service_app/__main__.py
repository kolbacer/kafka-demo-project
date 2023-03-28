import uvicorn

from service_app.api import app
import service_app

uvicorn.run(app, host=service_app.API_HOST, port=int(service_app.API_PORT))
