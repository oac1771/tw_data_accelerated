if __name__ == "__main__":
    from pyspark.sql import SparkSession
    from pyspark.sql.types import FloatType
    from pyspark.sql.functions import col

    PER_CAPITA_EMISSIONS = "Per capita CO2 emissions"

    spark = SparkSession.builder.master("spark://172.20.0.10:7077").getOrCreate()
    df = spark.read.format('csv').option('header',True).load('data/temp_vs_co2/EmissionsByCountry.csv')
    emitters = df.select("Entity", "Year", PER_CAPITA_EMISSIONS)
    emitters = emitters.na.drop()

    print(">>> Each countries highest recorded co2 emission ordered highest to lowest")
    emitters = emitters.withColumn(PER_CAPITA_EMISSIONS, col(PER_CAPITA_EMISSIONS).cast(FloatType()))
    emitters.groupBy("Entity").max(PER_CAPITA_EMISSIONS).sort(col('max(Per capita CO2 emissions)').desc()).show(truncate=False)