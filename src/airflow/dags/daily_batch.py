from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'traffic_daily_batch',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    catchup=False,
    tags=['traffic', 'batch'],
) as dag:

    hourly_density = SparkSubmitOperator(
        task_id='hourly_density',
        application='/opt/spark-app/src/spark/batch/hourly_density.py',
        conn_id='spark_default',
        verbose=True,
    )

    peak_hour = SparkSubmitOperator(
        task_id='peak_hour_analysis',
        application='/opt/spark-app/src/spark/batch/peak_hour_analysis.py',
        conn_id='spark_default',
        verbose=True,
    )

    weekly_trend = SparkSubmitOperator(
        task_id='weekly_trend',
        application='/opt/spark-app/src/spark/batch/weekly_trend.py',
        conn_id='spark_default',
        verbose=True,
    )

    weekday_weekend = SparkSubmitOperator(
        task_id='weekday_weekend',
        application='/opt/spark-app/src/spark/batch/weekday_weekend.py',
        conn_id='spark_default',
        verbose=True,
    )

    prediction_input = SparkSubmitOperator(
        task_id='prediction_input',
        application='/opt/spark-app/src/spark/batch/prediction_input.py',
        conn_id='spark_default',
        verbose=True,
    )

    [hourly_density, peak_hour] >> weekly_trend >> weekday_weekend >> prediction_input
