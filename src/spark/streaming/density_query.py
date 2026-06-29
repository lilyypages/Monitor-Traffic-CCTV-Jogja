from pyspark.sql.functions import col, from_json, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

from src.spark.streaming.base_stream import create_spark_session
from src.config import settings

spark = create_spark_session("DensityQuery")

AREA_SIZE = 100
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
    .option("startingOffsets", "latest")
    .load()
)

df = (
    df_raw.selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
)

density_df = df.withColumn("density", col("total") / lit(AREA_SIZE))


def write_to_postgres(batch_df, batch_id):
    (batch_df.write.format("jdbc")
        .option("url", JDBC_URL)
        .option("dbtable", "traffic_density")
        .options(**JDBC_PROPS)
        .mode("append")
        .save())


query = (
    density_df.writeStream
    .outputMode("append")
    .foreachBatch(write_to_postgres)
    .option("checkpointLocation", "/tmp/checkpoints/density")
    .start()
)

query.awaitTermination()