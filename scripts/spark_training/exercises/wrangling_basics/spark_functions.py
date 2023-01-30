if __name__ == "__main__":
    from pyspark.sql import SparkSession
    from pyspark.sql.types import FloatType
    from pyspark.sql.functions import col, when

    PER_CAPITA_EMISSIONS = "Per capita CO2 emissions"

    spark = SparkSession.builder.master("spark://spark-master:7077").getOrCreate()
    df = spark.read.format('csv').option('header',True).load('data/temp_vs_co2/EmissionsByCountry.csv')
    df = df.withColumn(PER_CAPITA_EMISSIONS, col(PER_CAPITA_EMISSIONS).cast(FloatType()))

    df_average_emission = df.groupBy("Entity").avg(PER_CAPITA_EMISSIONS)
    total_entities = df_average_emission.count()
    new_df = df_average_emission.filter(col("avg(Per capita CO2 emissions)") > 10.0)

    new_df.show()
    entities_with_average_emissions_higher_than_10 = new_df.count()

    print(entities_with_average_emissions_higher_than_10/total_entities)