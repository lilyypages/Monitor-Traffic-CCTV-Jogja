from pyspark.sql.functions import *
from pyspark.sql.types import *

from src.spark.streaming.base_stream import create_spark_session

spark = create_spark_session("AlertQuery")

THRESHOLD = 80

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

alerts = df.filter(col("total") > THRESHOLD)

query = (
    alerts.writeStream
    .outputMode("append")
    .format("console")
    .start()
)

query.awaitTermination()