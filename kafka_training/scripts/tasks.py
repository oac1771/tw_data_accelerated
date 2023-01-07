from invoke import task
from kafka import KafkaProducer, KafkaConsumer
from datetime import datetime
import time

TOPIC = "topic"
BOOTSTRAP_SERVER = "broker:9092"

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

@task
def start_structured_stream(_):
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col
    from pyspark.sql.types import StringType


    spark = SparkSession.builder.master("spark://172.20.0.10:7077") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1") \
        .appName("Stream Processer").getOrCreate()


    df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", BOOTSTRAP_SERVER) \
        .option("subscribe", TOPIC).load()
    
    df = df.select(col("key").cast(StringType()).alias("key"), col("value").cast(StringType()).alias("value"), col("partition"))
    df.printSchema()
