from pyspark.sql import SparkSession

def create_spark_session(app_name):

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config(
            "spark.jars",
            "D:/spark-jars/postgresql-42.7.3.jar"
        )
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark