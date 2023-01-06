from invoke import task
from kafka import KafkaProducer, KafkaConsumer
from datetime import datetime
import time

TOPIC = "topic"

@task
def produce(_):
    producer = KafkaProducer(bootstrap_servers="broker:9092")

    while True:
        print("Sending data...")
        producer.send(topic=TOPIC, value=f"{datetime.now()}".encode())
        time.sleep(2)


@task
def consume(_):
    consumer = KafkaConsumer(TOPIC, bootstrap_servers="broker:9092")
    print("Starting Consume Process")

    for message in consumer:
        print(f"message: {message}")

    print("done")