from invoke import task

@task
def foo(_):
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.master("spark://172.20.0.10:7077").getOrCreate()
    df = spark.read.format('json').load('data/students/student.json')
