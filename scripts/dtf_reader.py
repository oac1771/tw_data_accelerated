if __name__ == "__main__":
    from pyspark.sql import SparkSession
    from pyspark.sql.types import (
        StructType,
        StructField,
        DoubleType,
        StringType,
        ArrayType,
        FloatType,
    )

    spark = SparkSession.builder.master("spark://172.20.0.10:7077").getOrCreate()
    df_schema = StructType(
        [
            StructField("id", DoubleType(), True),
            StructField("name", StringType(), True),
            StructField("subjects", ArrayType(StringType()), True),
            StructField("total_marks", FloatType(), True),
            StructField(
                "address", StructType([StructField("city", StringType(), True)]), True
            ),
        ]
    )
    df = spark.read.schema(df_schema).json("data/students/student.json")

    df.show()
    df.printSchema()