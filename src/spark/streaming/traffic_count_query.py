from pyspark.sql.functions import *
from pyspark.sql.types import *

from src.spark.streaming.base_stream import create_spark_session

spark = create_spark_session("TrafficCountQuery")

schema = StructType([
    StructField("timestamp", StringType()),
    StructField("camera_id", StringType()),
    StructField("car", IntegerType()),
    StructField("motorcycle", IntegerType()),
    StructField("bus", IntegerType()),
    StructField("truck", IntegerType()),
    StructField("person", IntegerType()),
    StructField("total", IntegerType()),
    StructField("fps", DoubleType())
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

traffic_per_minute = (
    df
    .groupBy(
        window(col("event_time"), "1 minute"),
        col("camera_id")
    )
    .agg(
        sum("total").alias("vehicle_count")
    )
)

query = (
    traffic_per_minute.writeStream
    .outputMode("complete")
    .format("console")
    .option("truncate", False)
    .start()
)

query.awaitTermination()