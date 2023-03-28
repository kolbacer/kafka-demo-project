import logging
import os

# env variables
API_HOST = os.getenv('API_HOST', "127.0.0.1")
API_PORT = os.getenv('API_PORT', 8000)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
