import uvicorn

from burger_maker.api import app
import burger_maker

uvicorn.run(app, host=burger_maker.API_HOST, port=burger_maker.API_PORT)
