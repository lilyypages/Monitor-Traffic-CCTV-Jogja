from pyspark.sql.functions import *

from src.spark.batch.base_batch import create_spark_session

spark = create_spark_session("WeeklyTrend")

DB_CONFIG = {
    "url": "jdbc:postgresql://localhost:5432/traffic_monitor",
    "table": "traffic_logs",
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

df = spark.read.format("jdbc").options(**DB_CONFIG).load()

df = df.withColumn(
    "day_name",
    date_format(col("timestamp"), "EEEE")
)

trend = (
    df.groupBy("day_name")
    .agg(
        avg("total").alias("avg_traffic")
    )
)

trend.show(truncate=False)