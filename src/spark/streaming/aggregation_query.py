from pyspark.sql.functions import (
    col, from_json, to_timestamp, window, min as _min, max as _max, avg as _avg,
)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

from src.spark.streaming.base_stream import create_spark_session
from src.config import settings

spark = create_spark_session("AggregationQuery")

JDBC_URL = f"jdbc:postgresql://{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
JDBC_PROPS = {
    "user": settings.POSTGRES_USER,
    "password": settings.POSTGRES_PASSWORD,
    "driver": "org.postgresql.Driver",
}

schema = StructType([
    StructField("timestamp", StringType()),
    StructField("camera_id", StringType()),
    StructField("total", IntegerType()),
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

agg_df = (
    df.groupBy(window(col("event_time"), "5 minutes"), col("camera_id"))
    .agg(
        _min("total").alias("min_count"),
        _max("total").alias("max_count"),
        _avg("total").alias("avg_count"),
    )
    .select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("camera_id"),
        col("min_count"),
        col("max_count"),
        col("avg_count"),
    )
)


def write_to_postgres(batch_df, batch_id):
    (batch_df.write.format("jdbc")
        .option("url", JDBC_URL)
        .option("dbtable", "traffic_aggregated")
        .options(**JDBC_PROPS)
        .mode("overwrite")
        .save())


query = (
    agg_df.writeStream
    .outputMode("complete")
    .foreachBatch(write_to_postgres)
    .option("checkpointLocation", "/tmp/checkpoints/aggregation")
    .start()
)

query.awaitTermination()