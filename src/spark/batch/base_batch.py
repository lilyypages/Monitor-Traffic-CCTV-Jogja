import os
from pyspark.sql import SparkSession

def create_spark_session(app_name):
    master_url = os.getenv("SPARK_MASTER", "local[*]")
    spark = (
        SparkSession.builder
        .appName(app_name)
        .master(master_url)
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark