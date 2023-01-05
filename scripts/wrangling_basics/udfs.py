if __name__ == "__main__":

    from pyspark.sql import SparkSession
    from pyspark.sql.types import StringType
    from pyspark.sql import functions as f

    spark = SparkSession.builder.master("spark://172.20.0.10:7077").getOrCreate()
    df = spark.read.format('json').load('data/students/student.json')

    def grade(mark):
        if mark > 90:
            output = "A"
        elif mark > 80:
            output = "B"
        elif mark > 70:
            output = "C"
        elif mark > 60:
            output = "D"
        else:
            output = "F"
        return output

    determine_grade = spark.udf.register('determine_grade', grade, StringType())

    df.select(f.col("name"),determine_grade(f.col("total_marks")).alias("grade")).show()