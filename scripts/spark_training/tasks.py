from invoke import task
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StringType

TOPIC = "topic"
BOOTSTRAP_SERVER = "host.docker.internal:9092"

@task
def start_structured_stream(_):

    spark = SparkSession.builder.master("spark://spark-master:7077") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1") \
        .appName("Stream Processer").getOrCreate()


    df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", BOOTSTRAP_SERVER) \
        .option("subscribe", TOPIC).load()

    query = df.select(col("key").cast(StringType()).alias("key"), col("value").cast(StringType()).alias("value"), col("partition")) \
        .writeStream \
        .format("console") \
        .option("checkpointLocation", "checkpoint/") \
        .start()

    query.awaitTermination()
