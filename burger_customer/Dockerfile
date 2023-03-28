FROM python:3.11.2-slim-buster as base

WORKDIR /code

COPY customer_app /code/customer_app
COPY requirements.txt /code

ENV API_HOST=127.0.0.1
ENV API_PORT=8000
ENV KAFKA_CONSUMPTION_TOPIC=consumption
ENV KAFKA_NOTIFICATION_TOPIC=notification
ENV KAFKA_CONSUMER_GROUP=customer_group
ENV KAFKA_BOOTSTRAP_SERVERS=localhost:9092

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "-m", "customer_app"]