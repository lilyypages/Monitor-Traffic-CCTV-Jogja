from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PreDownload").master("local[1]").config(
    "spark.jars.packages",
    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
    "org.postgresql:postgresql:42.7.3",
).getOrCreate()
spark.stop()
print("[dummy] Packages downloaded successfully.")
