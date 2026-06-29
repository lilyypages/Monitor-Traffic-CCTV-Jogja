from pyspark.sql.functions import col, hour, avg

from src.spark.batch.base_batch import create_spark_session
from src.config import settings

spark = create_spark_session("HourlyDensity")

JDBC_URL = f"jdbc:postgresql://{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
JDBC_PROPS = {
    "user": settings.POSTGRES_USER,
    "password": settings.POSTGRES_PASSWORD,
    "driver": "org.postgresql.Driver",
}

df = (
    spark.read.format("jdbc")
    .option("url", JDBC_URL)
    .option("dbtable", "traffic_logs")
    .options(**JDBC_PROPS)
    .load()
)

result = (
    df.withColumn("hour", hour(col("timestamp")))
    .groupBy("camera_id", "hour")
    .agg(avg("total").alias("avg_density"))
    .orderBy("hour")
)

result.show(truncate=False)

(result.write.format("jdbc")
    .option("url", JDBC_URL)
    .option("dbtable", "batch_hourly_density")
    .options(**JDBC_PROPS)
    .mode("overwrite")
    .save())