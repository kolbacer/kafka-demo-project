import uvicorn

from maker_app.api import app
import maker_app

uvicorn.run(app, host=maker_app.API_HOST, port=int(maker_app.API_PORT))
