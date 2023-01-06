if __name__ == "__main__":
    from pyspark.sql import SparkSession
    from pyspark.sql.types import FloatType
    from pyspark.sql import functions as f

    spark = SparkSession.builder.master("spark://172.20.0.10:7077").getOrCreate()
    df = spark.read.format('json').load('data/students/student.json')

    jebbys = df.filter(f.lower(f.col("name")).contains("jebby"))
    almost_perfect_attendance = df.filter(f.col("total_days_present") > 90)

    jebbys_with_almost_perfect_attendance = jebbys.alias("jebbys").join(
        almost_perfect_attendance.alias("attendance"), f.col("jebbys.`name`") == f.col("attendance.`name`"),
        "inner"
    )

    print(f"Jebbys with almost perfect attendance: {jebbys_with_almost_perfect_attendance.count()}")
    print(f"jebbys: {jebbys.count()}")
    print(f"people with almost perfect attendance: {almost_perfect_attendance.count()}")
