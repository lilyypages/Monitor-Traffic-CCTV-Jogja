from pyspark.sql.functions import *

from src.spark.batch.base_batch import create_spark_session

spark = create_spark_session("HourlyDensity")

DB_CONFIG = {
    "url": "jdbc:postgresql://localhost:5432/traffic_monitor",
    "table": "traffic_logs",
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

df = (
    spark.read
    .format("jdbc")
    .options(**DB_CONFIG)
    .load()
)

df = df.withColumn(
    "hour",
    hour(col("timestamp"))
)

result = (
    df.groupBy("camera_id", "hour")
    .agg(
        avg("total").alias("avg_density")
    )
    .orderBy("hour")
)

result.show(truncate=False)