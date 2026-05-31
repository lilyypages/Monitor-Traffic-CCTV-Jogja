from pyspark.sql.functions import *

from src.spark.batch.base_batch import create_spark_session

spark = create_spark_session("PeakHourAnalysis")

DB_CONFIG = {
    "url": "jdbc:postgresql://localhost:5432/traffic_monitor",
    "table": "traffic_logs",
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

df = spark.read.format("jdbc").options(**DB_CONFIG).load()

df = df.withColumn("hour", hour(col("timestamp")))

hourly = (
    df.groupBy("camera_id", "hour")
    .agg(sum("total").alias("vehicle_total"))
)

peak = (
    hourly.orderBy(col("vehicle_total").desc())
)

peak.show(10, truncate=False)