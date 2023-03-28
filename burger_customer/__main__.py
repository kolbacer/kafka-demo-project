import uvicorn

from burger_customer.api import app
import burger_customer

uvicorn.run(app, host=burger_customer.API_HOST, port=burger_customer.API_PORT)
