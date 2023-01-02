import tempfile
import shutil
from invoke import task

PATH_TO_SPARK_DEPENDENCIES = "/opt/homebrew/Cellar/apache-spark/3.3.1/libexec/"

@task
def foo(_):
    from pyspark.sql import SparkSession
    # from pyspark import SparkConf
    spark = SparkSession.builder.master("spark://172.20.0.10:7077").getOrCreate()
    # sparkConf = SparkConf()
    # sparkConf.setMaster("spark://172.20.0.10:7077")
    # spark = SparkSession.builder.config(conf=sparkConf).getOrCreate()

    df = spark.read.csv("data/temp_vs_co2/EmissionsByCountry.csv")
    df.printSchema()

@task
def start_local(ctx):
    with ctx.cd("docker"):
        ctx.run("docker compose up -d")

@task
def stop_local(ctx):
    with ctx.cd("docker"):
        ctx.run("docker compose down")


@task
def docker_build(ctx):

    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree(src=PATH_TO_SPARK_DEPENDENCIES, dst=f"{temp_dir}/libexec")
        shutil.copytree(src="docker/", dst=f"{temp_dir}/docker")
        shutil.copy(src="docker/entrypoint.sh", dst=temp_dir)
        shutil.copy(src="docker/proxy-entrypoint.sh", dst=temp_dir)

        with ctx.cd(temp_dir):
            ctx.run("docker build -f docker/spark.Dockerfile . -t spark:latest")
            ctx.run("docker build -f docker/proxy.Dockerfile . -t proxy:latest")

