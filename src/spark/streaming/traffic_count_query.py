from pyspark.sql.functions import col, from_json, to_timestamp, window, sum as _sum
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType,
)

from src.spark.streaming.base_stream import create_spark_session
from src.config import settings

spark = create_spark_session("TrafficCountQuery")

JDBC_URL = f"jdbc:postgresql://{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
JDBC_PROPS = {
    "user": settings.POSTGRES_USER,
    "password": settings.POSTGRES_PASSWORD,
    "driver": "org.postgresql.Driver",
}

schema = StructType([
    StructField("timestamp", StringType()),
    StructField("camera_id", StringType()),
    StructField("car", IntegerType()),
    StructField("motorcycle", IntegerType()),
    StructField("bus", IntegerType()),
    StructField("truck", IntegerType()),
    StructField("person", IntegerType()),
    StructField("total", IntegerType()),
    StructField("fps", DoubleType()),
])

df_raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", settings.KAFKA_BROKER)
    .option("subscribe", settings.TOPIC_EVENTS)
    .load()
)

df = (
    df_raw.selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
    .withColumn("event_time", to_timestamp(col("timestamp")))
)

traffic_per_minute = (
    df.groupBy(window(col("event_time"), "1 minute"), col("camera_id"))
    .agg(_sum("total").alias("vehicle_count"))
    .select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("camera_id"),
        col("vehicle_count"),
    )
)


def write_to_postgres(batch_df, batch_id):
    (batch_df.write.format("jdbc")
        .option("url", JDBC_URL)
        .option("dbtable", "traffic_count_minutely")
        .options(**JDBC_PROPS)
        .mode("overwrite")
        .save())


query = (
    traffic_per_minute.writeStream
    .outputMode("complete")
    .foreachBatch(write_to_postgres)
    .option("checkpointLocation", "/tmp/checkpoints/traffic_count")
    .start()
)

query.awaitTermination()