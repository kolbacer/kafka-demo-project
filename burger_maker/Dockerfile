FROM python:3.11.2-slim-buster as base

WORKDIR /code

COPY maker_app /code/maker_app
COPY requirements.txt /code

ENV API_HOST=127.0.0.1
ENV API_PORT=8001
ENV KAFKA_COOKING_TOPIC=cooking
ENV KAFKA_BOOTSTRAP_SERVERS=localhost:9092

RUN pip install -r requirements.txt

EXPOSE 8001
CMD ["python", "-m", "maker_app"]