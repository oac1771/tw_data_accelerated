import tempfile
import shutil

from invoke import task
from jinja2 import Environment, FileSystemLoader

from kafka import KafkaProducer, KafkaConsumer
from datetime import datetime
import time

TOPIC = "topic"

@task
def start_local(ctx):
    rendered_compose = render_compose()

    with open("docker/docker-compose.yml", mode="w+", encoding="utf-8") as f:
        f.write(rendered_compose)

    ctx.run("docker compose -f docker/docker-compose.yml up -d")

@task
def stop_local(ctx):
    with ctx.cd("docker"):
        ctx.run("docker compose down")

@task
def docker_build(ctx):

    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree(src="docker/", dst=f"{temp_dir}/docker")
        shutil.copytree(src="scripts/", dst=f"{temp_dir}/docker/scripts")

        with ctx.cd(f"{temp_dir}/docker"):
            ctx.run("docker build -f kafka_broker.Dockerfile . -t kafka:latest")
            ctx.run("docker build -f proxy.Dockerfile . -t proxy-kafka:latest")



def render_compose():
    environment = Environment(loader=FileSystemLoader("docker/"))
    template = environment.get_template("docker-compose.yml.jinja")

    f = template.render()
    return f

@task
def create_topic(_, topic_name=TOPIC, num_partitions=1, replication_factor=1):
    from kafka.admin import KafkaAdminClient, NewTopic
    
    admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092", 
    )
    print(f"Creating new topic: {topic_name}")
    new_topic = [NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
    admin_client.create_topics(new_topics=new_topic, validate_only=False)

@task
def produce(_):
    producer = KafkaProducer(bootstrap_servers="localhost:9092")

    while True:
        print("Sending data...")
        producer.send(topic=TOPIC, value=f"{datetime.now()}".encode())
        time.sleep(2)


@task
def consume(_):
    consumer = KafkaConsumer(TOPIC, bootstrap_servers="localhost:9092")
    print("Starting Consume Process")

    for message in consumer:
        print(f"message: {message}")

    print("done")