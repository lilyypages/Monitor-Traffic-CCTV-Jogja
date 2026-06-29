from pyspark.sql.functions import *

from src.spark.batch.base_batch import create_spark_session
from src.config import settings

spark = create_spark_session("PredictionInput")

DB_CONFIG = {
    "url": f"jdbc:postgresql://{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
    "table": "traffic_logs",
    "user": settings.POSTGRES_USER,
    "password": settings.POSTGRES_PASSWORD,
    "driver": "org.postgresql.Driver",
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