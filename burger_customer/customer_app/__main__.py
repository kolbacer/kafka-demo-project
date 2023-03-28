import uvicorn

from customer_app.api import app
import customer_app

uvicorn.run(app, host=customer_app.API_HOST, port=int(customer_app.API_PORT))
