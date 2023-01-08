from invoke import task
from kafka import KafkaProducer, KafkaConsumer
from datetime import datetime
import time

TOPIC = "topic"
BOOTSTRAP_SERVER = "kafka-broker:9092"

@task
def produce(_):
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)

    while True:
        print("Sending data...")
        producer.send(topic=TOPIC, value=f"{datetime.now()}".encode())
        time.sleep(2)


@task
def consume(_):
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=BOOTSTRAP_SERVER)
    print("Starting Consume Process")

    for message in consumer:
        print(f"message: {message}")

    print("done")

@task
def create_topic(_, topic_name=TOPIC, num_partitions=1, replication_factor=1):
    from kafka.admin import KafkaAdminClient, NewTopic
    
    admin_client = KafkaAdminClient(
        bootstrap_servers=BOOTSTRAP_SERVER, 
    )
    print(f"Creating new topic: {topic_name}")
    new_topic = [NewTopic(name="test", num_partitions=num_partitions, replication_factor=replication_factor)]
    admin_client.create_topics(new_topics=new_topic, validate_only=False)

