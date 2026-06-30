from pyspark.sql.functions import col, from_json, to_json, struct
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

from src.spark.streaming.base_stream import create_spark_session
from src.config import settings

spark = create_spark_session("AlertQuery")

THRESHOLD = settings.DENSITY_THRESHOLD

schema = StructType([
    StructField("timestamp", StringType()),
    StructField("camera_id", StringType()),
    StructField("car", IntegerType()),
    StructField("motorcycle", IntegerType()),
    StructField("bus", IntegerType()),
    StructField("truck", IntegerType()),
    StructField("person", IntegerType()),
    StructField("total", IntegerType()),
    StructField("delta", IntegerType()),
    StructField("fps", DoubleType()),
])

df_raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", settings.KAFKA_BROKER)
    .option("subscribe", settings.TOPIC_EVENTS)
    .option("startingOffsets", "latest")
    .load()
)

df = (
    df_raw.selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
)

alerts = df.filter(col("delta") > THRESHOLD)

alerts_kafka = alerts.select(
    col("camera_id").cast("string").alias("key"),
    to_json(struct("timestamp", "camera_id", "delta", "total")).alias("value"),
)

query = (
    alerts_kafka.writeStream
    .format("kafka")
    .option("kafka.bootstrap.servers", settings.KAFKA_BROKER)
    .option("topic", settings.TOPIC_ALERTS)
    .option("checkpointLocation", "/tmp/checkpoints/alerts")
    .outputMode("append")
    .start()
)

query.awaitTermination()