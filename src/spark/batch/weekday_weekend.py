from pyspark.sql.functions import *

from src.spark.batch.base_batch import create_spark_session

spark = create_spark_session("WeekdayWeekend")

DB_CONFIG = {
    "url": "jdbc:postgresql://localhost:5432/traffic_monitor",
    "table": "traffic_logs",
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

df = spark.read.format("jdbc").options(**DB_CONFIG).load()

df = df.withColumn(
    "day_num",
    dayofweek(col("timestamp"))
)

df = df.withColumn(
    "category",
    when(col("day_num").isin([1, 7]), "Weekend")
    .otherwise("Weekday")
)

result = (
    df.groupBy("category")
    .agg(
        avg("total").alias("avg_traffic")
    )
)

result.show()