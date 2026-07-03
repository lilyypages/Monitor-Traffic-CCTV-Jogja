from pyspark.sql.functions import *

from src.spark.batch.base_batch import create_spark_session
from src.config import settings

spark = create_spark_session("WeekdayWeekend")

DB_CONFIG = {
    "url": f"jdbc:postgresql://{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
    "dbtable": "traffic_logs",
    "user": settings.POSTGRES_USER,
    "password": settings.POSTGRES_PASSWORD,
    "driver": "org.postgresql.Driver",
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
