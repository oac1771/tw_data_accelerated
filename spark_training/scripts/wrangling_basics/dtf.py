if __name__ == "__main__":
    from pyspark.sql import SparkSession
    import pandas as pd

    spark = SparkSession.builder.master("spark://172.20.0.10:7077").getOrCreate()

    int_list = [[i] for i in range(100)]
    df = spark.createDataFrame(int_list, ['Numbers'])
    df.show()

    a_set = (('Manu','100'),('Aditya','90'))
    df = spark.createDataFrame(a_set, ['Name', 'EnergyMeter'])
    df.show()

    pandas_dataframe = pd.DataFrame({'first':range(200), 'second':range(300,500)})
    df = spark.createDataFrame(pandas_dataframe)
    df.show()
    print(type(pandas_dataframe))
    print(type(df))