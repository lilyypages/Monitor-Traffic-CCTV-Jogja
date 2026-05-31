from pyspark.sql.functions import *
from pyspark.sql.types import *

from src.spark.streaming.base_stream import create_spark_session

spark = create_spark_session("AggregationQuery")

schema = StructType([
    StructField("timestamp", StringType()),
    StructField("camera_id", StringType()),
    StructField("total", IntegerType())
])

df_raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "traffic-events")
    .load()
)

df = (
    df_raw
    .selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
)

df = df.withColumn(
    "event_time",
    to_timestamp(col("timestamp"))
)

agg_df = (
    df
    .groupBy(
        window(col("event_time"), "5 minutes"),
        col("camera_id")
    )
    .agg(
        min("total").alias("min_count"),
        max("total").alias("max_count"),
        avg("total").alias("avg_count")
    )
)

query = (
    agg_df.writeStream
    .outputMode("complete")
    .format("console")
    .option("truncate", False)
    .start()
)

query.awaitTermination()