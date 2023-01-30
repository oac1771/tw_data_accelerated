if __name__ == "__main__":
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col
    from pyspark.sql.types import IntegerType, FloatType
    from pyspark.sql import functions as f
    import plotly.express as px


    spark = SparkSession.builder.master("spark://spark-master:7077").getOrCreate()

    df = spark.read.format('csv').option('header',True).load('data/temp_vs_co2/EmissionsByCountry.csv')

    df = df.select(col("Year"), col("Entity").alias("Country"), col("Annual CO2 emissions").alias("TotalEmissions"))
    df = df.filter(col("Country") != f.lit("World")).groupBy("Country").agg(f.avg(col("TotalEmissions")).alias("TotalEmissions")).sort(col("TotalEmissions").desc())

    fig = px.bar(df.toPandas(), x="Country", y="TotalEmissions")
