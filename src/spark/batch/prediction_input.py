from pyspark.sql.functions import *

from src.spark.batch.base_batch import create_spark_session

spark = create_spark_session("PredictionInput")

DB_CONFIG = {
    "url": "jdbc:postgresql://localhost:5432/traffic_monitor",
    "table": "traffic_logs",
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

df = spark.read.format("jdbc").options(**DB_CONFIG).load()

dataset = (
    df.select(
        "timestamp",
        "camera_id",
        "total",
        "car",
        "motorcycle",
        "bus",
        "truck",
        "person"
    )
)

dataset.write.mode("overwrite").csv(
    "data/processed/ml_input",
    header=True
)

print("ML dataset exported")