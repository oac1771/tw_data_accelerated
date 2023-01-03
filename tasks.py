import tempfile
import shutil
from invoke import task

PATH_TO_SPARK_DEPENDENCIES = "/opt/homebrew/Cellar/apache-spark/3.3.1/libexec/"

@task
def foo(_):
    from pyspark.sql import SparkSession
    from pyspark.sql import Window
    from pyspark.sql.types import FloatType
    from pyspark.sql.functions import col
    import pyspark.sql.functions as f

    PER_CAPITA_EMISSIONS = "Per capita CO2 emissions"

    spark = SparkSession.builder.master("spark://172.20.0.10:7077").getOrCreate()
    df = spark.read.format('csv').option('header',True).load('data/temp_vs_co2/EmissionsByCountry.csv')
    emitters = df.select("Entity", "Year", PER_CAPITA_EMISSIONS)

    w = Window.partitionBy("Entity")
    emitters.withColumn("max per capita emissions", f.max(PER_CAPITA_EMISSIONS).over(w))\
        .where(f.col('max per capita emissions') == f.col('Per Capita CO2 emissions'))\
        .drop('max per capita emissions').sort('Per Capita CO2 emissions').show(truncate=False)
    
    # emitters = emitters.na.drop()
    # emitters = emitters.withColumn(PER_CAPITA_EMISSIONS, col(PER_CAPITA_EMISSIONS).cast(FloatType()))
    # max_emitters = emitters.groupBy("Entity").max(PER_CAPITA_EMISSIONS).collect()
    # for emitter in max_emitters:
    #     print(emitter)




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

