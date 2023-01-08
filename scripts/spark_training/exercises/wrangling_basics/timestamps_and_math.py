if __name__ == "__main__":
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as f
    from pyspark.sql.functions import col

    PER_CAPITA_EMISSIONS = "Per capita CO2 emissions"
    PER_CAPITA_CONSUMPTION = "Per capita consumption-based CO2 emissions"

    spark = SparkSession.builder.master("spark://172.20.0.10:7077").getOrCreate()
    df = spark.read.format('csv').option('header', True).load('data/temp_vs_co2/EmissionsByCountry.csv')
    df = df.select(
        (col(PER_CAPITA_CONSUMPTION) / col(PER_CAPITA_EMISSIONS)).alias('ratio'), col("Entity")
    ).na.drop().orderBy(f.desc("ratio"))

    df.show()