if __name__ == "__main__":
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col
    from pyspark.sql import functions as f

    PER_CAPITA_EMISSIONS = "Per capita CO2 emissions"
    PER_CAPITA_CONSUMPTION = "Per capita consumption-based CO2 emissions"
    CO2_EMISSIONS_EMBEDED = "CO2 emissions embedded in trade"

    columns = [PER_CAPITA_EMISSIONS, PER_CAPITA_CONSUMPTION, CO2_EMISSIONS_EMBEDED]

    spark = SparkSession.builder.master("spark://172.20.0.10:7077").getOrCreate()
    df = spark.read.format('csv').option('header', True).load('data/temp_vs_co2/EmissionsByCountry.csv')

    # 1,2
    df.select(f.sum_distinct(PER_CAPITA_EMISSIONS), f.round(f.sum(PER_CAPITA_EMISSIONS), 3)).show()

    # 3
    df = df.select([f.sum(col(column)) for column in columns])
    df_as_dict = df.rdd.collect()[0].asDict()
    print(max(df_as_dict.values()))
    
    # 4
    df = spark.read.format('csv').option('header', True).load('data/temp_vs_co2/EmissionsByCountry.csv')
    df = df.select([f.count(col(column)) for column in columns])
    df_as_dict = df.rdd.collect()[0].asDict()
    print(f"Max Count: {max(df_as_dict.values())}")
    print(f"Min Count: {min(df_as_dict.values())}")